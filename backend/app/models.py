from datetime import datetime, timezone
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, JSON, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from .db import Base

def utcnow():
    return datetime.now(timezone.utc)

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    phone_hash: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    display_name: Mapped[str] = mapped_column(String(60), default="Learner")
    class_level: Mapped[str] = mapped_column(String(16), default="11")
    target_exam: Mapped[str] = mapped_column(String(24), default="MAIN_ADVANCED")
    language: Mapped[str] = mapped_column(String(16), default="en")
    daily_hours: Mapped[int] = mapped_column(Integer, default=3)
    timezone: Mapped[str] = mapped_column(String(64), default="Asia/Kolkata")
    consent_status: Mapped[str] = mapped_column(String(24), default="PENDING")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

class Topic(Base):
    __tablename__ = "topics"
    id: Mapped[int] = mapped_column(primary_key=True)
    subject: Mapped[str] = mapped_column(String(16), index=True)
    chemistry_branch: Mapped[str | None] = mapped_column(String(16), nullable=True)
    chapter: Mapped[str] = mapped_column(String(120))
    name: Mapped[str] = mapped_column(String(120))
    sequence_no: Mapped[int] = mapped_column(Integer, default=1)
    notes_md: Mapped[str] = mapped_column(Text, default="")
    video_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    formulas_json: Mapped[list] = mapped_column(JSON, default=list)
    key_points_json: Mapped[list] = mapped_column(JSON, default=list)
    active: Mapped[bool] = mapped_column(Boolean, default=True)

class Question(Base):
    __tablename__ = "questions"
    id: Mapped[int] = mapped_column(primary_key=True)
    topic_id: Mapped[int] = mapped_column(ForeignKey("topics.id"), index=True)
    subject: Mapped[str] = mapped_column(String(16))
    chapter: Mapped[str] = mapped_column(String(120))
    topic_name: Mapped[str] = mapped_column(String(120))
    question_type: Mapped[str] = mapped_column(String(24))
    difficulty: Mapped[str] = mapped_column(String(16), index=True)
    exam_level: Mapped[str] = mapped_column(String(16), default="MAIN")
    prompt_md: Mapped[str] = mapped_column(Text)
    options_json: Mapped[list] = mapped_column(JSON, default=list)
    answer_json: Mapped[dict] = mapped_column(JSON)
    solution_md: Mapped[str] = mapped_column(Text)
    common_mistake: Mapped[str] = mapped_column(Text, default="")
    concept_tags_json: Mapped[list] = mapped_column(JSON, default=list)
    pyq_year: Mapped[int | None] = mapped_column(Integer, nullable=True)
    source_license: Mapped[str] = mapped_column(String(32), default="ORIGINAL")
    active: Mapped[bool] = mapped_column(Boolean, default=True)

class TopicProgress(Base):
    __tablename__ = "topic_progress"
    __table_args__ = (UniqueConstraint("user_id", "topic_id", name="uq_user_topic_progress"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    topic_id: Mapped[int] = mapped_column(ForeignKey("topics.id"))
    status: Mapped[str] = mapped_column(String(20), default="LOCKED")
    attempts: Mapped[int] = mapped_column(Integer, default=0)
    passed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    easy_revision_suggested: Mapped[bool] = mapped_column(Boolean, default=False)

class TestAttempt(Base):
    __tablename__ = "test_attempts"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    topic_id: Mapped[int] = mapped_column(ForeignKey("topics.id"), index=True)
    attempt_no: Mapped[int] = mapped_column(Integer)
    question_ids_json: Mapped[list] = mapped_column(JSON)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    submitted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    passed: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    mode: Mapped[str] = mapped_column(String(12), default="PRACTICE")

class AttemptAnswer(Base):
    __tablename__ = "attempt_answers"
    id: Mapped[int] = mapped_column(primary_key=True)
    attempt_id: Mapped[int] = mapped_column(ForeignKey("test_attempts.id"), index=True)
    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id"))
    response_json: Mapped[dict] = mapped_column(JSON, default=dict)
    is_correct: Mapped[bool] = mapped_column(Boolean, default=False)
    time_seconds: Mapped[int] = mapped_column(Integer, default=0)

class MistakeNotebook(Base):
    __tablename__ = "mistake_notebook"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id"))
    attempt_id: Mapped[int] = mapped_column(ForeignKey("test_attempts.id"))
    response_json: Mapped[dict] = mapped_column(JSON, default=dict)
    reviewed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

class PauseToken(Base):
    __tablename__ = "pause_tokens"
    __table_args__ = (UniqueConstraint("user_id", "month_key", name="uq_user_pause_month"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    month_key: Mapped[str] = mapped_column(String(7))
    used_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

class Squad(Base):
    __tablename__ = "squads"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80))
    class_level: Mapped[str] = mapped_column(String(16))
    target_exam: Mapped[str] = mapped_column(String(24))
    timezone: Mapped[str] = mapped_column(String(64), default="Asia/Kolkata")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

class SquadMember(Base):
    __tablename__ = "squad_members"
    __table_args__ = (UniqueConstraint("squad_id", "user_id", name="uq_squad_user"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    squad_id: Mapped[int] = mapped_column(ForeignKey("squads.id"), index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    role: Mapped[str] = mapped_column(String(16), default="MEMBER")
    active: Mapped[bool] = mapped_column(Boolean, default=True)

class DoubtCard(Base):
    __tablename__ = "doubt_cards"
    id: Mapped[int] = mapped_column(primary_key=True)
    squad_id: Mapped[int] = mapped_column(ForeignKey("squads.id"), index=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    topic_id: Mapped[int] = mapped_column(ForeignKey("topics.id"))
    question_text: Mapped[str] = mapped_column(Text)
    attempt_summary: Mapped[str] = mapped_column(Text, default="")
    status: Mapped[str] = mapped_column(String(16), default="OPEN")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
