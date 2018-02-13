# coding=utf-8

from enum import IntEnum


class ErrorCodes(IntEnum):
    unknown_route = 0
    unauthorized = 1
    invalid_api_key = 2
    missing_parameters = 3
