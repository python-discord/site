# coding=utf-8

from enum import Enum, IntEnum
from os import environ


class ErrorCodes(IntEnum):
    unknown_route = 0
    unauthorized = 1
    invalid_api_key = 2
    incorrect_parameters = 3
    bad_data_format = 4


class ValidationTypes(Enum):
    json = "json"
    params = "params"


OWNER_ROLE = 267627879762755584
ADMIN_ROLE = 267628507062992896
MODERATOR_ROLE = 267629731250176001
HELPER_ROLE = 267630620367257601

DISCORD_OAUTH_ID = environ.get('DISCORD_OAUTH_ID', '')
DISCORD_OAUTH_SECRET = environ.get('DISCORD_OAUTH_SECRET', '')
DISCORD_OAUTH_SCOPE = 'identify email'
