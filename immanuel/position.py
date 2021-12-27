"""
    This file is part of immanuel - (C) The Rift Lab
    Author: Robert Davies (robert@theriftlab.com)


    This module provides data for an individual item's position & speed.

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

    def __init__(self, speed: float):
        self.data({
            const.RETROGRADE: speed < -const.STATION_SPEED,
            const.STATION: abs(speed) <= const.STATION_SPEED,
            const.DIRECT: speed > const.STATION_SPEED,
        })


class Motion(SerializableBoolean):
    """ Stores whether the passed item is slow (below mean daily motion)
    or fast (equal to or above mean daily motion).

    """

    def __init__(self, speed: float, name: str):
        self.data({
            const.SLOW: abs(speed) < const.MEAN_MOTIONS[name],
            const.FAST: abs(speed) >= const.MEAN_MOTIONS[name],
        })


class Dignities(SerializableBoolean):
    """ Stores which of the main essential dignities applies to the
    passed item, if any.

    """
    def __init__(self, lon: float, name: str):
        self._sign = sign(lon)

        self.data({
            const.DOMICILE: self._sign in domicile(name),
            const.EXALTED: self._sign == exalted(name),
            const.DETRIMENT: self._sign == detriment(name),
            const.FALL: self._sign == fall(name),
            const.FACE_RULER: name == face_ruler(lon),
            const.TERM_RULER: name == term_ruler(lon),
            const.TRIPLICITY_RULER: name in triplicity_rulers(self._sign),
        })

        self.score = sum({v for k, v in const.SCORES.items() if self[k]})


def sign(lon: float) -> str:
    """ Returns the zodiac sign the passed longitude belongs to. """
    return const.SIGNS[int(lon / 30)]


def domicile(name: str) -> tuple:
    """ Returns the sign(s) the passed planet is domiciled. """
    return const.ESSENTIAL_DIGNITIES[name][const.DOMICILE]


def exalted(name: str) -> str:
    """ Returns the sign the passed planet is exalted. """
    return const.ESSENTIAL_DIGNITIES[name][const.EXALTED]


def detriment(name: str) -> str:
    """ Returns the sign the passed planet is in detriment. """
    return const.ESSENTIAL_DIGNITIES[name][const.DETRIMENT]


def fall(name: str) -> str:
    """ Returns the sign the passed planet is in fall / exile. """
    return const.ESSENTIAL_DIGNITIES[name][const.FALL]


def face_ruler(lon: float) -> str:
    """ Returns the planetary decan ruler of the pased longitude. """
    return const.FACE_RULERS[sign(lon)][int((lon % 30) // 10)]


def term_ruler(lon: float) -> str:
    """ Returns the planetary term ruler of the pased longitude. """
    sign_lon = int(lon % 30)

    for planet, lon_range in const.TERM_RULERS[sign(lon)].items():
        if lon_range[0] <= sign_lon < lon_range[1]:
            return planet


def triplicity_rulers(sign: str) -> tuple:
    """ Returns the three triplicity rulers for the passed sign. """
    return const.TRIPLICITY_RULERS[sign]


def is_out_of_bounds(dec: float) -> bool:
    """ Returns whether the passed declination is out of bounds. """
    return abs(dec) < const.DECLINATION_BOUNDARY
