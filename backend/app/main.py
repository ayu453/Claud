from datetime import datetime, timedelta, timezone
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from .db import Base, engine, get_db
from .models import User, Topic, Question, TestAttempt, AttemptAnswer, MistakeNotebook
from .schemas import DailyTestSubmit
from .progression import unseen_question_set, evaluate_answer, apply_daily_result, QuestionBankExhausted

Base.metadata.create_all(bind=engine)
app = FastAPI(title="JEE Squad API", version="0.1.0")

@app.get("/health")
def health():
    return {"status": "ok", "service": "jee-squad-api"}

@app.get("/topics")
def list_topics(db: Session = Depends(get_db)):
    topics = db.scalars(select(Topic).where(Topic.active.is_(True)).order_by(Topic.sequence_no)).all()
    return [{"id": t.id, "subject": t.subject, "chapter": t.chapter, "name": t.name} for t in topics]

@app.post("/dev/users")
def create_dev_user(phone_hash: str, display_name: str = "Learner", db: Session = Depends(get_db)):
    # Local development only; replace with verified OTP and rate limiting before deployment.
    if db.scalar(select(User).where(User.phone_hash == phone_hash)):
        raise HTTPException(409, "User already exists")
    user = User(phone_hash=phone_hash, display_name=display_name, consent_status="PENDING")
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"id": user.id, "display_name": user.display_name, "consent_status": user.consent_status}

@app.post("/dev/users/{user_id}/approve-consent")
def approve_dev_consent(user_id: int, db: Session = Depends(get_db)):
    # Development fixture only; never expose this route in production.
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(404, "User not found")
    user.consent_status = "APPROVED"
    db.commit()
    return {"user_id": user_id, "consent_status": user.consent_status}

@app.post("/users/{user_id}/topics/{topic_id}/daily-test")
def start_daily_test(user_id: int, topic_id: int, db: Session = Depends(get_db)):
    user, topic = db.get(User, user_id), db.get(Topic, topic_id)
    if not user or not topic or not topic.active:
        raise HTTPException(404, "User or topic not found")
    if user.consent_status != "APPROVED":
        raise HTTPException(403, "Guardian consent is required before study features are enabled")
    active = db.scalar(select(TestAttempt).where(
        TestAttempt.user_id == user_id, TestAttempt.topic_id == topic_id,
        TestAttempt.submitted_at.is_(None)
    ))
    if active:
        raise HTTPException(409, "An active attempt already exists")
    try:
        questions = unseen_question_set(db, user_id, topic_id)
    except QuestionBankExhausted as exc:
        raise HTTPException(409, str(exc))
    previous = db.scalars(select(TestAttempt).where(
        TestAttempt.user_id == user_id, TestAttempt.topic_id == topic_id
    )).all()
    attempt = TestAttempt(
        user_id=user_id, topic_id=topic_id, attempt_no=len(previous) + 1,
        question_ids_json=[q.id for q in questions], mode="PRACTICE",
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=20)
    )
    db.add(attempt)
    db.commit()
    db.refresh(attempt)
    return {
        "attempt_id": attempt.id, "question_count": 7, "pass_score": 5,
        "time_limit_seconds": 1200,
        "questions": [{
            "id": q.id, "question_type": q.question_type, "difficulty": q.difficulty,
            "prompt_md": q.prompt_md, "options": q.options_json
        } for q in questions]
    }

@app.post("/users/{user_id}/attempts/{attempt_id}/submit")
def submit_daily_test(user_id: int, attempt_id: int, payload: DailyTestSubmit, db: Session = Depends(get_db)):
    attempt = db.get(TestAttempt, attempt_id)
    if not attempt or attempt.user_id != user_id:
        raise HTTPException(404, "Attempt not found")
    if attempt.submitted_at:
        raise HTTPException(409, "This test set has already been submitted")
    if attempt.expires_at and datetime.now(timezone.utc) > attempt.expires_at:
        raise HTTPException(410, "Test time expired")
    issued_ids = set(attempt.question_ids_json or [])
    submitted_ids = [a.question_id for a in payload.answers]
    if len(set(submitted_ids)) != 7 or set(submitted_ids) != issued_ids:
        raise HTTPException(422, "Submit exactly the seven questions assigned to this attempt")
    questions = {q.id: q for q in db.scalars(select(Question).where(Question.id.in_(issued_ids))).all()}
    score, answer_rows = 0, []
    for answer in payload.answers:
        question = questions.get(answer.question_id)
        if not question:
            raise HTTPException(422, "Question set is invalid")
        correct = evaluate_answer(question, answer.response)
        score += int(correct)
        answer_rows.append(AttemptAnswer(
            attempt_id=attempt.id, question_id=question.id, response_json=answer.response,
            is_correct=correct, time_seconds=answer.time_seconds
        ))
        if not correct:
            db.add(MistakeNotebook(
                user_id=user_id, question_id=question.id, attempt_id=attempt.id,
                response_json=answer.response
            ))
    attempt.score, attempt.passed = score, score >= 5
    attempt.submitted_at = datetime.now(timezone.utc)
    db.add_all(answer_rows)
    progress = apply_daily_result(db, user_id, attempt.topic_id, score)
    db.commit()
    return {
        "attempt_id": attempt.id, "score": score, "out_of": 7,
        "passed": attempt.passed, "topic_status": progress.status,
        "attempts_on_topic": progress.attempts,
        "easy_revision_suggested": progress.easy_revision_suggested,
        "message": "Great work. Next topic is eligible." if attempt.passed else "No stress. Review the solutions and try a fresh set."
    }
