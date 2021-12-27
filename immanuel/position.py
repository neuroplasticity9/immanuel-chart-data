"""
    This file is part of immanuel - (C) The Rift Lab
    Author: Robert Davies (robert@theriftlab.com)


    This module provides data for an individual item's position & speed.

    These classes provide simple serializable, stringable objects
    for various positional data such as movement, motion, and dignities,
    as well as helper functions.

"""

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
        self.data({
            const.DOMICILE: is_domicile(name, lon),
            const.EXALTED: is_exalted(name, lon),
            const.DETRIMENT: is_in_detriment(name, lon),
            const.FALL: is_in_fall(name, lon),
            const.TRIPLICITY_RULER: is_triplicity_ruler(name, lon),
            const.FACE_RULER: is_face_ruler(name, lon),
            const.TERM_RULER: is_term_ruler(name, lon),
        })

        self.score = sum({v for k, v in const.DIGNITY_SCORES.items() if self[k]})


def sign(lon: float) -> str:
    """ Returns the zodiac sign the passed longitude belongs to. """
    return const.SIGNS[int(lon / 30)]


def is_domicile(name: str, lon: float) -> bool:
    """ Whether the passed planet is domiciled in the passed longitude. """
    _sign = sign(lon)
    dignity = const.ESSENTIAL_DIGNITIES[_sign][const.DOMICILE]
    return (name in dignity) if isinstance(dignity, tuple) else (name == dignity)


def is_exalted(name: str, lon: float) -> bool:
    """ Whether the passed planet is exalted in the passed longitude. """
    _sign = sign(lon)
    dignity = const.ESSENTIAL_DIGNITIES[_sign][const.EXALTED]
    return (name in dignity) if isinstance(dignity, tuple) else (name == dignity)


def is_in_detriment(name: str, lon: float) -> bool:
    """ Whether the passed planet is in detriment in the passed longitude. """
    _sign = sign(lon)
    dignity = const.ESSENTIAL_DIGNITIES[_sign][const.DETRIMENT]
    return (name in dignity) if isinstance(dignity, tuple) else (name == dignity)


def is_in_fall(name: str, lon: float) -> bool:
    """ Whether the passed planet is in fall in the passed longitude. """
    _sign = sign(lon)
    dignity = const.ESSENTIAL_DIGNITIES[_sign][const.FALL]
    return (name in dignity) if isinstance(dignity, tuple) else (name == dignity)


def is_triplicity_ruler(name: str, lon: float) -> bool:
    """ Whether the passed planet is a triplicity ruler
    in the passed longitude. """
    _sign = sign(lon)
    return name in const.ESSENTIAL_DIGNITIES[_sign][const.TRIPLICITY_RULER]


def is_face_ruler(name: str, lon: float) -> bool:
    """ Whether the passed planet is the decan ruler
    in the passed longitude. """
    _sign = sign(lon)
    return name in const.ESSENTIAL_DIGNITIES[_sign][const.FACE_RULER][int((lon % 30) // 10)]


def is_term_ruler(name: str, lon: float) -> bool:
    """ Whether the passed planet is the term ruler
    in the passed longitude. """
    _sign = sign(lon)
    sign_lon = int(lon % 30)

    for planet, lon_range in const.ESSENTIAL_DIGNITIES[_sign][const.TERM_RULER].items():
        if name == planet and lon_range[0] <= sign_lon < lon_range[1]:
            return True

    return False


def is_out_of_bounds(dec: float) -> bool:
    """ Returns whether the passed declination is out of bounds. """
    return abs(dec) < const.DECLINATION_BOUNDARY
