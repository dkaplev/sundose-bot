# ☀️ SunDose Bot — Engagement Features Specification

Extra features to maximize daily retention and fun. Ordered by recommended implementation priority.

---

## Phase 1: MVP Extras (zero or near-zero dev cost, ship with v1)

---

### Feature 1 — Streak Personas

**What it is:**
The streak counter has a name that evolves as the user progresses. Not just "🔥 7 days" — the bot addresses you by your current title.

**Why it works:**
People come back to see what they'll become next. Identity-based habits are significantly more durable than outcome-based ones.

**Implementation:**
Add a `streak_persona` computed field based on `streak` count. Display in daily notification and on `/streak` command.

**Persona table:**

| Streak | Title (RU) | Title (EN) |
|---|---|---|
| 1–2 | Любопытный Новичок 🌱 | Curious Newbie 🌱 |
| 3–6 | Охотник за Солнцем 🌤 | Sun Seeker 🌤 |
| 7–13 | Солнечный Падаван ⚡ | Solar Apprentice ⚡ |
| 14–29 | Бронзовый Ящер 🦎 | Bronze Lizard 🦎 |
| 30–59 | Дитя Средиземноморья 🏛 | Child of the Mediterranean 🏛 |
| 60–99 | Хранитель Фотонов 🔆 | Photon Guardian 🔆 |
| 100–179 | Древний Грек ☀️ | Ancient Greek ☀️ |
| 180–364 | Живая Легенда Загара 🌞 | Living Tan Legend 🌞 |
| 365+ | Бог Солнечного Метаболизма 👑 | God of Solar Metabolism 👑 |

**In notification:**
```
🔥 Серия: 14 дней
Статус: Бронзовый Ящер 🦎
До следующего уровня: 15 дней
```

**DB change:** No schema change needed — computed from existing `streak` field.

---

### Feature 2 — Instant UV Check (On-Demand)

**What it is:**
A persistent button (or `/now` command) available at any time. User taps it and instantly gets the current UV status — no waiting for a scheduled notification.

**Why it works:**
Transforms the bot from a passive reminder into an active utility. Creates daily pull behavior rather than just push. High open rate, low friction.

**Implementation:**
Add a `☀️ Проверить сейчас` button to the main keyboard (reply keyboard, always visible). Also accessible via `/now`.

**Response format:**
```
☀️ UV прямо сейчас в Никосии

UV-индекс: 8.4 🔥
Статус окна: АКТИВНО ✅
Осталось: ~2 ч 15 мин

Тебе нужно: 20 мин с открытыми руками и ногами
Лучшее время за день: уже сейчас

[✅ Вышел]  [⏰ Напомни через 30 мин]
```

If window is not active:
```
UV прямо сейчас в Никосии: 1.2

Окна УФ-B сегодня больше нет.
Следующее — завтра около 10:50.

[🔔 Напомни завтра за 30 мин]
```

**DB change:** None. Reuses existing UV fetch logic.

---

## Phase 2: Social & Anticipation Features

---

### Feature 3 — Evening Forecast Message

**What it is:**
A short optional evening notification (around 21:00 local time) previewing tomorrow's UV window and flagging exceptional days.

**Why it works:**
Creates anticipation. People plan their morning differently if they know tomorrow is a 10+ UV day. Night messages have strong open rates. Turns a reactive habit into a proactive one.

**Implementation:**
New scheduled job per user at 21:00 local time. Opt-in during onboarding or in `/settings`. Fetches next-day UV forecast from Open-Meteo.

**Message format:**
```
🌙 Прогноз на завтра — Никосия

Окно УФ-B: 10:45 – 14:30
Пик UV: ~10 в 12:30
Облачность: 10% (ясно) 

💡 Лучший день этой недели — не пропусти.

Напомню за 30 минут до начала, как обычно ☀️
```

On a weak UV day:
```
🌙 Прогноз на завтра — Никосия

UV-индекс: максимум 2.1 (недостаточно для синтеза D)
Облачность: 90%

Завтра — день для добавки D₃ 💊
Я напомню.
```

**DB change:** Add `evening_notify` boolean to `users` table, default FALSE.

---

