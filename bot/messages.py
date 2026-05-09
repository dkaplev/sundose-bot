from __future__ import annotations

MSG: dict[str, dict[str, str]] = {
    "ru": {
        "choose_language": "🌍 Выберите язык / Choose language:",
        "welcome": (
            "☀️ <b>SunDose</b> — твой личный советник по витамину D.\n\n"
            "Витамин D — на самом деле стероидный гормон, который регулирует "
            "иммунитет, кальциевый обмен и ~300 генов. Он синтезируется в коже "
            "под действием УФ-B излучения, а не поступает «с едой».\n\n"
            "Я буду присылать тебе точное время, когда нужно выйти на улицу, "
            "и на сколько минут — с учётом твоего города, типа кожи и сезона.\n\n"
            "Давай настроим. 3 вопроса, 1 минута. Поехали!"
        ),
        "ask_city": "🏙 В каком городе ты сейчас?\nНапиши название на английском или русском:",
        "city_found": "Нашёл: <b>{display}</b> 🌍",
        "city_not_found": "❌ Город не найден. Попробуй написать иначе (например, на английском):",
        "ask_skin": "🎨 <b>Какой у тебя тип кожи?</b>\nЭто влияет на время, которое нужно провести на солнце.",
        "ask_area": "👕 <b>Сколько кожи ты обычно открываешь на улице?</b>\nБольше кожи = меньше времени нужно.",
        "ask_hour": "🔔 <b>В какое время тебе удобно получать утреннее уведомление?</b>\nБот предупредит тебя заранее — до начала УФ-B окна.",
        "setup_done": (
            "✅ <b>Готово! Всё настроено.</b>\n\n"
            "📍 Город: {city}\n🎨 Кожа: {skin}\n👕 Открытая зона: {area}\n🔔 Уведомления: в {hour}:00\n\n"
            "{window_info}\n\nПервое уведомление придёт завтра в {hour}:00 ☀️"
        ),
        "morning_notification": (
            "☀️ <b>Доброе утро!</b>\n\n"
            "Сегодняшнее УФ-B окно в {city}: <b>{window}</b>\n"
            "UV-индекс в пике: ~{uv} 🔆\n\n"
            "Рекомендую выйти на <b>{minutes} мин</b> около {best_time}\n"
            "без санскрина, с открытыми {area_text}.\n\n"
            "🔥 Серия: {streak} {days_word} | {persona}\n\n"
            "🧠 <b>Совет дня:</b>\n{tip}"
        ),
        "cloud_warning": "\n\n☁️ Сегодня облачно (~{cloud:.0f}%). УФ-B снижен, рекомендую {minutes} мин вместо {base}.",
        "winter_notification": (
            "❄️ Сегодня в {city} нет УФ-B окна (UV < 3 весь день).\n"
            "Рекомендуется принимать витамин D₃ 2000 МЕ/день с жирной едой.\n\n"
            "💊 Совет: принимай с завтраком — он обычно содержит жиры для усвоения."
        ),
        "reminder_30": "⏰ Через 30 минут начинается УФ-B окно!\n\nСамое время собраться на улицу ☀️\nНужно всего {minutes} минут.",
        "went_out_response": (
            "🎉 <b>Отлично! +1 к твоей серии.</b>\n"
            "🔥 Серия: {streak} {days_word}\n"
            "Статус: {persona}\n"
            "{next_level_line}\n\n"
            "{iu_line}"
        ),
        "next_level_line": "До следующего уровня: {days} {days_word}",
        "max_level_line": "Ты на максимальном уровне 👑",
        "iu_line": "🌞 Примерный синтез сегодня: ~{iu} МЕ",
        "skipped_response": "Окей, бывает. Завтра новое окно ☀️\nСерия: {streak} {days_word}",
        "streak_reset": "Серия сброшена. Начинаем заново — сегодня новый шанс! ☀️",
        "alone_or_together": "Ты был один или с кем-то? ☀️",
        "share_duo_link": "Здорово! Они тоже в SunDose?\nОтправь им ссылку — если присоединятся, оба разблокируете бейдж «Солнечные Напарники» 👫☀️\n\n{link}",
        "solar_duo_badge": "👫 <b>Солнечные Напарники!</b>\n\nВы вместе поймали солнце 5 раз.\nНовый бейдж: Солнечные Напарники 👫☀️\n\nДружба, укреплённая гормонами. Буквально.",
        "badge_earned": "🏅 <b>Новый бейдж:</b> {badge_name}",
        "tier2_unlock": "🔓 <b>Новый уровень разблокирован!</b>\n\nТы уже 7 дней подряд выходишь на солнце.\nОткрываю следующий слой знаний 🧅\nТеперь в советах дня — более редкие факты.",
        "tier3_unlock": "🔓 <b>Глубокий слой разблокирован!</b>\n\nТы уже 30 дней подряд. Серьёзно.\nОткрываю самые редкие факты — те, что знают немногие 🧅🧅",
        "status_header": "☀️ <b>Статус на сегодня — {city}</b>\n\n",
        "status_window": "🌞 УФ-B окно: <b>{window}</b>\nUV в пике: ~{uv}\nРекомендую: <b>{minutes} мин</b>\n\nВыйди около {best_time} с открытыми {area_text}.",
        "status_winter": "❄️ Сегодня нет УФ-B окна (UV < 3). Рекомендуется витамин D₃ 2000 МЕ/день.",
        "now_active": (
            "☀️ <b>UV прямо сейчас в {city}</b>\n\n"
            "UV-индекс: <b>{uv}</b> 🔆\nСтатус окна: АКТИВНО ✅\nОсталось: ~{remaining}\n\n"
            "Тебе нужно: <b>{minutes} мин</b> с открытыми {area_text}\nЛучшее время: прямо сейчас"
        ),
        "now_inactive": (
            "☀️ <b>UV прямо сейчас в {city}</b>\n\n"
            "UV-индекс: <b>{uv}</b>\n\n"
            "{window_msg}"
        ),
        "now_window_later": "Следующее окно сегодня около {time}.",
        "now_window_none": "Окна УФ-B сегодня больше нет. Следующее — завтра около {time}.",
        "remind_scheduled": "⏰ Напомню в {time}!",
        "streak_info": "🔥 <b>Серия: {streak} {days_word}</b>\nСтатус: {persona}\n{next_level_line}",
        "tip_message": "🧠 <b>Совет дня:</b>\n\n{tip}",
        "winter_info": (
            "❄️ <b>Зимний режим — когда солнца недостаточно</b>\n\n"
            "При UV < 3 синтез D в коже практически невозможен.\n\n"
            "<b>Рекомендации:</b>\n• Витамин D₃ 2000 МЕ/день\n• Принимать с жирной едой\n"
            "• Добавить K₂ при дозах выше 2000 МЕ\n• Проверить 25-OH-D раз в год"
        ),
        "about_text": (
            "☀️ <b>SunDose Bot</b>\n\n"
            "Помогает получать витамин D от солнца: считает оптимальное окно УФ-B "
            "для твоего города, типа кожи и UV-индекса.\n\n"
            "<b>Данные:</b>\n• UV-индекс: Open-Meteo\n• Геокодинг: Nominatim / OpenStreetMap\n\n"
            "<i>Бот не является медицинским устройством.</i>"
        ),
        "settings_menu": "⚙️ <b>Настройки</b>\nЧто хочешь изменить?",
        "city_updated": "📍 Город обновлён: <b>{display}</b>",
        "skin_updated": "🎨 Тип кожи обновлён.",
        "area_updated": "👕 Открытая зона обновлена.",
        "hour_updated": "🔔 Время уведомлений обновлено: {hour}:00",
        "lang_updated": "✅ Язык изменён на русский.",
        "evening_notify_on": "🌙 Вечерний прогноз включён! Буду присылать прогноз на завтра в ~21:00.",
        "evening_notify_off": "🌙 Вечерний прогноз отключён.",
        "leaderboard_on": "🏙 Ты в рейтинге городов! По воскресеньям получишь итоги недели по городам.",
        "leaderboard_off": "🏙 Ты вышел из рейтинга городов.",
        "stopped": "🔕 Уведомления отключены. Напиши /start, чтобы вернуться.",
        "already_registered": "С возвращением! Напиши /status чтобы увидеть окно на сегодня.",
        "error_uv": "⚠️ Не удалось получить данные UV. Попробуй позже.",
        "duel_created": "⚔️ Вызов создан!\n\nОтправь другу эту ссылку:\n{link}\n\nКак только он примет — дуэль на 7 дней начнётся.",
        "duel_accepted": "⚔️ Дуэль началась!\n\nТы вызвал {opponent}. 7 дней. Первый, кто пропустит день — проигрывает.",
        "duel_status": "⚔️ Дуэль: день {day} из 7\nТы: {my_streak} | Соперник: {opp_streak}",
        "duel_victory": "🏆 <b>Победа!</b>\n\nСоперник пропустил день.\nТы — устоял.\n\nНовый бейдж: Солнечный Дуэлянт ⚔️☀️",
        "duel_defeat": "Соперник устоял, ты — нет.\nЛучшее — враг хорошего. Завтра новое окно ☀️",
        "no_duel": "У тебя нет активной дуэли. Начни новую командой /duel.",
        "weekly_stats": (
            "📊 <b>Итоги недели — {city}</b>\n\n"
            "Вышел на солнце: {sessions} из 7 дней\n"
            "Примерный синтез: ~{total_iu:,} МЕ за неделю\n"
            "Серия: {streak} {days_word} 🔥\n"
            "Статус: {persona}"
        ),
        "evening_forecast": (
            "🌙 <b>Прогноз на завтра — {city}</b>\n\n"
            "Окно УФ-B: {window}\nПик UV: ~{uv} в {best_time}\nОблачность: {cloud:.0f}%\n\n"
            "{comment}\n\nНапомню за 30 мин до начала, как обычно ☀️"
        ),
        "evening_forecast_weak": (
            "🌙 <b>Прогноз на завтра — {city}</b>\n\n"
            "UV-индекс: максимум {uv:.1f} (недостаточно для синтеза D)\nОблачность: {cloud:.0f}%\n\n"
            "Завтра — день для добавки D₃ 💊 Я напомню."
        ),
        "forecast_comment_excellent": "💡 Лучший день этой недели — не пропусти.",
        "forecast_comment_good": "Хорошее окно, стоит выйти.",
        "forecast_comment_normal": "Стандартное окно, как обычно.",
        "days_1": "день",
        "days_2_4": "дня",
        "days_5plus": "дней",
    },
    "en": {
        "choose_language": "🌍 Choose language / Выберите язык:",
        "welcome": (
            "☀️ <b>SunDose</b> — your personal vitamin D advisor.\n\n"
            "Vitamin D is actually a steroid hormone that regulates immunity, "
            "calcium metabolism, and ~300 genes. It's synthesized in skin by UVB radiation.\n\n"
            "I'll tell you exactly when to go outside and for how long — "
            "based on your city, skin type, and season.\n\n"
            "3 questions, 1 minute. Let's go!"
        ),
        "ask_city": "🏙 What city are you in?\nType the city name:",
        "city_found": "Found: <b>{display}</b> 🌍",
        "city_not_found": "❌ City not found. Please try a different spelling:",
        "ask_skin": "🎨 <b>What is your skin type?</b>\nThis affects how long you need to stay in the sun.",
        "ask_area": "👕 <b>How much skin do you usually expose?</b>\nMore skin = less time needed.",
        "ask_hour": "🔔 <b>What time for your morning notification?</b>\nThe bot will alert you before the UVB window starts.",
        "setup_done": (
            "✅ <b>All set!</b>\n\n"
            "📍 City: {city}\n🎨 Skin: {skin}\n👕 Exposed area: {area}\n🔔 Notifications: at {hour}:00\n\n"
            "{window_info}\n\nFirst notification tomorrow at {hour}:00 ☀️"
        ),
        "morning_notification": (
            "☀️ <b>Good morning!</b>\n\n"
            "Today's UVB window in {city}: <b>{window}</b>\n"
            "Peak UV index: ~{uv} 🔆\n\n"
            "Recommended: <b>{minutes} min</b> around {best_time}\n"
            "without sunscreen, with exposed {area_text}.\n\n"
            "🔥 Streak: {streak} {days_word} | {persona}\n\n"
            "🧠 <b>Today's tip:</b>\n{tip}"
        ),
        "cloud_warning": "\n\n☁️ Cloudy today (~{cloud:.0f}%). UVB reduced — try {minutes} min instead of {base}.",
        "winter_notification": (
            "❄️ No UVB window today in {city} (UV < 3 all day).\n"
            "Consider vitamin D₃ 2000 IU/day with a fatty meal.\n\n"
            "💊 Tip: take it with breakfast."
        ),
        "reminder_30": "⏰ UVB window starts in 30 minutes!\n\nTime to head outside ☀️\nYou only need {minutes} minutes.",
        "went_out_response": (
            "🎉 <b>Great! +1 to your streak.</b>\n"
            "🔥 Streak: {streak} {days_word}\n"
            "Status: {persona}\n"
            "{next_level_line}\n\n"
            "{iu_line}"
        ),
        "next_level_line": "Next level in: {days} {days_word}",
        "max_level_line": "You're at the maximum level 👑",
        "iu_line": "🌞 Estimated synthesis today: ~{iu} IU",
        "skipped_response": "OK, happens. New window tomorrow ☀️\nStreak: {streak} {days_word}",
        "streak_reset": "Streak reset. Fresh start — today is a new chance! ☀️",
        "alone_or_together": "Were you alone or with someone? ☀️",
        "share_duo_link": "Nice! Are they on SunDose?\nSend them this link — if they join, you both unlock the Solar Partners badge 👫☀️\n\n{link}",
        "solar_duo_badge": "👫 <b>Solar Partners!</b>\n\nYou caught the sun together 5 times.\nNew badge: Solar Partners 👫☀️\n\nFriendship strengthened by hormones. Literally.",
        "badge_earned": "🏅 <b>New badge:</b> {badge_name}",
        "tier2_unlock": "🔓 <b>New tier unlocked!</b>\n\nYou've gone outside 7 days in a row.\nUnlocking the next layer of knowledge 🧅\nMore unusual facts incoming.",
        "tier3_unlock": "🔓 <b>Deep layer unlocked!</b>\n\n30 days in a row. Seriously.\nUnlocking the rarest facts — the ones few know 🧅🧅",
        "status_header": "☀️ <b>Today's status — {city}</b>\n\n",
        "status_window": "🌞 UVB window: <b>{window}</b>\nPeak UV: ~{uv}\nRecommended: <b>{minutes} min</b>\n\nGo out around {best_time} with exposed {area_text}.",
        "status_winter": "❄️ No UVB window today (UV < 3). Consider vitamin D₃ 2000 IU/day.",
        "now_active": (
            "☀️ <b>UV right now in {city}</b>\n\n"
            "UV index: <b>{uv}</b> 🔆\nWindow status: ACTIVE ✅\nTime remaining: ~{remaining}\n\n"
            "You need: <b>{minutes} min</b> with exposed {area_text}\nBest time: right now"
        ),
        "now_inactive": (
            "☀️ <b>UV right now in {city}</b>\n\n"
            "UV index: <b>{uv}</b>\n\n"
            "{window_msg}"
        ),
        "now_window_later": "Next window today around {time}.",
        "now_window_none": "No more UVB window today. Next one — tomorrow around {time}.",
        "remind_scheduled": "⏰ I'll remind you at {time}!",
        "streak_info": "🔥 <b>Streak: {streak} {days_word}</b>\nStatus: {persona}\n{next_level_line}",
        "tip_message": "🧠 <b>Today's tip:</b>\n\n{tip}",
        "winter_info": (
            "❄️ <b>Winter mode — when sunlight is insufficient</b>\n\n"
            "When UV < 3 skin synthesis is near zero.\n\n"
            "<b>Recommendations:</b>\n• Vitamin D₃ 2000 IU/day\n• Take with a fatty meal\n"
            "• Add K₂ at doses above 2000 IU\n• Check 25-OH-D annually"
        ),
        "about_text": (
            "☀️ <b>SunDose Bot</b>\n\nHelps you get vitamin D from sunlight.\n\n"
            "<b>Data:</b>\n• UV index: Open-Meteo\n• Geocoding: Nominatim / OpenStreetMap\n\n"
            "<i>Not a medical device.</i>"
        ),
        "settings_menu": "⚙️ <b>Settings</b>\nWhat would you like to change?",
        "city_updated": "📍 City updated: <b>{display}</b>",
        "skin_updated": "🎨 Skin type updated.",
        "area_updated": "👕 Exposed area updated.",
        "hour_updated": "🔔 Notification time updated: {hour}:00",
        "lang_updated": "✅ Language changed to English.",
        "evening_notify_on": "🌙 Evening forecast enabled! I'll send tomorrow's preview around 21:00.",
        "evening_notify_off": "🌙 Evening forecast disabled.",
        "leaderboard_on": "🏙 You're in the city leaderboard! Weekly city stats every Sunday.",
        "leaderboard_off": "🏙 Removed from city leaderboard.",
        "stopped": "🔕 Notifications disabled. Send /start to reactivate.",
        "already_registered": "Welcome back! Use /status to see today's window.",
        "error_uv": "⚠️ Could not fetch UV data. Please try again later.",
        "duel_created": "⚔️ Challenge created!\n\nSend your friend this link:\n{link}\n\nOnce they accept — 7-day duel begins.",
        "duel_accepted": "⚔️ Duel started!\n\nYou challenged {opponent}. 7 days. First to miss a day loses.",
        "duel_status": "⚔️ Duel: day {day} of 7\nYou: {my_streak} | Opponent: {opp_streak}",
        "duel_victory": "🏆 <b>Victory!</b>\n\nYour opponent missed a day.\nYou held on.\n\nNew badge: Solar Duelist ⚔️☀️",
        "duel_defeat": "Opponent held on, you didn't.\nNew window tomorrow ☀️",
        "no_duel": "No active duel. Start one with /duel.",
        "weekly_stats": (
            "📊 <b>Weekly summary — {city}</b>\n\n"
            "Sessions: {sessions} of 7 days\n"
            "Estimated synthesis: ~{total_iu:,} IU this week\n"
            "Streak: {streak} {days_word} 🔥\n"
            "Status: {persona}"
        ),
        "evening_forecast": (
            "🌙 <b>Tomorrow's forecast — {city}</b>\n\n"
            "UVB window: {window}\nPeak UV: ~{uv} at {best_time}\nCloud cover: {cloud:.0f}%\n\n"
            "{comment}\n\nI'll remind you 30 min before, as usual ☀️"
        ),
        "evening_forecast_weak": (
            "🌙 <b>Tomorrow's forecast — {city}</b>\n\n"
            "UV index: max {uv:.1f} (insufficient for D synthesis)\nCloud cover: {cloud:.0f}%\n\n"
            "Tomorrow is a D₃ supplement day 💊 I'll remind you."
        ),
        "forecast_comment_excellent": "💡 Best day of the week — don't miss it.",
        "forecast_comment_good": "Good window, worth going out.",
        "forecast_comment_normal": "Standard window, as usual.",
        "days_1": "day",
        "days_2_4": "days",
        "days_5plus": "days",
    },
}

