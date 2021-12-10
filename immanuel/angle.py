"""
    This file is part of immanuel - (C) The Rift Lab
    Author: Robert Davies (robert@theriftlab.com)


    This module provides simple classes for handling angles.

    Use the Angle class for generic angles, and ChartAngle for ecliptic
    chart angles that need to be split into signs.

"""

from __future__ import annotations
from decimal import Decimal

from immanuel import convert


class Angle:
    """ Instances of this class can be compared against floats or other
    instances. It takes care of common conversions between decimal
    angles and human-readable formats.

    """

    def __init__(self, angle):
        self.angle = self.full = angle
        self.dict = dict(zip(['direction', 'degrees', 'minutes', 'seconds'], convert.dec_to_dms(self.angle)))
        self.str = convert.dec_to_string(self.angle, convert.FORMAT_DMS)

    def __add__(self, other: float | Angle) -> float:
        return self.full + (other.full if isinstance(other, Angle) else other)

    def __sub__(self, other: float | Angle) -> float:
        return self.full - (other.full if isinstance(other, Angle) else other)

    def __lt__(self, other: float | Angle) -> bool:
        return self.full < (other.full if isinstance(other, Angle) else other)

    def __le__(self, other: float | Angle) -> bool:
        return self.full <= (other.full if isinstance(other, Angle) else other)

    def __eq__(self, other: float | Angle) -> bool:
        return self.full == (other.full if isinstance(other, Angle) else other)

    def __ne__(self, other: float | Angle) -> bool:
        return self.full != (other.full if isinstance(other, Angle) else other)

    def __gt__(self, other: float | Angle) -> bool:
        return self.full > (other.full if isinstance(other, Angle) else other)

    def __ge__(self, other: float | Angle) -> bool:
        return self.full >= (other.full if isinstance(other, Angle) else other)

    def __str__(self):
        return self.str


class ChartAngle(Angle):
    """ This class inherits converts full ecliptic 0-359° longitudes to
    per-sign 0-29° longitudes. Comparisons are still based on the full
    ecliptic longitude (eg. 5° Taurus is > 20° Aries).

    """

    def __init__(self, angle):
        super().__init__(float(Decimal(str(angle)) % 30))
        self.full = angle
