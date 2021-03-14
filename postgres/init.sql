CREATE DATABASE metricity;

\c metricity;

CREATE TABLE users (
    id varchar,
    joined_at timestamp,
    primary key(id)
);

INSERT INTO users VALUES (
    0,
    current_timestamp
);

CREATE TABLE messages (
    id varchar,
    author_id varchar references users(id),
    is_deleted boolean,
    created_at timestamp,
    channel_id varchar,
    primary key(id)
);

INSERT INTO messages VALUES(
    0,
    0,
    false,
    now(),
    '267659945086812160'
);

INSERT INTO messages VALUES(
    1,
    0,
    false,
    now() + INTERVAL '10 minutes,',
    '1234'
);
