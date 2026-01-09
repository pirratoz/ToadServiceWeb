CREATE TYPE enum_task AS ENUM (
    'work',
    'reward_clan',
    'reward_marriage',
    'eat_frog',
    'eat_toad'
);


CREATE TABLE tasks (
    user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    task_type enum_task NOT NULL,
    next_run TIMESTAMP WITH TIME ZONE,
    turn BOOLEAN NOT NULL DEFAULT FALSE,
    extra JSONB DEFAULT '{}'::jsonb,
    PRIMARY KEY(user_id, task_type)
);
