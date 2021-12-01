"""
    This file is part of immanuel - (C) The Rift Lab
    Author: Robert Davies (robert@theriftlab.com)


    This module provides conversions between base-12 and base-10.

    The class performs simple conversions between the base-12 data used
    by astrology (ie. angles, coordinates, and time) and decimal numbers.

"""

import math
from decimal import Decimal


class DuoDec:
    """ This class is instatiated with either a duodecimal list
    or a decimal float, and can be converted between one another.

    """

    def __init__(self, value):
        """ Accepts either a float, a float as a string, a list of ints,
        or a list of ints as strings.
        """
        if isinstance(value, float):
            self.value = value
        elif isinstance(value, list):
            self.value = [value[0]] + [int(v) for v in value[1:]]
        elif isinstance(value, str):
            self.value = float(value)
        else:
            self.value = None

        self.float = self._to_float()
        self.list = self._to_list()

    def _to_float(self):
        """ Returns the decimal conversion of a duodecimal list. """
        if isinstance(self.value, float) or self.value is None:
            return self.value

        values = [abs(v) / 60**k for (k,v) in enumerate(self.value[1:])]
        multiplier = -1 if self.value[0] == '-' else 1
        return sum(values) * multiplier

    def _to_list(self):
        """ Returns the duodecimal conversion of a decimal float
        as a list. """
        if isinstance(self.value, list) or self.value is None:
            return self.value

        value = abs(self.value)
        values = [0, 0, 0, 0]

        for i in range(4):
            values[i] = math.floor(value)
            value = (Decimal(str(value)) - Decimal(str(values[i]))) * 60

        return ['-' if self.value < 0 else '+'] + values