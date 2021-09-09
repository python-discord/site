CREATE TABLE IF NOT EXISTS users (
    id varchar,
    joined_at timestamp,
    primary key(id)
);

INSERT INTO users VALUES (
    0,
    current_timestamp
) ON CONFLICT (id) DO NOTHING;

INSERT INTO users VALUES (
    1,
    current_timestamp
) ON CONFLICT (id) DO NOTHING;

CREATE TABLE IF NOT EXISTS channels (
    id varchar,
    name varchar,
    primary key(id)
);

INSERT INTO channels VALUES(
    '267659945086812160',
    'python-general'
) ON CONFLICT (id) DO NOTHING;

INSERT INTO channels VALUES(
    '11',
    'help-apple'
) ON CONFLICT (id) DO NOTHING;

INSERT INTO channels VALUES(
    '12',
    'help-cherry'
) ON CONFLICT (id) DO NOTHING;

INSERT INTO channels VALUES(
    '21',
    'ot0-hello'
) ON CONFLICT (id) DO NOTHING;

INSERT INTO channels VALUES(
    '22',
    'ot1-world'
) ON CONFLICT (id) DO NOTHING;

INSERT INTO channels VALUES(
    '31',
    'voice-chat-0'
) ON CONFLICT (id) DO NOTHING;

INSERT INTO channels VALUES(
    '32',
    'code-help-voice-0'
) ON CONFLICT (id) DO NOTHING;

INSERT INTO channels VALUES(
    '1234',
    'zebra'
) ON CONFLICT (id) DO NOTHING;

CREATE TABLE IF NOT EXISTS messages (
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
) ON CONFLICT (id) DO NOTHING;

INSERT INTO messages VALUES(
    1,
    0,
    false,
    now() + INTERVAL '10 minutes,',
    '1234'
) ON CONFLICT (id) DO NOTHING;

INSERT INTO messages VALUES(
    2,
    0,
    false,
    now(),
    '11'
) ON CONFLICT (id) DO NOTHING;

INSERT INTO messages VALUES(
    3,
    0,
    false,
    now(),
    '12'
) ON CONFLICT (id) DO NOTHING;

INSERT INTO messages VALUES(
    4,
    1,
    false,
    now(),
    '21'
) ON CONFLICT (id) DO NOTHING;

INSERT INTO messages VALUES(
    5,
    1,
    false,
    now(),
    '22'
) ON CONFLICT (id) DO NOTHING;

INSERT INTO messages VALUES(
    6,
    1,
    false,
    now(),
    '31'
) ON CONFLICT (id) DO NOTHING;

INSERT INTO messages VALUES(
    7,
    1,
    false,
    now(),
    '32'
) ON CONFLICT (id) DO NOTHING;

INSERT INTO messages VALUES(
    8,
    1,
    true,
    now(),
    '32'
) ON CONFLICT (id) DO NOTHING;
