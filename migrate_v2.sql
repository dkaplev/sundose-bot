-- Run this once on Railway to add new columns + tables for v2 features.
-- Safe to run multiple times (uses IF NOT EXISTS / IF EXISTS).

ALTER TABLE users ADD COLUMN IF NOT EXISTS evening_notify BOOLEAN DEFAULT FALSE;
ALTER TABLE users ADD COLUMN IF NOT EXISTS leaderboard_opt_in BOOLEAN DEFAULT FALSE;

ALTER TABLE daily_logs ADD COLUMN IF NOT EXISTS estimated_iu INTEGER;
ALTER TABLE daily_logs ADD COLUMN IF NOT EXISTS session_hour SMALLINT;
ALTER TABLE daily_logs ADD COLUMN IF NOT EXISTS shared_with BIGINT REFERENCES users(telegram_id);

CREATE TABLE IF NOT EXISTS duels (
    id              SERIAL PRIMARY KEY,
    challenger      BIGINT REFERENCES users(telegram_id),
    opponent        BIGINT REFERENCES users(telegram_id),
    started_at      DATE,
    status          VARCHAR(20) DEFAULT 'pending',
    winner          BIGINT REFERENCES users(telegram_id),
    token           VARCHAR(20) UNIQUE,
    challenger_streak SMALLINT DEFAULT 0,
    opponent_streak   SMALLINT DEFAULT 0
);

CREATE TABLE IF NOT EXISTS quests (
    id          SERIAL PRIMARY KEY,
    slug        VARCHAR(50) UNIQUE,
    name_ru     VARCHAR(100),
    name_en     VARCHAR(100),
    start_date  DATE,
    end_date    DATE,
    goal        SMALLINT
);

CREATE TABLE IF NOT EXISTS user_quests (
    user_id     BIGINT REFERENCES users(telegram_id),
    quest_id    INT REFERENCES quests(id),
    progress    SMALLINT DEFAULT 0,
    completed   BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (user_id, quest_id)
);

CREATE TABLE IF NOT EXISTS user_badges (
    user_id     BIGINT REFERENCES users(telegram_id),
    badge_slug  VARCHAR(50),
    earned_at   TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (user_id, badge_slug)
);

-- Seed initial quests
INSERT INTO quests (slug, name_ru, name_en, start_date, end_date, goal) VALUES
    ('summer_june',    'Летний Старт',          'Summer Start',      '2026-06-01', '2026-06-30', 10),
    ('summer_july',    'Ящер-марафон',           'Lizard Marathon',   '2026-07-01', '2026-07-31', 20),
    ('winter_warrior', 'Зимний Воин',            'Winter Warrior',    '2026-12-01', '2026-12-31', 15),
    ('early_bird',     'Ранняя Пташка',          'Early Bird',        '2026-01-01', '2099-12-31', 5),
    ('uv_extreme',     'Пляжный Учёный',         'Beach Scientist',   '2026-01-01', '2099-12-31', 3)
ON CONFLICT (slug) DO NOTHING;
