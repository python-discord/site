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
    params = "params"


class BotEventTypes(Enum):
    mod_log = "mod_log"

    send_message = "send_message"
    send_embed = "send_embed"

    add_role = "add_role"
    remove_role = "remove_role"


DEBUG_MODE = "FLASK_DEBUG" in environ

# All snowflakes should be strings as RethinkDB rounds them as ints
OWNER_ROLE = "267627879762755584"
ADMIN_ROLE = "267628507062992896"
MODERATOR_ROLE = "267629731250176001"
DEVOPS_ROLE = "409416496733880320"
HELPER_ROLE = "267630620367257601"
CONTRIB_ROLE = "295488872404484098"
JAMMERS_ROLE = "423054537079783434 "

ALL_STAFF_ROLES = (OWNER_ROLE, ADMIN_ROLE, MODERATOR_ROLE, DEVOPS_ROLE)
TABLE_MANAGER_ROLES = (OWNER_ROLE, ADMIN_ROLE, DEVOPS_ROLE)
EDITOR_ROLES = ALL_STAFF_ROLES + (HELPER_ROLE, CONTRIB_ROLE)

SERVER_ID = 267624335836053506

DISCORD_API_ENDPOINT = "https://discordapp.com/api"

DISCORD_OAUTH_REDIRECT = "/auth/discord"
DISCORD_OAUTH_AUTHORIZED = "/auth/discord/authorized"
DISCORD_OAUTH_ID = environ.get('DISCORD_OAUTH_ID', '')
DISCORD_OAUTH_SECRET = environ.get('DISCORD_OAUTH_SECRET', '')
DISCORD_OAUTH_SCOPE = 'identify'
OAUTH_DATABASE = "oauth_data"

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
