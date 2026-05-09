from datetime import date, datetime
from typing import Optional
from sqlalchemy import BigInteger, Boolean, Date, DateTime, Float, ForeignKey, Integer, SmallInteger, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    telegram_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    language: Mapped[str] = mapped_column(String(2), default="ru")
    city: Mapped[Optional[str]] = mapped_column(String(100))
    lat: Mapped[Optional[float]] = mapped_column(Float)
    lon: Mapped[Optional[float]] = mapped_column(Float)
    timezone: Mapped[Optional[str]] = mapped_column(String(50))
    skin_type: Mapped[Optional[int]] = mapped_column(SmallInteger)
    exposed_area: Mapped[str] = mapped_column(String(10), default="arms_legs")
    notify_hour: Mapped[int] = mapped_column(SmallInteger, default=9)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    streak: Mapped[int] = mapped_column(SmallInteger, default=0)
    last_out: Mapped[Optional[date]] = mapped_column(Date)
    tip_index: Mapped[int] = mapped_column(SmallInteger, default=0)
    evening_notify: Mapped[bool] = mapped_column(Boolean, default=False)
    leaderboard_opt_in: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())


class DailyLog(Base):
    __tablename__ = "daily_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.telegram_id"))
    log_date: Mapped[Optional[date]] = mapped_column(Date)
    went_out: Mapped[bool] = mapped_column(Boolean, default=False)
    uv_at_time: Mapped[Optional[float]] = mapped_column(Float)
    recommended_min: Mapped[Optional[int]] = mapped_column(SmallInteger)
    estimated_iu: Mapped[Optional[int]] = mapped_column(Integer)
    session_hour: Mapped[Optional[int]] = mapped_column(SmallInteger)
    shared_with: Mapped[Optional[int]] = mapped_column(BigInteger, ForeignKey("users.telegram_id"), nullable=True)
    logged_at: Mapped[Optional[datetime]] = mapped_column(DateTime)


class Duel(Base):
    __tablename__ = "duels"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    challenger: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.telegram_id"))
    opponent: Mapped[Optional[int]] = mapped_column(BigInteger, ForeignKey("users.telegram_id"), nullable=True)
    started_at: Mapped[Optional[date]] = mapped_column(Date)
    status: Mapped[str] = mapped_column(String(20), default="pending")  # pending, active, completed
    winner: Mapped[Optional[int]] = mapped_column(BigInteger, ForeignKey("users.telegram_id"), nullable=True)
    token: Mapped[str] = mapped_column(String(20), unique=True)
    challenger_streak: Mapped[int] = mapped_column(SmallInteger, default=0)
    opponent_streak: Mapped[int] = mapped_column(SmallInteger, default=0)


class Quest(Base):
    __tablename__ = "quests"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    slug: Mapped[str] = mapped_column(String(50), unique=True)
    name_ru: Mapped[str] = mapped_column(String(100))
    name_en: Mapped[str] = mapped_column(String(100))
    start_date: Mapped[Optional[date]] = mapped_column(Date)
    end_date: Mapped[Optional[date]] = mapped_column(Date)
    goal: Mapped[int] = mapped_column(SmallInteger)


class UserQuest(Base):
    __tablename__ = "user_quests"

    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.telegram_id"), primary_key=True)
    quest_id: Mapped[int] = mapped_column(Integer, ForeignKey("quests.id"), primary_key=True)
    progress: Mapped[int] = mapped_column(SmallInteger, default=0)
    completed: Mapped[bool] = mapped_column(Boolean, default=False)


class UserBadge(Base):
    __tablename__ = "user_badges"

    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.telegram_id"), primary_key=True)
    badge_slug: Mapped[str] = mapped_column(String(50), primary_key=True)
    earned_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
