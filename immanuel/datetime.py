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
        self.dt = dt
        self.lat = lat
        self.lon = lon
        self.is_dst = is_dst
        self.dst_ambiguous = False
        self.timezone = self._timezone()
        self.offset = self._offset()
        self.jd = None if self.offset is None else self._jd()

    def _timezone(self):
        """ Returns the timezone's name. """
        return TimezoneFinder().certain_timezone_at(lat=self.lat, lng=self.lon)

    def _offset(self):
        """ Returns the timezone's offset after DST ambiguity check. """
        tz = timezone(self.timezone)

        try:
            dt_local = tz.localize(self.dt, self.is_dst)
        except exceptions.AmbiguousTimeError:
            self.dst_ambiguous = True
            return None

        dt_utc = utc.localize(self.dt)
        return (dt_utc - dt_local).total_seconds() / 3600

    def _jd(self):
        """ Returns the Julian date. """
        hour = convert.dms_to_dec(['+', self.dt.hour-self.offset, self.dt.minute, self.dt.second])
        return swe.julday(self.dt.year, self.dt.month, self.dt.day, hour)
