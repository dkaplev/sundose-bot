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
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())


class DailyLog(Base):
    __tablename__ = "daily_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.telegram_id"))
    log_date: Mapped[Optional[date]] = mapped_column(Date)
    went_out: Mapped[bool] = mapped_column(Boolean, default=False)
    uv_at_time: Mapped[Optional[float]] = mapped_column(Float)
    recommended_min: Mapped[Optional[int]] = mapped_column(SmallInteger)
    logged_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
