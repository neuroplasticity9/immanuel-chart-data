"""
    This file is part of immanuel - (C) The Rift Lab
    Author: Robert Davies (robert@theriftlab.com)


    This module provides conversions between base-12 and base-10.

    This class provides simple conversion between the base-12 data used
    by astrology (ie. angles, coordinates, and time) and decimal numbers.

"""

import math


class DuoDec:
    """ This class is instatiated with either a duodecimal string or a
    decimal float, and can be converted between one another.

    """

    def __init__(self, value):
        self.value = value

    def to_decimal(self):
        """ Returns the decimal conversion of a duodecimal string or list. """
        if isinstance(self.value, float):
            return self.value

        multiplier = -1 if self.value[0] == '-' else 1
        value = self.value.split(':') if isinstance(self.value, str) else self.value[1:]
        values = [abs(int(v)) / 60**(k) for (k,v) in enumerate(value)]
        return sum(values) * multiplier


    def to_duodecimal(self, as_list=False):
        """ Returns the duodecimal conversion of a decimal float. """
        if isinstance(self.value, str):
            return self.value

        values = [0, 0, 0, 0]
        value = abs(self.value)

        for i in range(4):
            values[i] = math.floor(value)
            value = (value - values[i]) * 60

        if as_list:
            return (['-'] if self.value < 0 else ['+']) + values

        return ('-' if self.value < 0 else '+') + ':'.join(str(v) for v in values)