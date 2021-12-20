"""
    This file is part of immanuel - (C) The Rift Lab
    Author: Robert Davies (robert@theriftlab.com)


    This module provides data for a planet's position & speed.

    These classes provide simple serializable, stringable objects
    for various positional data such as movement, motion, and dignity,
    as well as helper functions.

"""

from abc import ABC

from immanuel import const
from immanuel.serializable import SerializableBoolean


class Movement(SerializableBoolean):
    """ Stores whether the passed item is retrograde, stationed,
    or direct. Stationed can still be in daily motion < 1 second.

    """

    def __init__(self, speed):
        self.data({
            const.RETROGRADE: speed < -const.STATION_SPEED,
            const.STATION: abs(speed) <= const.STATION_SPEED,
            const.DIRECT: speed > const.STATION_SPEED,
        })


class Motion(SerializableBoolean):
    """ Stores whether the passed item is slow (below mean daily motion)
    or fast (equal to or above mean daily motion).

    """

    def __init__(self, speed, name):
        self.data({
            const.SLOW: abs(speed) < const.MEAN_MOTIONS[name],
            const.FAST: abs(speed) >= const.MEAN_MOTIONS[name],
        })


class Dignity(SerializableBoolean):
    """ Stores which of the four main essential dignities applies to the
    passed item, if any.

    """
    def __init__(self, sign, name):
        self.data({
            const.DOMICILE: sign in const.ESSENTIAL_DIGNITIES[name]['domicile'],
            const.EXALTED: sign == const.ESSENTIAL_DIGNITIES[name]['exalted'],
            const.DETRIMENT: sign == const.ESSENTIAL_DIGNITIES[name]['detriment'],
            const.FALL: sign == const.ESSENTIAL_DIGNITIES[name]['fall'],
        })


def sign(lon: float) -> str:
    """ Returns the zodiac sign the passed longitude belongs to. """
    return const.SIGNS[int(lon/30)]


def is_out_of_bounds(dec: float) -> bool:
    """ Returns whether the passed declination is out of bounds. """
    return abs(dec) < const.DECLINATION_BOUNDARY
