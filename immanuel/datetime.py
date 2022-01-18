"""
    This file is part of immanuel - (C) The Rift Lab
    Author: Robert Davies (robert@theriftlab.com)


    This module provides a simple class and helper functions for converting
    between location-specific Gregorian dates and times, and universal
    Julian dates.

    The class and functions essentially wrap pyswisseph's jul_day() and
    jdut1_to_utc() functions but take into account timezones based on
    lat/long coordinates and do the heavy lifting for you.

"""

from datetime import datetime

import swisseph as swe
from pytz import exceptions, timezone, UTC
from timezonefinder import TimezoneFinder

from immanuel import convert


class DateTime:
    """ This class is instatiated with either a standard Python datetime
    object or a Julian day as a float, and decimal lat / lon coordinates
    as floats. is_dst can be True or False to clarify ambiguous datetimes
    (eg. 01:30 when DST ends).

    """

    def __init__(self, dt_jd: datetime | float, lat: float, lon: float, is_dst: bool = None):
        self.datetime = None
        self.timezone = TimezoneFinder().certain_timezone_at(lat=lat, lng=lon)
        self.dst_ambiguous = None
        self.jd = None

        if (isinstance(dt_jd, datetime)):
            self._dt_instance(dt_jd, is_dst)
        else:
            self._jd_instance(dt_jd)

    def _dt_instance(self, dt: datetime, is_dst: bool):
        """ Accept a datetime object, localise it, and calculate the
        universal Julian day. """
        try:
            self.datetime = timezone(self.timezone).localize(dt, is_dst)
        except exceptions.AmbiguousTimeError:
            self.datetime = None

        self.jd = datetime_to_jd(self.datetime) if self.datetime is not None else None
        self.dst_ambiguous = self.datetime is None

    def _jd_instance(self, jd: float):
        """ Accept a universal Julian day and generate a localised
        datetime object. """
        self.jd = jd
        self.datetime = jd_to_datetime(jd).astimezone(timezone(self.timezone))
        self.dst_ambiguous = False

    def isoformat(self) -> str:
        """ Returns the underlying datetime object's ISO format. """
        return self.datetime.isoformat()

    def __str__(self) -> str:
        """ Returns the full date with timezone string. """
        return f'{self.datetime.strftime("%a %d %b %Y %H:%M:%S")} {self.timezone}'


def datetime_to_jd(dt: datetime) -> float:
    """ Convert localised datetime into universal Julian day. """
    dt = dt.astimezone(UTC)
    hour = convert.dms_to_dec(['+', dt.hour, dt.minute, dt.second])
    return swe.julday(dt.year, dt.month, dt.day, hour)


def jd_to_datetime(jd: float) -> datetime:
    """ Convert Julian day into UTC datetime object. """
    swe_utc = swe.jdut1_to_utc(jd)
    seconds_float = swe_utc[5]
    seconds = int(seconds_float)
    microseconds = round((seconds_float - seconds) * 1000)
    utc = swe_utc[:5] + (seconds, microseconds)
    return datetime(*utc, tzinfo=UTC)
