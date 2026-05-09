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
        "ask_skin": (
            "🎨 <b>Какой у тебя тип кожи?</b>\n"
            "Это влияет на время, которое нужно провести на солнце."
        ),
        "ask_area": (
            "👕 <b>Сколько кожи ты обычно открываешь на улице?</b>\n"
            "Влияет на расчёт времени: больше кожи = меньше времени нужно."
        ),
        "ask_hour": (
            "🔔 <b>В какое время тебе удобно получать утреннее уведомление?</b>\n"
            "Бот предупредит тебя заранее — до начала УФ-B окна."
        ),
        "setup_done": (
            "✅ <b>Готово! Всё настроено.</b>\n\n"
            "📍 Город: {city}\n"
            "🎨 Кожа: {skin}\n"
            "👕 Открытая зона: {area}\n"
            "🔔 Уведомления: в {hour}:00\n\n"
            "{window_info}\n\n"
            "Первое уведомление придёт завтра в {hour}:00 ☀️"
        ),
        "morning_notification": (
            "☀️ <b>Доброе утро!</b>\n\n"
            "Сегодняшнее УФ-B окно в {city}: <b>{window}</b>\n"
            "UV-индекс в пике: ~{uv} 🔆\n\n"
            "Рекомендую выйти на <b>{minutes} мин</b> около {best_time}\n"
            "без санскрина, с открытыми {area_text}.\n\n"
            "🧠 <b>Совет дня:</b>\n{tip}"
        ),
        "cloud_warning": "\n\n☁️ Сегодня облачно (~{cloud:.0f}%). УФ-B снижен, рекомендую выйти на {minutes} мин вместо {base}.",
        "winter_notification": (
            "❄️ Сегодня в {city} нет УФ-B окна (UV < 3 весь день).\n"
            "В этот период рекомендуется принимать витамин D₃ 2000 МЕ/день с жирной едой.\n\n"
            "💊 Совет: принимай с завтраком — он обычно содержит жиры для усвоения."
        ),
        "reminder_30": (
            "⏰ Через 30 минут начинается УФ-B окно!\n\n"
            "Самое время собраться на улицу ☀️\n"
            "Нужно всего {minutes} минут."
        ),
        "went_out_response": (
            "🎉 <b>Отлично! +1 к твоей серии.</b>\n"
            "🔥 Серия: {streak} {days_word} подряд\n\n"
            "Ты набрал свою дозу витамина D сегодня."
        ),
        "skipped_response": (
            "Окей, бывает. Завтра новое окно ☀️\n"
            "Серия: {streak} {days_word}"
        ),
        "streak_reset": "Серия сброшена. Начинаем заново — сегодня новый шанс! ☀️",
        "status_header": "☀️ <b>Статус на сегодня — {city}</b>\n\n",
        "status_window": "🌞 УФ-B окно: <b>{window}</b>\nUV в пике: ~{uv}\nРекомендую: <b>{minutes} мин</b>\n\nВыйди около {best_time} с открытыми {area_text}.",
        "status_winter": "❄️ Сегодня нет УФ-B окна (UV < 3). Рекомендуется витамин D₃ 2000 МЕ/день.",
        "streak_info": "🔥 <b>Твоя серия: {streak} {days_word}</b>\n\nПродолжай выходить на солнце каждый день!",
        "tip_message": "🧠 <b>Совет дня:</b>\n\n{tip}",
        "winter_info": (
            "❄️ <b>Зимний режим — когда солнца недостаточно</b>\n\n"
            "При UV < 3 (обычно ноябрь–февраль в умеренных широтах) синтез D в коже практически невозможен.\n\n"
            "<b>Рекомендации:</b>\n"
            "• Витамин D₃ 2000 МЕ/день (взрослым)\n"
            "• Принимать с жирной едой (ужин или завтрак)\n"
            "• Добавить K₂ при дозах выше 2000 МЕ\n"
            "• Проверить уровень 25-OH-D в крови раз в год"
        ),
        "about_text": (
            "☀️ <b>SunDose Bot</b>\n\n"
            "Помогает получать витамин D от солнца: считает оптимальное окно УФ-B "
            "для твоего города, типа кожи и UV-индекса.\n\n"
            "<b>Данные:</b>\n"
            "• UV-индекс: Open-Meteo (open-meteo.com)\n"
            "• Геокодинг: Nominatim / OpenStreetMap\n\n"
            "<i>Бот не является медицинским устройством и не заменяет консультацию врача.</i>"
        ),
        "settings_menu": "⚙️ <b>Настройки</b>\nЧто хочешь изменить?",
        "city_updated": "📍 Город обновлён: <b>{display}</b>",
        "skin_updated": "🎨 Тип кожи обновлён.",
        "area_updated": "👕 Открытая зона обновлена.",
        "hour_updated": "🔔 Время уведомлений обновлено: {hour}:00",
        "lang_updated": "✅ Язык изменён на русский.",
        "stopped": "🔕 Уведомления отключены. Напиши /start, чтобы вернуться.",
        "already_registered": "С возвращением! Напиши /status чтобы увидеть окно на сегодня.",
        "error_uv": "⚠️ Не удалось получить данные UV. Попробуй позже.",
        "days_1": "день",
        "days_2_4": "дня",
        "days_5plus": "дней",
    },
    "en": {
        "choose_language": "🌍 Choose language / Выберите язык:",
        "welcome": (
            "☀️ <b>SunDose</b> — your personal vitamin D advisor.\n\n"
            "Vitamin D is actually a steroid hormone that regulates immunity, "
            "calcium metabolism, and ~300 genes. It's synthesized in your skin "
            "by UVB radiation — not absorbed from food.\n\n"
            "I'll tell you exactly when to go outside and for how long — "
            "based on your city, skin type, and season.\n\n"
            "Let's set it up. 3 questions, 1 minute. Let's go!"
        ),
        "ask_city": "🏙 What city are you in?\nType the city name:",
        "city_found": "Found: <b>{display}</b> 🌍",
        "city_not_found": "❌ City not found. Please try a different spelling:",
        "ask_skin": (
            "🎨 <b>What is your skin type?</b>\n"
            "This affects how long you need to stay in the sun."
        ),
        "ask_area": (
            "👕 <b>How much skin do you usually expose outside?</b>\n"
            "More skin = less time needed."
        ),
        "ask_hour": (
            "🔔 <b>What time would you like your morning notification?</b>\n"
            "The bot will alert you before the UVB window starts."
        ),
        "setup_done": (
            "✅ <b>All set!</b>\n\n"
            "📍 City: {city}\n"
            "🎨 Skin: {skin}\n"
            "👕 Exposed area: {area}\n"
            "🔔 Notifications: at {hour}:00\n\n"
            "{window_info}\n\n"
            "First notification tomorrow at {hour}:00 ☀️"
        ),
        "morning_notification": (
            "☀️ <b>Good morning!</b>\n\n"
            "Today's UVB window in {city}: <b>{window}</b>\n"
            "Peak UV index: ~{uv} 🔆\n\n"
            "Recommended: <b>{minutes} min</b> around {best_time}\n"
            "without sunscreen, with exposed {area_text}.\n\n"
            "🧠 <b>Today's tip:</b>\n{tip}"
        ),
        "cloud_warning": "\n\n☁️ Cloudy today (~{cloud:.0f}%). UVB reduced — try {minutes} min instead of {base}.",
        "winter_notification": (
            "❄️ No UVB window today in {city} (UV < 3 all day).\n"
            "Consider taking vitamin D₃ 2000 IU/day with a fatty meal.\n\n"
            "💊 Tip: take it with breakfast — it usually contains fats for absorption."
        ),
        "reminder_30": (
            "⏰ UVB window starts in 30 minutes!\n\n"
            "Time to head outside ☀️\n"
            "You only need {minutes} minutes."
        ),
        "went_out_response": (
            "🎉 <b>Great! +1 to your streak.</b>\n"
            "🔥 Streak: {streak} {days_word} in a row\n\n"
            "You've got your vitamin D dose today."
        ),
        "skipped_response": "OK, happens. New window tomorrow ☀️\nStreak: {streak} {days_word}",
        "streak_reset": "Streak reset. Fresh start — today is a new chance! ☀️",
        "status_header": "☀️ <b>Today's status — {city}</b>\n\n",
        "status_window": "🌞 UVB window: <b>{window}</b>\nPeak UV: ~{uv}\nRecommended: <b>{minutes} min</b>\n\nGo out around {best_time} with exposed {area_text}.",
        "status_winter": "❄️ No UVB window today (UV < 3). Consider vitamin D₃ 2000 IU/day.",
        "streak_info": "🔥 <b>Your streak: {streak} {days_word}</b>\n\nKeep going outside every day!",
        "tip_message": "🧠 <b>Today's tip:</b>\n\n{tip}",
        "winter_info": (
            "❄️ <b>Winter mode — when sunlight is insufficient</b>\n\n"
            "When UV < 3 (typically November–February at mid-latitudes) skin synthesis is near zero.\n\n"
            "<b>Recommendations:</b>\n"
            "• Vitamin D₃ 2000 IU/day (adults)\n"
            "• Take with a fatty meal\n"
            "• Add K₂ at doses above 2000 IU\n"
            "• Check 25-OH-D blood level once a year"
        ),
        "about_text": (
            "☀️ <b>SunDose Bot</b>\n\n"
            "Helps you get vitamin D from sunlight: calculates the optimal UVB window "
            "for your city, skin type, and UV index.\n\n"
            "<b>Data sources:</b>\n"
            "• UV index: Open-Meteo (open-meteo.com)\n"
            "• Geocoding: Nominatim / OpenStreetMap\n\n"
            "<i>This bot is not a medical device and does not replace professional advice.</i>"
        ),
        "settings_menu": "⚙️ <b>Settings</b>\nWhat would you like to change?",
        "city_updated": "📍 City updated: <b>{display}</b>",
        "skin_updated": "🎨 Skin type updated.",
        "area_updated": "👕 Exposed area updated.",
        "hour_updated": "🔔 Notification time updated: {hour}:00",
        "lang_updated": "✅ Language changed to English.",
        "stopped": "🔕 Notifications disabled. Send /start to reactivate.",
        "already_registered": "Welcome back! Use /status to see today's window.",
        "error_uv": "⚠️ Could not fetch UV data. Please try again later.",
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
