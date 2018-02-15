# coding=utf-8

from enum import IntEnum


class ErrorCodes(IntEnum):
    unknown_route = 0
    unauthorized = 1
    invalid_api_key = 2
    missing_parameters = 3


OWNER_ROLE = 267627879762755584
ADMIN_ROLE = 267628507062992896
MODERATOR_ROLE = 267629731250176001
HELPER_ROLE = 267630620367257601
