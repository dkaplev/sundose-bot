from __future__ import annotations

import secrets
from datetime import date, datetime, timedelta
from typing import Optional

from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import DailyLog, Duel, Quest, User, UserBadge, UserQuest


# ── Users ──────────────────────────────────────────────────────────────────

async def get_user(session: AsyncSession, telegram_id: int) -> Optional[User]:
    result = await session.execute(select(User).where(User.telegram_id == telegram_id))
    return result.scalar_one_or_none()


async def create_user(session: AsyncSession, telegram_id: int, language: str = "ru") -> User:
    user = User(telegram_id=telegram_id, language=language)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def get_or_create_user(session: AsyncSession, telegram_id: int) -> tuple[User, bool]:
    user = await get_user(session, telegram_id)
    if user:
        return user, False
    return await create_user(session, telegram_id), True


async def update_user(session: AsyncSession, telegram_id: int, **kwargs) -> None:
    await session.execute(update(User).where(User.telegram_id == telegram_id).values(**kwargs))
    await session.commit()


async def get_active_users(session: AsyncSession) -> list[User]:
    result = await session.execute(select(User).where(User.active == True, User.city != None))
    return list(result.scalars().all())


# ── Streak & logging ────────────────────────────────────────────────────────

async def log_daily(
    session: AsyncSession,
    user_id: int,
    log_date: date,
    went_out: bool,
    uv_at_time: Optional[float] = None,
    recommended_min: Optional[int] = None,
    estimated_iu: Optional[int] = None,
    session_hour: Optional[int] = None,
    shared_with: Optional[int] = None,
) -> None:
    entry = DailyLog(
        user_id=user_id,
        log_date=log_date,
        went_out=went_out,
        uv_at_time=uv_at_time,
        recommended_min=recommended_min,
        estimated_iu=estimated_iu,
        session_hour=session_hour,
        shared_with=shared_with,
        logged_at=datetime.utcnow(),
    )
    session.add(entry)
    await session.commit()


async def apply_went_out(
    session: AsyncSession,
    user: User,
    log_date: date,
    uv: Optional[float] = None,
    minutes: Optional[int] = None,
    session_hour: Optional[int] = None,
) -> int:
    if user.last_out == log_date:
        return user.streak

    from core.iu import estimate_iu
    iu = None
    if uv and minutes and user.skin_type:
        iu = estimate_iu(user.skin_type, user.exposed_area, uv, minutes)

    new_streak = user.streak + 1
    await update_user(session, user.telegram_id, streak=new_streak, last_out=log_date)
    await log_daily(
        session, user.telegram_id, log_date, went_out=True,
        uv_at_time=uv, recommended_min=minutes, estimated_iu=iu, session_hour=session_hour,
    )
    await update_quest_progress(session, user.telegram_id, log_date, uv, session_hour)
    return new_streak


async def apply_skipped(session: AsyncSession, user: User, log_date: date) -> int:
    if user.last_out is None or (log_date - user.last_out).days > 1:
        await update_user(session, user.telegram_id, streak=0)
        await log_daily(session, user.telegram_id, log_date, went_out=False)
        return 0
    await log_daily(session, user.telegram_id, log_date, went_out=False)
    return user.streak


# ── Tips (tiered) ──────────────────────────────────────────────────────────

def _tip_range(streak: int) -> int:
    if streak >= 30:
        return 50
    if streak >= 7:
        return 35
    return 20


async def get_next_tip(session: AsyncSession, user: User) -> tuple[str, bool, bool]:
    """Return (tip_text, tier2_unlocked, tier3_unlocked)."""
    from core.tips import TIPS

    available = _tip_range(user.streak)
    idx = user.tip_index % available
    tip = TIPS[idx]
    next_index = (user.tip_index + 1) % available

    await update_user(session, user.telegram_id, tip_index=next_index)

    tier2_new = user.streak == 7 and not await has_badge(session, user.telegram_id, "intermediate_unlocked")
    tier3_new = user.streak == 30 and not await has_badge(session, user.telegram_id, "advanced_unlocked")

    if tier2_new:
        await award_badge(session, user.telegram_id, "intermediate_unlocked")
    if tier3_new:
        await award_badge(session, user.telegram_id, "advanced_unlocked")

    return tip, tier2_new, tier3_new


# ── Badges ─────────────────────────────────────────────────────────────────

async def has_badge(session: AsyncSession, user_id: int, slug: str) -> bool:
    result = await session.execute(
        select(UserBadge).where(UserBadge.user_id == user_id, UserBadge.badge_slug == slug)
    )
    return result.scalar_one_or_none() is not None


async def award_badge(session: AsyncSession, user_id: int, slug: str) -> bool:
    if await has_badge(session, user_id, slug):
        return False
    session.add(UserBadge(user_id=user_id, badge_slug=slug))
    await session.commit()
    return True


async def check_streak_badge(session: AsyncSession, user_id: int, streak: int) -> Optional[str]:
    from core.personas import check_streak_badge as _check
    slug = _check(streak)
    if slug and await award_badge(session, user_id, slug):
        return slug
    return None


# ── Weekly stats ───────────────────────────────────────────────────────────

