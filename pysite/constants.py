# coding=utf-8

from enum import Enum, IntEnum


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
