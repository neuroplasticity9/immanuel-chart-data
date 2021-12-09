"""
    This file is part of immanuel - (C) The Rift Lab
    Author: Robert Davies (robert@theriftlab.com)


    This module provides a simple class for handling chart angles.

    Instances of this class can be compared against floats or other
    instances. It takes care of common conversions between decimal
    angles and human-readable formats.

    If the "ecliptic" argument is set to True, the "sign" member assumes
    a 0-360 chart angle (ecliptic longitude) and converts it to a per-sign
    angle - this is of course irrelevant if the original angle passed is not
    an ecliptic longitude.

"""

from __future__ import annotations
from decimal import Decimal

from immanuel import convert


class Angle:
    def __init__(self, angle, ecliptic = True):
        self.full = angle
        self.sign = float(Decimal(str(angle)) % 30) if ecliptic else angle
        self.dict = dict(zip(['direction', 'degrees', 'minutes', 'seconds'], convert.dec_to_dms(self.sign)))
        self.str = convert.dec_to_string(self.sign, convert.FORMAT_DMS)

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