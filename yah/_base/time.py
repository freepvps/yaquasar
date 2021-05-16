import time

import datetime as dt


NANOSECONDS_IN_SECOND = 1000000000
DATE_FMT = '%Y-%m-%d'


def to_nanosec(seconds: float) -> int:
    sec = int(seconds)
    return sec * NANOSECONDS_IN_SECOND + int((seconds - sec) * NANOSECONDS_IN_SECOND)


def unixtime_ns() -> int:
    return time.time_ns()


def to_unixtime(time: dt.datetime) -> int:
    return int((time - dt.datetime(1970, 1, 1)).total_seconds())


def from_unixtime(seconds: int) -> dt.datetime:
    return dt.datetime(1970, 1, 1) + dt.timedelta(seconds=seconds)


def parse_time(s: str) -> dt.time:
    return dt.time.fromisoformat(s)


def parse_datetime(s: str) -> dt.datetime:
    return dt.datetime.fromisoformat(s.rstrip('Z'))


def parse_date(s: str) -> dt.date:
    return dt.datetime.strptime(s, DATE_FMT).date()


def date_str(d: dt.date) -> str:
    return d.strftime(DATE_FMT)


def day_begin(date: dt.date) -> dt.datetime:
    return dt.datetime(date.year, date.month, date.day, 0, 0, 0)


def day_end(date: dt.date) -> dt.datetime:
    return dt.datetime(date.year, date.month, date.day, 23, 59, 59)


def time_seconds(t: dt.time) -> float:
    return (t.hour * 60 + t.minute) * 60 + t.second + t.microsecond / 10**6
