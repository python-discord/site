from enum import Enum, IntEnum
from os import environ

from flask_wtf import CSRFProtect


class ErrorCodes(IntEnum):
    unknown_route = 0
    unauthorized = 1
    invalid_api_key = 2
    incorrect_parameters = 3
    bad_data_format = 4


class ValidationTypes(Enum):
    json = "json"
    none = "none"
    params = "params"


class BotEventTypes(Enum):
    mod_log = "mod_log"

    send_message = "send_message"
    send_embed = "send_embed"

    add_role = "add_role"
    remove_role = "remove_role"


DEBUG_MODE = "FLASK_DEBUG" in environ

# All snowflakes should be strings as RethinkDB rounds them as ints
ADMIN_BOTS_ROLE = "270988689419665409"
ADMINS_ROLE = "267628507062992896"
ANNOUNCEMENTS_ROLE = "463658397560995840"
BOTS_ROLE = "277546923144249364"
CODE_JAM_CHAMPIONS_ROLE = "430492892331769857"
CONTRIBS_ROLE = "295488872404484098"
DEVOPS_ROLE = "409416496733880320"
DEVELOPERS_ROLE = "352427296948486144"
HELPERS_ROLE = "267630620367257601"
JAMMERS_ROLE = "423054537079783434"
MODERATORS_ROLE = "267629731250176001"
MUTED_ROLE = "277914926603829249"
OWNERS_ROLE = "267627879762755584"
PARTNERS_ROLE = "323426753857191936"
PYTHON_ROLE = "458226699344019457"
STREAMERS_ROLE = "462650825978806274"
SUBREDDIT_MOD_ROLE = "458226413825294336"

ALL_STAFF_ROLES = (OWNERS_ROLE, ADMINS_ROLE, MODERATORS_ROLE, DEVOPS_ROLE)
TABLE_MANAGER_ROLES = (OWNERS_ROLE, ADMINS_ROLE, DEVOPS_ROLE)
EDITOR_ROLES = ALL_STAFF_ROLES + (HELPERS_ROLE, CONTRIBS_ROLE)

SERVER_ID = 267624335836053506

DISCORD_API_ENDPOINT = "https://discordapp.com/api"

DISCORD_OAUTH_REDIRECT = "/auth/discord"
DISCORD_OAUTH_AUTHORIZED = "/auth/discord/authorized"
DISCORD_OAUTH_ID = environ.get('DISCORD_OAUTH_ID', '')
DISCORD_OAUTH_SECRET = environ.get('DISCORD_OAUTH_SECRET', '')
DISCORD_OAUTH_SCOPE = 'identify'
OAUTH_DATABASE = "oauth_data"

GITLAB_ACCESS_TOKEN = environ.get("GITLAB_ACCESS_TOKEN", '')

PREFERRED_URL_SCHEME = environ.get("PREFERRED_URL_SCHEME", "http")

ERROR_DESCRIPTIONS = {
    # 5XX
    500: "The server encountered an unexpected error ._.",
    501: "Woah! You seem to have found something we haven't even implemented yet!",
    502: "This is weird, one of our upstream servers seems to have experienced an error.",
    503: "Looks like one of our services is down for maintenance and couldn't respond to your request.",
    504: "Looks like an upstream server experienced a timeout while we tried to talk to it!",
    505: "You're using an old HTTP version. It might be time to upgrade your browser.",
    # 4XX
    400: "You sent us a request that we don't know what to do with.",
    401: "Nope! You'll need to authenticate before we let you do that.",
    403: "No way! You're not allowed to do that.",
    404: "We looked, but we couldn't seem to find that page.",
    405: "That's a real page, but you can't use that method.",
    408: "We waited a really long time, but never got your request.",
    410: "This used to be here, but it's gone now.",
    411: "You forgot to tell us the length of the content.",
    413: "No way! That payload is, like, way too big!",
    415: "The thing you sent has the wrong format.",
    418: "I'm a teapot, I can't make coffee. (._.)",
    429: "Please don't send us that many requests."
}

JAM_STATES = [
    "planning",
    "announced",
    "preparing",
    "running",
    "judging",
    "finished"
]

JAM_QUESTION_TYPES = [
    "checkbox",
    "email",
    "number",
    "radio",
    "range",
    "text",
    "textarea",
    "slider"
]

# Server role colors
ROLE_COLORS = {
    ADMIN_BOTS_ROLE: "#6f9fed",
    ADMINS_ROLE: "#e76e6c",
    BOTS_ROLE: "#6f9fed",
    CODE_JAM_CHAMPIONS_ROLE: "#b108b4",
    CONTRIBS_ROLE: "#55cc6c",
    DEVOPS_ROLE: "#a1d1ff",
    DEVELOPERS_ROLE: "#fcfcfc",
    HELPERS_ROLE: "#e0b000",
    JAMMERS_ROLE: "#258639",
    MODERATORS_ROLE: "#ce3c42",
    MUTED_ROLE: "#fcfcfc",
    OWNERS_ROLE: "#ffa3a1",
    PARTNERS_ROLE: "#b66fed",
    PYTHON_ROLE: "#6f9fed",
    STREAMERS_ROLE: "#833cba",
    SUBREDDIT_MOD_ROLE: "#d897ed",
}

# CSRF
CSRF = CSRFProtect()

# Bot key
BOT_API_KEY = environ.get("BOT_API_KEY")

# RabbitMQ settings
BOT_EVENT_QUEUE = "bot_events"

RMQ_USERNAME = environ.get("RABBITMQ_DEFAULT_USER") or "guest"
RMQ_PASSWORD = environ.get("RABBITMQ_DEFAULT_PASS") or "guest"
RMQ_HOST = "localhost" if DEBUG_MODE else environ.get("RABBITMQ_HOST") or "pdrmq"
RMQ_PORT = 5672

# Channels
CHANNEL_MOD_LOG = 282638479504965634
CHANNEL_DEV_LOGS = 409308876241108992
CHANNEL_JAM_LOGS = 452486310121439262
