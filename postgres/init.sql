CREATE DATABASE metricity;

\c metricity;

CREATE TABLE users (
    id varchar(255),
    name varchar(255) not null,
    avatar_hash varchar(255),
    joined_at timestamp not null,
    created_at timestamp not null,
    is_staff boolean not null,
    opt_out boolean default false,
    bot boolean default false,
    is_guild boolean default true,
    is_verified boolean default false,
    public_flags text default '{}',
    verified_at timestamp,
    primary key(id)
);

INSERT INTO users VALUES (
    0,
    'foo',
    'bar',
    current_timestamp,
    current_timestamp,
    false,
    false,
    false,
    true,
    false,
    '{}',
    NULL
);

CREATE TABLE messages (
    id varchar(255),
    author_id varchar(255) references users(id),
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
