CREATE TABLE IF NOT EXISTS users_data
(
    user_id integer NOT NULL,
    CONSTRAINT users_config_pkey PRIMARY KEY (user_id)
);

CREATE TABLE IF NOT EXISTS users_news
(
    user_id integer NOT NULL,
    cnbc boolean DEFAULT false,
    wall_street_journal boolean DEFAULT false,
    marketwatch boolean DEFAULT false,
    bloomberg boolean DEFAULT false,
    forbes boolean DEFAULT false,
    "коммерсантъ" boolean DEFAULT false,
    "лента" boolean DEFAULT false,
    russia_today boolean DEFAULT false,
    kase_news boolean DEFAULT false,
    CONSTRAINT users_news_pkey PRIMARY KEY (user_id),
    CONSTRAINT users_news_user_id_fkey FOREIGN KEY (user_id)
        REFERENCES users_data (user_id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS users_news_notification
(
    user_id integer NOT NULL,
    cnbc boolean DEFAULT false,
    wall_street_journal boolean DEFAULT false,
    marketwatch boolean DEFAULT false,
    bloomberg boolean DEFAULT false,
    forbes boolean DEFAULT false,
    "коммерсантъ" boolean DEFAULT false,
    "лента" boolean DEFAULT false,
    russia_today boolean DEFAULT false,
    kase_news boolean DEFAULT false,
    CONSTRAINT users_news_notification_pkey PRIMARY KEY (user_id),
    CONSTRAINT users_news_notification_user_id_fkey FOREIGN KEY (user_id)
        REFERENCES users_data (user_id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
);