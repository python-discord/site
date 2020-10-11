CREATE DATABASE metricity;

\c metricity;

CREATE TABLE users (
    id varchar,
    verified_at timestamp,
    primary key(id)
);

INSERT INTO users VALUES (
    0,
    current_timestamp
);

CREATE TABLE messages (
    id varchar,
    author_id varchar references users(id),
    primary key(id)
);

INSERT INTO messages VALUES(
    0,
    0
);

INSERT INTO messages VALUES(
    1,
    0
);
