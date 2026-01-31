CREATE TABLE history_promocodes (
    id SERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    promocode_id INTEGER NOT NULL REFERENCES promocodes(id) ON DELETE CASCADE,
    activated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT (NOW() AT TIME ZONE 'utc')
);

CREATE INDEX idx_history_user_id
ON history_promocodes(user_id);

CREATE UNIQUE INDEX idx_unique_user_promo 
ON history_promocodes (user_id, promocode_id);
