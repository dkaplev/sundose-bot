from __future__ import annotations

import random

TEMPLATES_GOOD_RU = [
    (
        "🔮 Оракул Витамина D говорит:\n\n"
        "В {best_day} UV в {city} достигнет {peak_uv:.0f}.\n"
        "Это не совпадение. Это знак.\n"
        "Выйди на улицу. {minutes} минут. Без крема.\n"
        "Вселенная требует.\n\n"
        "Лучшее окно недели: {window_str} ☀️"
    ),
    (
        "🔮 Эта неделя — подарок.\n\n"
        "UV {peak_uv:.0f}+ в {city} на {good_days}.\n"
        "Оракул видит тебя на улице в обед.\n"
        "Возможно, с кофе.\n"
        "Определённо — без санскрина.\n\n"
        "Лучший момент: {window_str}"
    ),
    (
        "🔮 Солнце благосклонно к {city} на этой неделе.\n\n"
        "Пик UV: {peak_uv:.0f} в {best_day}.\n"
        "Синтез витамина D будет максимальным.\n"
        "Гормоны одобряют. Иди гулять.\n\n"
        "Рекомендую: {minutes} мин около {window_str}"
    ),
]

TEMPLATES_WEAK_RU = [
    (
        "🔮 Оракул Витамина D молчалив на этой неделе.\n\n"
        "UV не поднимется выше {peak_uv:.0f} в {city}.\n"
        "Звёзды говорят: пей D₃ с жирным завтраком.\n"
        "Магний не забудь.\n"
        "Такова воля гормонов."
    ),
    (
        "🔮 Облака скрыли солнце {city}.\n\n"
        "UV недостаточен для синтеза D всю неделю.\n"
        "Оракул предрекает: 2000 МЕ D₃ в день с едой.\n"
        "Это не трагедия. Это просто зима.\n"
        "Оракул скорбит, но с пониманием."
    ),
]

TEMPLATES_GOOD_EN = [
    (
        "🔮 The Vitamin D Oracle speaks:\n\n"
        "{best_day}: UV in {city} will reach {peak_uv:.0f}.\n"
        "This is not a coincidence. This is a sign.\n"
        "Go outside. {minutes} minutes. No sunscreen.\n"
        "The universe demands it.\n\n"
        "Best window this week: {window_str} ☀️"
    ),
    (
        "🔮 This week is a gift.\n\n"
        "UV {peak_uv:.0f}+ in {city} for {good_days}.\n"
        "The Oracle sees you outside at noon.\n"
        "Possibly with coffee.\n"
        "Definitely without a shirt.\n\n"
        "Best time: {window_str}"
    ),
    (
        "🔮 The sun smiles upon {city} this week.\n\n"
        "Peak UV: {peak_uv:.0f} on {best_day}.\n"
        "Vitamin D synthesis will be maximal.\n"
        "Your hormones approve. Go outside.\n\n"
        "Recommended: {minutes} min around {window_str}"
    ),
]

TEMPLATES_WEAK_EN = [
    (
        "🔮 The Vitamin D Oracle is quiet this week.\n\n"
        "UV won't exceed {peak_uv:.0f} in {city}.\n"
        "The stars say: take D₃ with a fatty breakfast.\n"
        "Don't forget magnesium.\n"
        "Such is the will of hormones."
    ),
    (
        "🔮 Clouds have taken {city} this week.\n\n"
        "UV insufficient for D synthesis all week.\n"
        "The Oracle predicts: 2000 IU D₃ daily with food.\n"
        "This is not a tragedy. It's just winter.\n"
        "The Oracle mourns, but understands."
    ),
]

DAYS_RU = ["понедельник", "вторник", "среду", "четверг", "пятницу", "субботу", "воскресенье"]
DAYS_EN = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def build_oracle_message(
    lang: str,
    city: str,
    peak_uv: float,
    best_weekday: int,
    window_str: str,
    minutes: int,
    good_days_count: int,
) -> str:
    is_good = peak_uv >= 3
    days = DAYS_RU if lang == "ru" else DAYS_EN
    best_day = days[best_weekday % 7]
    good_days = f"{good_days_count} дн." if lang == "ru" else f"{good_days_count} days"

    templates = (TEMPLATES_GOOD_RU if lang == "ru" else TEMPLATES_GOOD_EN) if is_good else (
        TEMPLATES_WEAK_RU if lang == "ru" else TEMPLATES_WEAK_EN
    )

    template = random.choice(templates)
    return template.format(
        city=city,
        peak_uv=peak_uv,
        best_day=best_day,
        window_str=window_str,
        minutes=minutes,
        good_days=good_days,
    )


async def fetch_weekly_uv(lat: float, lon: float, timezone: str) -> dict:
    import httpx
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "uv_index,cloud_cover",
        "timezone": timezone,
        "forecast_days": 7,
    }
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get("https://api.open-meteo.com/v1/forecast", params=params)
        resp.raise_for_status()
        return resp.json()