### Feature 4 — The Vitamin D Oracle (Weekly)

**What it is:**
Every Sunday, the bot sends a playful "sun horoscope" based on real UV forecast data for the coming week. Funny, shareable, actually grounded in real data.

**Why it works:**
Humor is the most shareable content format on Telegram. One good oracle message gets forwarded. Drives organic growth.

**Implementation:**
Sunday job at 10:00 local time. Fetch weekly UV data. Find the peak UV moment of the week. Generate a templated "oracle" message from a pool of ~20 templates, filled with real data.

**Message pool examples:**

```
🔮 Оракул Витамина D говорит:

Во вторник в 12:33 UV в Никосии достигнет 11.4.
Это не совпадение. Это знак.
Выйди на улицу. 20 минут. Без крема.
Вселенная требует.

Лучшее окно недели: вт–ср, 11:00–13:30 ☀️
```

```
🔮 Оракул Витамина D молчалив на этой неделе.

UV не поднимется выше 3.
Звёзды говорят: пей D₃ с жирным завтраком.
Магний не забудь.
Такова воля гормонов.
```

```
🔮 Эта неделя — подарок.

UV 10+ с понедельника по пятницу.
Оракул видит тебя на балконе в обед.
Возможно, с кофе.
Определённо — без рубашки.
```

**DB change:** None.

---

### Feature 5 — Sun Duels (Friend Challenges)

**What it is:**
A user can challenge a friend to a 7-day streak duel. Both must log daily sun sessions. First to miss a day loses. Winner gets a unique badge.

**Why it works:**
Social accountability is the strongest habit-formation mechanism. Adds stakes without punishment — it's playful competition, not pressure.

**Implementation:**

1. User taps `⚔️ Вызвать друга` in `/settings` or after logging a streak of 3+
2. Bot generates a unique challenge link: `t.me/sundose_bot?start=duel_XXXXXX`
3. Recipient accepts → duel begins at midnight local time
4. Both get daily duel status update alongside normal notification
5. If one misses → the other gets a victory message + badge

**Duel notification addon:**
```
⚔️ Дуэль с Артёмом: день 4 из 7
Ты: ✅✅✅✅ | Артём: ✅✅✅✅
Держись — он не отстаёт 😤
```

**Victory message:**
```
🏆 Победа!

Артём пропустил день 5.
Ты — устоял.

Новый бейдж: Солнечный Дуэлянт ⚔️☀️
```

**DB changes:**
```sql
CREATE TABLE duels (
    id          SERIAL PRIMARY KEY,
    challenger  BIGINT REFERENCES users(telegram_id),
    opponent    BIGINT REFERENCES users(telegram_id),
    started_at  DATE,
    status      VARCHAR(20) DEFAULT 'active', -- active, completed
    winner      BIGINT REFERENCES users(telegram_id),
    token       VARCHAR(20) UNIQUE
);
```

---

### Feature 6 — Seasonal Quests

**What it is:**
Time-limited challenges tied to seasons or calendar events. Users opt in and track progress toward a goal. Completing a quest unlocks a unique badge.

**Why it works:**
Creates spikes of engagement at natural transition points. Limited-time mechanics are proven to drive re-engagement from lapsed users.

**Implementation:**
Hardcoded quest schedule. Quest announcement sent to all active users on start date. Progress tracked via `daily_logs`.

**Quest examples:**

| Quest | Trigger | Goal | Badge |
|---|---|---|---|
| ☀️ Летний старт | June 1 | 10 sessions in June | Солнечный Июнь ☀️ |
| 🦎 Ящер-марафон | July 1 | 20 sessions in July | Профессиональный Ящер 🦎 |
| ❄️ Зимний воин | Dec 1 | 15 sessions in Dec (any UV ≥ 3) | Полярный Исследователь ❄️ |
| 🌅 Ранняя пташка | Any month | 5 sessions before 11:00 | Жаворонок ☀️ |
| 🏖 Пляжный учёный | Any | Log 3 sessions with UV > 10 | УФ-Экстремал 🔆 |

