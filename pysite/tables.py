from typing import List, NamedTuple


class Table(NamedTuple):
    primary_key: str
    keys: List[str]
    locked: bool = True


TABLES = {
    "bot_events": Table(  # Events to be sent to the bot via websocket
        primary_key="id",
        keys=sorted([
            "id",
            "data"
        ])
    ),

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

    "code_jams": Table(  # Information about each code jam
        primary_key="number",
        keys=sorted([
            "date_end",  # datetime
            "date_start",  # datetime
            "end_html",  # str
            "end_rst",  # str
            "info_rst",  # str
            "info_html",  # str
            "number",  # int
            "participants",  # list[str]
            "repo",  # str
            "state",  # str
            "task_html",  # str
            "task_rst",  # str
            "teams",  # list[str]
            "theme",  # str
            "title",  # str
            "winning_team"  # str
        ])
    ),

    "code_jam_forms": Table(  # Application forms for each jam
        primary_key="number",
        keys=sorted([
            "number",  # int
            "preamble_rst",  # str
            "preamble_html",  # str
            "questions"  # list[dict[str, str]]  {title, type, input_type, options?}
        ])
    ),

    "code_jam_questions": Table(  # Application form questions
        primary_key="id",
        keys=sorted([
            "data",  # dict
            "id",  # uuid
            "optional",  # bool
            "title",  # str
            "type",  # str
        ])
    ),

    "code_jam_responses": Table(  # Application form responses
        primary_key="id",
        keys=sorted([
            "id",  # uuid
            "snowflake",  # str
            "jam",  # int
            "answers",  # list [{question, answer, metadata}]
            "approved"  # bool
        ])
    ),

    "code_jam_teams": Table(  # Teams for each jam
        primary_key="id",
        keys=sorted([
            "id",  # uuid
            "name",  # str
            "members",  # list[str]
            "repo",  # str
            "jam"  # int
        ])
    ),

    "code_jam_infractions": Table(  # Individual infractions for each user
        primary_key="id",
        keys=sorted([
            "id",  # uuid
            "participant",  # str
            "reason",  # str
            "number",  # int (optionally -1 for permanent)
            "decremented_for"  # list[int]
        ])
    ),

    "code_jam_participants": Table(  # Info for each participant
        primary_key="id",
        keys=sorted([
            "id",  # str
            "gitlab_username",  # str
            "timezone"  # str
        ])
    ),

    "member_chunks": Table(
        primary_key="id",
        keys=sorted([
            "id",  # str
            "chunk",  # list
        ])
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

    "off_topic_names": Table(  # Names for the off-topic category channels
        primary_key="name",
        keys=("name",),
        locked=False
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

    "special_snakes": Table(  # Special case snakes for the snake converter
        primary_key="name",
        keys=sorted([
            "name",
            "info",
            "image_list",
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
            "avatar",
            "user_id",
            "roles",
            "username",
            "discriminator"
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
        primary_key="id",
        keys=sorted([
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
    ),

    "pydoc_links": Table(  # pydoc_links
        primary_key="package",
        keys=sorted([
            "base_url",
            "inventory_url",
            "package"
        ]),
        locked=False
    ),

    "bot_settings": Table(
        primary_key="key",
        keys=sorted([
            "key",  # str
            "value"  # any
        ])
    ),

    "watched_users": Table(  # Users being monitored by the bot's BigBrother cog
        primary_key="user_id",
        keys=sorted([
            "user_id",
            "channel_id"
        ])
    )
}
