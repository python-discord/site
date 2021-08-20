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

INSERT INTO users VALUES (
    1,
    current_timestamp
);

CREATE TABLE channels (
    id varchar,
    name varchar,
    primary key(id)
);

INSERT INTO channels VALUES(
    '267659945086812160',
    'python-general'
);

INSERT INTO channels VALUES(
    '11',
    'help-apple'
);

INSERT INTO channels VALUES(
    '12',
    'help-cherry'
);

INSERT INTO channels VALUES(
    '21',
    'ot0-hello'
);

INSERT INTO channels VALUES(
    '22',
    'ot1-world'
);

INSERT INTO channels VALUES(
    '31',
    'voice-chat-0'
);

INSERT INTO channels VALUES(
    '32',
    'code-help-voice-0'
);

INSERT INTO channels VALUES(
    '1234',
    'zebra'
);

CREATE TABLE messages (
    id varchar,
    author_id varchar references users(id),
    is_deleted boolean,
    created_at timestamp,
    channel_id varchar references channels(id),
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

INSERT INTO messages VALUES(
    2,
    0,
    false,
    now(),
    '11'
);

INSERT INTO messages VALUES(
    3,
    0,
    false,
    now(),
    '12'
);

INSERT INTO messages VALUES(
    4,
    1,
    false,
    now(),
    '21'
);

INSERT INTO messages VALUES(
    5,
    1,
    false,
    now(),
    '22'
);

INSERT INTO messages VALUES(
    6,
    1,
    false,
    now(),
    '31'
);

INSERT INTO messages VALUES(
    7,
    1,
    false,
    now(),
    '32'
);

INSERT INTO messages VALUES(
    8,
    1,
    true,
    now(),
    '32'
);
