from datetime import datetime, timedelta

from rethinkdb import make_timezone


UNITS = {
    's': lambda value: value,
    'm': lambda value: value * 60,
    'h': lambda value: value * 60 * 60,
    'd': lambda value: value * 60 * 60 * 24,
    'w': lambda value: value * 60 * 60 * 24 * 7
}


def parse_duration(duration: str) -> datetime:
    """
    Parses a string like '3w' into a datetime 3 weeks from now.

    Also supports strings like 1w2d or 1h25m.

    This function is adapted from a bot called ROWBOAT, written by b1naryth1ef.
    See https://github.com/b1naryth1ef/rowboat/blob/master/rowboat/util/input.py

    :param duration: a string containing the number and a time unit shorthand.
    :return: A datetime representing now + the duration
    """

    if not duration:
        raise ValueError("No duration provided.")

    value = 0
    digits = ''

    for char in duration:

        # Add all numbers to the digits string
        if char.isdigit():
            digits += char
            continue

        # If it's not a number and not one of the letters in UNITS, it must be invalid.
        if char not in UNITS or not digits:
            raise ValueError("Invalid duration")

        # Otherwise, call the corresponding lambda to convert the value, and keep iterating.
        value += UNITS[char](int(digits))
        digits = ''

    return datetime.now(make_timezone("00:00")) + timedelta(seconds=value + 1)


def is_expired(rdb_datetime: datetime) -> bool:
    """
    Takes a rethinkdb datetime (timezone aware) and
    figures out if it has expired yet.

    Always compares with UTC 00:00

    :param rdb_timestamp: A datetime as stored in rethinkdb.
    :return: True if the datetime is in the past.
    """
    return datetime.now(make_timezone("00:00")) > rdb_datetime