async def get_weekly_stats(session: AsyncSession, user_id: int) -> dict:
    week_start = datetime.utcnow().date() - timedelta(days=6)
    result = await session.execute(
        select(DailyLog).where(
            DailyLog.user_id == user_id,
            DailyLog.log_date >= week_start,
            DailyLog.went_out == True,
        )
    )
    logs = list(result.scalars().all())
    total_iu = sum(l.estimated_iu or 0 for l in logs)
    return {"sessions": len(logs), "total_iu": total_iu}


# ── City leaderboard ───────────────────────────────────────────────────────

async def get_leaderboard(session: AsyncSession) -> list[dict]:
    week_start = datetime.utcnow().date() - timedelta(days=6)
    result = await session.execute(
        select(User.city, func.count(DailyLog.id).label("sessions"))
        .join(DailyLog, DailyLog.user_id == User.telegram_id)
        .where(
            User.leaderboard_opt_in == True,
            DailyLog.log_date >= week_start,
            DailyLog.went_out == True,
        )
        .group_by(User.city)
        .having(func.count(User.telegram_id.distinct()) >= 3)
        .order_by(func.count(DailyLog.id).desc())
    )
    return [{"city": row.city, "sessions": row.sessions} for row in result]


# ── Duels ──────────────────────────────────────────────────────────────────

async def create_duel(session: AsyncSession, challenger_id: int) -> Duel:
    token = secrets.token_urlsafe(12)
    duel = Duel(challenger=challenger_id, token=token)
    session.add(duel)
    await session.commit()
    await session.refresh(duel)
    return duel


async def get_duel_by_token(session: AsyncSession, token: str) -> Optional[Duel]:
    result = await session.execute(select(Duel).where(Duel.token == token))
    return result.scalar_one_or_none()


async def accept_duel(session: AsyncSession, duel: Duel, opponent_id: int) -> None:
    duel.opponent = opponent_id
    duel.status = "active"
    duel.started_at = datetime.utcnow().date()
    await session.commit()


async def get_active_duel(session: AsyncSession, user_id: int) -> Optional[Duel]:
    result = await session.execute(
        select(Duel).where(
            Duel.status == "active",
            (Duel.challenger == user_id) | (Duel.opponent == user_id),
        )
    )
    return result.scalar_one_or_none()


async def update_duel_streak(session: AsyncSession, duel: Duel, user_id: int) -> None:
    if duel.challenger == user_id:
        duel.challenger_streak += 1
    else:
        duel.opponent_streak += 1
    await session.commit()


async def resolve_duel(session: AsyncSession, duel: Duel, loser_id: int) -> int:
    winner_id = duel.opponent if duel.challenger == loser_id else duel.challenger
    duel.status = "completed"
    duel.winner = winner_id
    await session.commit()
    await award_badge(session, winner_id, "solar_duelist")
    return winner_id


# ── Quests ─────────────────────────────────────────────────────────────────

async def get_active_quests(session: AsyncSession) -> list[Quest]:
    today = datetime.utcnow().date()
    result = await session.execute(
        select(Quest).where(Quest.start_date <= today, Quest.end_date >= today)
    )
    return list(result.scalars().all())


async def update_quest_progress(
    session: AsyncSession,
    user_id: int,
    log_date: date,
    uv: Optional[float],
    session_hour: Optional[int],
) -> list[str]:
    quests = await get_active_quests(session)
    completed_slugs = []
    for quest in quests:
        uq_result = await session.execute(
            select(UserQuest).where(UserQuest.user_id == user_id, UserQuest.quest_id == quest.id)
        )
        uq = uq_result.scalar_one_or_none()
        if uq and uq.completed:
            continue

        qualifies = _qualifies_for_quest(quest.slug, uv, session_hour)
        if not qualifies:
            continue

        if uq is None:
            uq = UserQuest(user_id=user_id, quest_id=quest.id, progress=1)
            session.add(uq)
        else:
            uq.progress += 1

        if uq.progress >= quest.goal:
            uq.completed = True
            await award_badge(session, user_id, quest.slug)
            completed_slugs.append(quest.slug)

    await session.commit()
    return completed_slugs


def _qualifies_for_quest(slug: str, uv: Optional[float], session_hour: Optional[int]) -> bool:
    if slug == "early_bird":
        return session_hour is not None and session_hour < 11
    if slug == "uv_extreme":
        return uv is not None and uv > 10
    return True  # general session-count quests


async def get_user_quest_progress(session: AsyncSession, user_id: int, quest_id: int) -> int:
    result = await session.execute(
        select(UserQuest).where(UserQuest.user_id == user_id, UserQuest.quest_id == quest_id)
    )
    uq = result.scalar_one_or_none()
    return uq.progress if uq else 0


# ── Shared sessions ────────────────────────────────────────────────────────

async def mark_shared(session: AsyncSession, user_id: int, log_date: date, partner_id: int) -> None:
    result = await session.execute(
        select(DailyLog).where(
            DailyLog.user_id == user_id,
            DailyLog.log_date == log_date,
            DailyLog.went_out == True,
        )
    )
    log = result.scalar_one_or_none()
    if log:
        log.shared_with = partner_id
        await session.commit()

    result2 = await session.execute(
        select(DailyLog).where(
            DailyLog.user_id == user_id,
            DailyLog.went_out == True,
            DailyLog.shared_with == partner_id,
        )
    )
    shared_count = len(list(result2.scalars().all()))
    if shared_count >= 5:
        await award_badge(session, user_id, "solar_duo")
        await award_badge(session, partner_id, "solar_duo")