**Quest announcement:**
```
🎯 Новый квест: Летний Старт

Июнь начался — и вместе с ним охота за солнцем.

Задача: выйди на улицу в УФ-B окно 10 раз за июнь.
Награда: бейдж "Солнечный Июнь ☀️"

Прогресс: 0 / 10
[✅ Участвую!]
```

**DB changes:**
```sql
CREATE TABLE quests (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(100),
    start_date  DATE,
    end_date    DATE,
    goal        SMALLINT
);

CREATE TABLE user_quests (
    user_id     BIGINT REFERENCES users(telegram_id),
    quest_id    INT REFERENCES quests(id),
    progress    SMALLINT DEFAULT 0,
    completed   BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (user_id, quest_id)
);
```

---

## Phase 3: Depth & Community Features

---

### Feature 7 — Cumulative Dose Tracker ("Skin Memory")

**What it is:**
The bot tracks an estimated cumulative vitamin D synthesized over the week, displayed in IU (international units). Sunday summary shows the weekly total.

**Why it works:**
Makes the invisible visible. Watching a number grow is intrinsically satisfying. Directionally accurate enough to be useful, specific enough to feel like data.

**Implementation:**
After each logged session, calculate estimated IU based on: UV index at session time, skin type, exposed area, session duration (use recommended duration as proxy). Store per `daily_logs` row.

**Estimation formula (approximate):**
```python
# Base IU for skin type 3 (medium), arms+legs, UV=6, 20 min ≈ 3000 IU
base_iu = 3000
skin_multiplier = {1: 2.0, 2: 1.5, 3: 1.0, 4: 0.6, 5: 0.4}
area_multiplier = {'arms': 0.6, 'arms_legs': 1.0, 'full': 1.4}
uv_multiplier = uv_index / 6
time_multiplier = min(duration / 20, 1.5)  # caps at 150% — no infinite D

estimated_iu = base_iu * skin_multiplier[skin_type] * area_multiplier[area] * uv_multiplier * time_multiplier
```

**Sunday summary:**
```
📊 Итоги недели — Никосия

Сессий: 5 из 7 дней ✅
Примерный синтез: ~14,200 МЕ за неделю
Жировые запасы: довольны 😌
Серия: 12 дней 🔥
Статус: Бронзовый Ящер 🦎

На следующей неделе UV прогноз: отличный ☀️
```

**DB change:** Add `estimated_iu` column to `daily_logs`.

---

### Feature 8 — Escalating "Did You Know" Tips

**What it is:**
The 50 tips in the tip rotation are unlocked progressively. First 2 weeks: basic tips. After that: increasingly surprising, counterintuitive, or strange facts. The bot feels like it's revealing deeper secrets the longer you use it.

**Why it works:**
Mirrors the "onion" metaphor — the longer you stick with it, the stranger and more interesting it gets. Creates a reason to stay engaged beyond the habit itself.

**Implementation:**
Tips split into 3 tiers. Tier unlocked based on `streak` or `days_active` count.

| Tier | Unlock condition | Content |
|---|---|---|
| 🟢 Basic (tips 1–20) | Always available | Core mechanism, UV basics, skin types |
| 🟡 Intermediate (tips 21–35) | 7+ day streak | Paradoxes (Cyprus deficiency, inuits), evolution, deficiency scale |
| 🔴 Advanced (tips 36–50) | 30+ day streak | Vitamin K2 synergy, magnesium dependency, ancestral data, astronaut bone loss |

When a new tier unlocks:
```
🔓 Новый уровень разблокирован!

Ты уже 7 дней подряд выходишь на солнце.
Открываю тебе следующий слой 🧅

Теперь в советах дня — более редкие факты.
Те, которые знают немногие.
```

**DB change:** None — computed from `streak` field.

---

### Feature 9 — City Leaderboard (Opt-in)

**What it is:**
An optional weekly leaderboard showing average sessions per user by city. No names, no individual rankings — only aggregate city stats. Opt-in only.

**Why it works:**
Creates a sense of community and local identity without the pressure of personal competition. Also genuinely funny when Moscow averages 0.3 sessions in February.

**Implementation:**
Opt-in flag in `/settings`. Sunday aggregation job. Only cities with 3+ opted-in users are shown (privacy threshold).

