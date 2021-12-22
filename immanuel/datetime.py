"""
    This file is part of immanuel - (C) The Rift Lab
    Author: Robert Davies (robert@theriftlab.com)


    This module provides a simple class for handling location-specific
    dates and times.

    The class essentially wraps pyswisseph's jul_day() function but
    additionally takes into account timezones based on lat/long coordinates
    and does the heavy lifting for you.

"""

from datetime import datetime

import swisseph as swe
from pytz import timezone, utc, exceptions
from timezonefinder import TimezoneFinder

from immanuel import convert


class DateTime:
    """ This class is instatiated with a standard Python datetime object,
    and decimal lat / lon coordinates as floats. is_dst can be True or False
    to clarify ambiguous datetimes (eg. 01:30 when DST ends).

    """

    def __init__(self, dt: datetime, lat: float, lon: float, is_dst = None):
        self._dt = dt
        self._lat = lat
        self._lon = lon
        self._is_dst = is_dst
        self.dst_ambiguous = False
        self.timezone = self._timezone()
        self.offset = self._offset()
        self.jd = None if self.offset is None else self._jd()

    @staticmethod
    def from_jd(jd: float, lat: float, lon: float, is_dst = None):
        utc = swe.jdut1_to_utc(jd)
        seconds_float = utc[5]
        seconds = int(seconds_float)
        microseconds = round((seconds_float - seconds) * 1000)
        dt_utc = utc[:5] + (seconds, microseconds)
        dt = datetime(*dt_utc)
        return DateTime(dt, lat, lon)

    def _timezone(self) -> str:
        """ Returns the timezone's name. """
        return TimezoneFinder().certain_timezone_at(lat=self._lat, lng=self._lon)

    def _offset(self) -> float:
        """ Returns the timezone's offset after DST ambiguity check. """
        tz = timezone(self.timezone)

        try:
            dt_local = tz.localize(self._dt, self._is_dst)
        except exceptions.AmbiguousTimeError:
            self.dst_ambiguous = True
            return None

        dt_utc = utc.localize(self._dt)
        return (dt_utc - dt_local).total_seconds() / 3600

    def _jd(self) -> float:
        """ Returns the Julian date. """
        hour = convert.dms_to_dec(['+', self._dt.hour-self.offset, self._dt.minute, self._dt.second])
        return swe.julday(self._dt.year, self._dt.month, self._dt.day, hour)

    def __str__(self):
        return f'{self._dt.strftime("%c")} {self.timezone}'
