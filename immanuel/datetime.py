"""
    This file is part of immanuel - (C) The Rift Lab
    Author: Robert Davies (robert@theriftlab.com)


    This module provides a simple class for handling location-specific
    dates and times.

    The class essentially does the job of pyswisseph's date_conversion()
    function but additionally takes into account timezones based on
    lat/long coordinates and does the heavy lifting for you.

"""

from datetime import datetime
from jdcal import gcal2jd
from pytz import timezone, utc
from timezonefinder import TimezoneFinder


class DateTime:
    """ This class is instatiated with a datetime string such as is accepted
    by the standard Python datetime.fromisoformat() method, and coordinates.

    """

    def __init__(self, dt, coords):
        self.dt = datetime.fromisoformat(dt)
        self.coords = coords
        self.timezone = self._timezone()
        self.offset = self._offset()
        self.jdn = self._jdn()

    def _timezone(self):
        return TimezoneFinder().certain_timezone_at(lat=self.coords.lat, lng=self.coords.lon)

    def _offset(self):
        """ Returns the timezone's offset. """
        tz = timezone(self.timezone)
        dt_local = tz.localize(self.dt)
        dt_utc = utc.localize(self.dt)
        return int((dt_utc - dt_local).total_seconds() / 3600)

    def _jdn(self):
        """ Returns the Julian date. """
        date = sum(gcal2jd(self.dt.year, self.dt.month, self.dt.day))
        time = (self.dt.hour-self.offset)/24 + self.dt.minute/1440 + self.dt.second/86400
        return date + time