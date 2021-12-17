"""
    This file is part of immanuel - (C) The Rift Lab
    Author: Robert Davies (robert@theriftlab.com)


    This module provides simple classes for handling angles.

    Use the Angle class for generic angles, and SignAngle for the
    chart items' angles that need to be split into signs.

"""

from __future__ import annotations
from abc import ABC, abstractmethod
from decimal import Decimal

from immanuel import convert
from immanuel.serializable import Serializable


class BaseAngle(ABC, Serializable):
    """ Base class for taking care of common conversions between decimal
    angles and human-readable formats. Instances can be compared against
    floats or other instances. The _full member is left up to inheriting
    classes to assign.

    """

    _full = 0

    @abstractmethod
    def __init__(self, angle: float):
        """ Sets members common to all angles. """
        dms = convert.dec_to_dms(angle)
        self.angle = angle
        self.direction = dms[0]
        self.degrees = dms[1]
        self.minutes = dms[2]
        self.seconds = dms[3]

    def __add__(self, other: float | BaseAngle) -> float:
        return self._full + (other._full if isinstance(other, BaseAngle) else other)

    def __sub__(self, other: float | BaseAngle) -> float:
        return self._full - (other._full if isinstance(other, BaseAngle) else other)

    def __lt__(self, other: float | BaseAngle) -> bool:
        return self._full < (other._full if isinstance(other, BaseAngle) else other)

    def __le__(self, other: float | BaseAngle) -> bool:
        return self._full <= (other._full if isinstance(other, BaseAngle) else other)

    def __eq__(self, other: float | BaseAngle) -> bool:
        return self._full == (other._full if isinstance(other, BaseAngle) else other)

    def __ne__(self, other: float | BaseAngle) -> bool:
        return self._full != (other._full if isinstance(other, BaseAngle) else other)

    def __gt__(self, other: float | BaseAngle) -> bool:
        return self._full > (other._full if isinstance(other, BaseAngle) else other)

    def __ge__(self, other: float | BaseAngle) -> bool:
        return self._full >= (other._full if isinstance(other, BaseAngle) else other)

    def __abs__(self):
        return abs(self._full)

    def __str__(self):
        return convert.dec_to_string(self.angle, convert.FORMAT_DMS)


class Angle(BaseAngle):
    """ Simple class for handling 0-359° values. This is useful for any
    value that should be in DD:MM:SS format, such as latitudes, longitudes,
    speed, declination, etc.

    """

    def __init__(self, angle: float):
        self._full = angle
        super().__init__(angle)


class SignAngle(BaseAngle):
    """ This class converts full ecliptic 0-359° longitudes to
    per-sign 0-29° longitudes. Comparisons are still based on the
    full ecliptic longitude (eg. 5° Taurus is > 20° Aries).

    """

    def __init__(self, angle: float):
        self._full = self.full = angle
        super().__init__(float(Decimal(str(angle)) % 30))
