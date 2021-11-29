"""
    This file is part of immanuel - (C) The Rift Lab
    Author: Robert Davies (robert@theriftlab.com)


    This module provides a class for lat/lon coordinates.

    Essentially this only serves to ensure any coordinates provided
    are stored in decimal format for internal use.

"""

from immanuel.duodec import DuoDec


class Coords:
    def __init__(self, lat, lon):
        self.lat = self._to_decimal(lat)
        self.lon = self._to_decimal(lon)

    def _to_decimal(self, value):
        if isinstance(value, float):
            return value

        char_signs = {'N': '+', 'S': '-', 'E': '+', 'W': '-'}
        value = value.upper()

        for char in char_signs.keys():
            if char in value:
                return DuoDec(char_signs[char] + value.replace(char, ':')).to_decimal()