SKIN_NAMES = {
    "ru": {1: "очень светлая", 2: "светлая", 3: "средняя", 4: "смуглая", 5: "тёмная"},
    "en": {1: "very light", 2: "light", 3: "medium", 4: "tan", 5: "dark"},
}

AREA_NAMES = {
    "ru": {"arms": "только руки и лицо", "arms_legs": "руки + ноги", "full": "руки + ноги + живот"},
    "en": {"arms": "arms and face only", "arms_legs": "arms + legs", "full": "arms + legs + torso"},
}

AREA_NOTIFICATION = {
    "ru": {"arms": "руками и лицом", "arms_legs": "руками и ногами", "full": "руками, ногами и животом"},
    "en": {"arms": "arms and face", "arms_legs": "arms and legs", "full": "arms, legs, and torso"},
}

BADGE_NAMES = {
    "ru": {
        "solar_apprentice": "Солнечный Падаван ⚡",
        "bronze_lizard": "Бронзовый Ящер 🦎",
        "ancient_greek": "Древний Грек ☀️",
        "sun_god": "Бог Солнечного Метаболизма 👑",
        "solar_duelist": "Солнечный Дуэлянт ⚔️",
        "intermediate_unlocked": "Второй Слой 🧅",
        "advanced_unlocked": "Глубокий Слой 🧅🧅",
        "solar_duo": "Солнечные Напарники 👫☀️",
        "summer_june": "Солнечный Июнь ☀️",
        "winter_warrior": "Полярный Исследователь ❄️",
        "early_bird": "Жаворонок ☀️",
        "uv_extreme": "УФ-Экстремал 🔆",
    },
    "en": {
        "solar_apprentice": "Solar Apprentice ⚡",
        "bronze_lizard": "Bronze Lizard 🦎",
        "ancient_greek": "Ancient Greek ☀️",
        "sun_god": "God of Solar Metabolism 👑",
        "solar_duelist": "Solar Duelist ⚔️",
        "intermediate_unlocked": "Second Layer 🧅",
        "advanced_unlocked": "Deep Layer 🧅🧅",
        "solar_duo": "Solar Partners 👫☀️",
        "summer_june": "Sunny June ☀️",
        "winter_warrior": "Polar Explorer ❄️",
        "early_bird": "Early Bird ☀️",
        "uv_extreme": "UV Extremist 🔆",
    },
}


def t(lang: str, key: str, **kwargs) -> str:
    text = MSG.get(lang, MSG["ru"]).get(key, MSG["ru"].get(key, key))
    return text.format(**kwargs) if kwargs else text


def days_word(lang: str, n: int) -> str:
    if lang == "en":
        return t(lang, "days_1") if n == 1 else t(lang, "days_5plus")
    if n % 10 == 1 and n % 100 != 11:
        return t(lang, "days_1")
    if 2 <= n % 10 <= 4 and not (12 <= n % 100 <= 14):
        return t(lang, "days_2_4")
    return t(lang, "days_5plus")
