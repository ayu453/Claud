from datetime import datetime, timezone
from sqlalchemy import select
from sqlalchemy.orm import Session
from .models import Question, TopicProgress, TestAttempt

DAILY_DIFFICULTY = ["EASY", "EASY", "EASY", "MEDIUM", "MEDIUM", "MEDIUM", "HARD"]

class QuestionBankExhausted(Exception):
    pass

def unseen_question_set(db: Session, user_id: int, topic_id: int) -> list[Question]:
    seen = set()
    attempts = db.scalars(select(TestAttempt).where(
        TestAttempt.user_id == user_id, TestAttempt.topic_id == topic_id
    )).all()
    for attempt in attempts:
        seen.update(attempt.question_ids_json or [])
    chosen = []
    for difficulty in DAILY_DIFFICULTY:
        q = db.scalar(select(Question).where(
            Question.topic_id == topic_id,
            Question.active.is_(True),
            Question.difficulty == difficulty,
            Question.id.not_in(seen) if seen else True
        ).order_by(Question.id).limit(1))
        if q is None:
            raise QuestionBankExhausted(f"Unseen {difficulty} questions exhausted for topic {topic_id}")
        chosen.append(q)
        seen.add(q.id)
    return chosen

def evaluate_answer(question: Question, response: dict) -> bool:
    return response == (question.answer_json or {})

def apply_daily_result(db: Session, user_id: int, topic_id: int, score: int) -> TopicProgress:
    progress = db.scalar(select(TopicProgress).where(
        TopicProgress.user_id == user_id, TopicProgress.topic_id == topic_id
    ))
    if progress is None:
        progress = TopicProgress(user_id=user_id, topic_id=topic_id, status="UNLOCKED")
        db.add(progress)
        db.flush()
    progress.attempts += 1
    if score >= 5:
        progress.status = "PASSED"
        progress.passed_at = datetime.now(timezone.utc)
    else:
        progress.status = "UNLOCKED"
        if progress.attempts >= 3:
            progress.easy_revision_suggested = True
    db.flush()
    return progress
