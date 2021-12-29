"""
    This file is part of immanuel - (C) The Rift Lab
    Author: Robert Davies (robert@theriftlab.com)


    This module provides simple classes for handling angles.

    Use the Angle class for generic angles, and SignAngle for the
    chart items' angles that need to be split into signs.

"""

from __future__ import annotations
from decimal import Decimal

import swisseph as swe

from immanuel import convert
from immanuel.serializable import Serializable


WHOLE = 0
SHORTEST = 1

class AngleBase(Serializable):
    """ Base class for taking care of common conversions between decimal
    angles and human-readable formats. Instances can be compared against
    floats or other instances. The _full member is left up to inheriting
    classes to assign. Although this is not an abstract class, it should
    essentially be treated as one.

    """

    _full = 0

    def __init__(self, angle: float):
        """ Sets members common to all angles. """
        dms = convert.dec_to_dms(angle)
        self.angle = angle
        self.direction, self.degrees, self.minutes, self.seconds = dms

    def diff(self, other: AngleBase, normalise: int = SHORTEST) -> Angle:
        """ Returns the distance between two chart angles. """
        return Angle(swe.difdeg2n(other._full, self._full)) if normalise == SHORTEST else Angle(swe.difdegn(other._full, self._full))

    def __add__(self, other: float | AngleBase) -> float:
        return self._full + (other._full if isinstance(other, AngleBase) else other)

    def __radd__(self, other: float | AngleBase) -> float:
        return (other._full if isinstance(other, AngleBase) else other) + self._full

    def __sub__(self, other: float | AngleBase) -> float:
        return self._full - (other._full if isinstance(other, AngleBase) else other)

    def __rsub__(self, other: float | AngleBase) -> float:
        return (other._full if isinstance(other, AngleBase) else other) - self._full

    def __truediv__(self, other: float | AngleBase) -> float:
        return self._full / (other._full if isinstance(other, AngleBase) else other)

    def __floordiv__(self, other: float | AngleBase) -> int:
        return self._full // (other._full if isinstance(other, AngleBase) else other)

    def __mod__(self, other: float | AngleBase) -> int:
        return self._full % (other._full if isinstance(other, AngleBase) else other)

    def __lt__(self, other: float | AngleBase) -> bool:
        return self._full < (other._full if isinstance(other, AngleBase) else other)

    def __le__(self, other: float | AngleBase) -> bool:
        return self._full <= (other._full if isinstance(other, AngleBase) else other)

    def __eq__(self, other: float | AngleBase) -> bool:
        return self._full == (other._full if isinstance(other, AngleBase) else other)

    def __ne__(self, other: float | AngleBase) -> bool:
        return self._full != (other._full if isinstance(other, AngleBase) else other)

    def __gt__(self, other: float | AngleBase) -> bool:
        return self._full > (other._full if isinstance(other, AngleBase) else other)

    def __ge__(self, other: float | AngleBase) -> bool:
        return self._full >= (other._full if isinstance(other, AngleBase) else other)

    def __abs__(self) -> float:
        return abs(self._full)

    def __int__(self) -> int:
        return int(self.full)

    def __float__(self) -> float:
        return self.full

    def __str__(self) -> str:
        return convert.dec_to_string(self.angle, convert.FORMAT_DMS)


class Angle(AngleBase):
    """ Simple class for handling 0-359° values. This is useful for any
    value that should be in DD:MM:SS format, such as latitudes, longitudes,
    speed, declination, etc.

    """

    def __init__(self, angle: float):
        self._full = angle
        super().__init__(angle)


class SignAngle(AngleBase):
    """ This class converts full ecliptic 0-359° longitudes to
    per-sign 0-29° longitudes. Comparisons are still based on the
    full ecliptic longitude (eg. 5° Taurus is > 20° Aries).

    """

    def __init__(self, angle: float):
        self._full = self.full = angle
        super().__init__(float(Decimal(str(angle)) % 30))
