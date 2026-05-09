from __future__ import annotations

PERSONAS = [
    (1,   2,   "Любопытный Новичок 🌱",        "Curious Newbie 🌱"),
    (3,   6,   "Охотник за Солнцем 🌤",         "Sun Seeker 🌤"),
    (7,   13,  "Солнечный Падаван ⚡",           "Solar Apprentice ⚡"),
    (14,  29,  "Бронзовый Ящер 🦎",             "Bronze Lizard 🦎"),
    (30,  59,  "Дитя Средиземноморья 🏛",       "Child of the Mediterranean 🏛"),
    (60,  99,  "Хранитель Фотонов 🔆",          "Photon Guardian 🔆"),
    (100, 179, "Древний Грек ☀️",               "Ancient Greek ☀️"),
    (180, 364, "Живая Легенда Загара 🌞",        "Living Tan Legend 🌞"),
    (365, 99999,"Бог Солнечного Метаболизма 👑","God of Solar Metabolism 👑"),
]

STREAK_BADGES = {
    7:   "solar_apprentice",
    14:  "bronze_lizard",
    100: "ancient_greek",
    365: "sun_god",
}


def get_persona(streak: int, lang: str) -> str:
    idx = 2 if lang == "ru" else 3
    for lo, hi, *titles in PERSONAS:
        if lo <= streak <= hi:
            return titles[idx - 2]
    return PERSONAS[0][2] if lang == "ru" else PERSONAS[0][3]


def days_to_next_level(streak: int) -> int | None:
    for lo, hi, *_ in PERSONAS:
        if lo <= streak <= hi:
            if hi == 99999:
                return None
            return hi - streak + 1
    return None


def check_streak_badge(streak: int) -> str | None:
    return STREAK_BADGES.get(streak)
