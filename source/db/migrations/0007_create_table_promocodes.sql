CREATE TABLE promocodes (
    id SERIAL PRIMARY KEY,
    code VARCHAR(16) UNIQUE NOT NULL,
    count_activation INTEGER,
    duration VARCHAR(64)
);
