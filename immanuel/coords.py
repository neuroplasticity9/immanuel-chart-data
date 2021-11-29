"""
    This file is part of immanuel - (C) The Rift Lab
    Author: Robert Davies (robert@theriftlab.com)


    This module provides a class for lat/lon coordinates.

    Essentially this only serves to ensure any coordinates provided
    are stored in decimal format for internal use.

"""

from immanuel.duodec import DuoDec


class Coords:
    """ This class is instatiated with either a string or a
    decimal float. Strings will be converted to decimal.

    """

    def __init__(self, lat, lon):
        self.lat = self._to_decimal(lat)
        self.lon = self._to_decimal(lon)

    def _to_decimal(self, value):
        """ Ensures the passed value is in decimal format. """
        if isinstance(value, float):
            return value
        elif isinstance(value, str) and '.' in value:
            return float(value)

        direction = next(filter(str.isalpha, value))
        dd_list = ['-' if direction.upper() in 'SW' else '+'] + value.split(direction)
        return DuoDec(dd_list).to_decimal()