**Weekly message:**
```
🏙 Солнечный рейтинг городов — эта неделя

1. Лимассол 🇨🇾 — 5.8 сессий/чел ☀️☀️☀️
2. Никосия 🇨🇾 — 5.1 сессий/чел ☀️☀️☀️
3. Афины 🇬🇷 — 4.7 сессий/чел ☀️☀️
4. Тель-Авив 🇮🇱 — 4.2 сессий/чел ☀️☀️
5. Стамбул 🇹🇷 — 3.9 сессий/чел ☀️

...

🏚 Москва 🇷🇺 — 0.4 сессий/чел ❄️
(Оракул скорбит)

Ты: 5 сессий — выше среднего по Никосии 💪
```

**DB changes:**
Add `leaderboard_opt_in` boolean to `users`, default FALSE.

---

### Feature 10 — Bring a Friend to the Sun

**What it is:**
When a user logs a session, they can optionally note they went with someone. After 5 shared sessions, both users (if both are in the bot) unlock a joint badge.

**Why it works:**
Turns a solitary habit into a social ritual. The most durable habits are the ones embedded in relationships. Also drives referral growth naturally.

**Implementation:**

After tapping "Вышел ✅", show optional followup:
```
Отлично! Ты был один или с кем-то? ☀️

[🙋 Один]  [👫 С кем-то]
```

If "С кем-то":
```
Здорово! Они тоже в SunDose?
Отправь им эту ссылку — если они присоединятся,
вы оба разблокируете бейдж "Солнечные Напарники" 👫☀️

t.me/sundose_bot?start=duo_XXXXXX
```

After 5 logged shared sessions (both users must confirm):
```
👫 Солнечные Напарники!

Вы с [именем] вместе поймали солнце 5 раз.
Новый совместный бейдж: Солнечные Напарники 👫☀️

Дружба, укреплённая гормонами. Буквально.
```

**DB changes:**
```sql
ALTER TABLE daily_logs ADD COLUMN shared_with BIGINT REFERENCES users(telegram_id);

CREATE TABLE user_badges (
    user_id     BIGINT REFERENCES users(telegram_id),
    badge_slug  VARCHAR(50),
    earned_at   TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (user_id, badge_slug)
);
```

---

## Implementation Roadmap

| Phase | Features | Effort | Impact |
|---|---|---|---|
| MVP (v1) | Streak Personas (#1), Instant UV Check (#2) | Low | High |
| v1.5 | Evening Forecast (#3), Weekly Oracle (#4) | Low | High |
| v2 | Sun Duels (#5), Seasonal Quests (#6) | Medium | Very High |
| v3 | Dose Tracker (#7), Escalating Tips (#8) | Medium | Medium |
| v4 | City Leaderboard (#9), Duo Sessions (#10) | Medium | High |

---

## Badge Registry (full list)

For reference — all badges mentioned across features:

| Badge slug | Display name | How earned |
|---|---|---|
| `solar_apprentice` | Солнечный Падаван ⚡ | 7-day streak |
| `bronze_lizard` | Бронзовый Ящер 🦎 | 14-day streak |
| `ancient_greek` | Древний Грек ☀️ | 100-day streak |
| `sun_god` | Бог Солнечного Метаболизма 👑 | 365-day streak |
| `solar_duelist` | Солнечный Дуэлянт ⚔️ | Win a duel |
| `summer_june` | Солнечный Июнь ☀️ | 10 sessions in June quest |
| `winter_warrior` | Полярный Исследователь ❄️ | 15 sessions in December |
| `early_bird` | Жаворонок ☀️ | 5 sessions before 11:00 |
| `uv_extreme` | УФ-Экстремал 🔆 | 3 sessions with UV > 10 |
| `solar_duo` | Солнечные Напарники 👫☀️ | 5 shared sessions with a friend |
| `intermediate_unlocked` | Второй Слой 🧅 | 7-day streak (tip tier 2) |
| `advanced_unlocked` | Глубокий Слой 🧅🧅 | 30-day streak (tip tier 3) |

---

*All engagement features are additive — the core daily notification remains simple and non-intrusive regardless of which extras are enabled. Each feature can be independently toggled in the user's settings.*
