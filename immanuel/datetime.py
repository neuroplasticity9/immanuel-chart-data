"""
    This file is part of immanuel - (C) The Rift Lab
    Author: Robert Davies (robert@theriftlab.com)


    This module provides a simple class for handling location-specific
    dates and times.

    The class essentially wraps pyswisseph's jul_day() function but
    additionally takes into account timezones based on lat/long coordinates
    and does the heavy lifting for you.

"""

import swisseph
from datetime import datetime
from pytz import timezone, utc
from timezonefinder import TimezoneFinder
from immanuel.duodec import DuoDec


class DateTime:
    """ This class is instatiated with a datetime string such as is accepted
    by the standard Python datetime.fromisoformat() method, and coordinates.

    """

    def __init__(self, dt, coords):
        self.dt = datetime.fromisoformat(dt)
        self.coords = coords
        self.timezone = self._timezone()
        self.offset = self._offset()
        self.jd = self._jd()

    def _timezone(self):
        """ Returns the timezone's name. """
        return TimezoneFinder().certain_timezone_at(lat=self.coords.lat, lng=self.coords.lon)

    def _offset(self):
        """ Returns the timezone's offset. """
        tz = timezone(self.timezone)
        dt_local = tz.localize(self.dt)
        dt_utc = utc.localize(self.dt)
        return int((dt_utc - dt_local).total_seconds() / 3600)

    def _jd(self):
        """ Returns the Julian date. """
        hour = DuoDec(['+', self.dt.hour-self.offset, self.dt.minute, self.dt.second]).float
        return swisseph.julday(self.dt.year, self.dt.month, self.dt.day, hour)