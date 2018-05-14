from typing import List, NamedTuple


class Table(NamedTuple):
    primary_key: str
    keys: List[str]
    locked: bool = True


TABLES = {
    "hiphopify": Table(  # Users in hiphop prison
        primary_key="user_id",
        keys=sorted([
            "user_id",
            "end_timestamp",
            "forced_nick"
        ])
    ),

    "hiphopify_namelist": Table(  # Names and images of hiphop artists
        primary_key="name",
        keys=sorted([
            "name",
            "image_url"
        ]),
        locked=False
    ),

    "oauth_data": Table(  # OAuth login information
        primary_key="id",
        keys=sorted([
            "id",
            "access_token",
            "expires_at",
            "refresh_token",
            "snowflake"
        ])
    ),

    "snake_facts": Table(  # Snake facts
        primary_key="fact",
        keys=sorted([
            "fact"
        ]),
        locked=False
    ),

    "snake_idioms": Table(  # Snake idioms
        primary_key="idiom",
        keys=sorted([
            "idiom"
        ]),
        locked=False
    ),

    "snake_movies": Table(  # Snake movies
        primary_key="movie",
        keys=sorted([
            "movie"
        ]),
        locked=False
    ),

    "snake_names": Table(  # Snake names
        primary_key="name",
        keys=sorted([
            "name",
            "scientific"
        ]),
        locked=False
    ),

    "snake_quiz": Table(  # Snake questions and answers
        primary_key="id",
        keys=sorted([
            "id",
            "question",
            "options",
            "answerkey"
        ]),
        locked=False
    ),

    "tags": Table(  # Tag names and values
        primary_key="tag_name",
        keys=sorted([
            "tag_name",
            "tag_content"
        ]),
        locked=False
    ),

    "users": Table(  # Users from the Discord server
        primary_key="user_id",
        keys=sorted([
            "user_id",
            "roles",
            "username",
            "discriminator",
            "email"
        ])
    ),

    "wiki": Table(  # Wiki articles
        primary_key="slug",
        keys=sorted([
            "slug",
            "headers",
            "html",
            "rst",
            "text",
            "title"
        ])
    ),

    "wiki_revisions": Table(  # Revisions of wiki articles
        primary_key="id", keys=sorted([
            "id",
            "date",
            "post",
            "slug",
            "user"
        ])
    ),

    "_versions": Table(  # Table migration versions
        primary_key="table",
        keys=sorted([
            "table",
            "version"
        ])
    )
}
