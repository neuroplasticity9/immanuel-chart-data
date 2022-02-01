"""
    This file is part of immanuel - (C) The Rift Lab
    Author: Robert Davies (robert@theriftlab.com)


    This module provides

    TODO

"""

from immanuel import chart, const
from immanuel.serializable import SerializableBoolean


def is_domicile(name: str, lon: float) -> bool:
    """ Whether the passed planet is domiciled in the passed longitude. """
    return name in const.ESSENTIAL_DIGNITIES[chart.sign(lon)][const.DOMICILE]


def is_exalted(name: str, lon: float) -> bool:
    """ Whether the passed planet is exalted in the passed longitude. """
    return name in const.ESSENTIAL_DIGNITIES[chart.sign(lon)][const.EXALTED]


def is_in_detriment(name: str, lon: float) -> bool:
    """ Whether the passed planet is in detriment in the passed longitude. """
    return name in const.ESSENTIAL_DIGNITIES[chart.sign(lon)][const.DETRIMENT]


def is_in_fall(name: str, lon: float) -> bool:
    """ Whether the passed planet is in fall in the passed longitude. """
    return name in const.ESSENTIAL_DIGNITIES[chart.sign(lon)][const.FALL]


def is_triplicity_ruler(name: str, lon: float) -> bool:
    """ Whether the passed planet is a triplicity ruler
    in the passed longitude. """
    return name in const.ESSENTIAL_DIGNITIES[chart.sign(lon)][const.TRIPLICITY_RULER]


def is_term_ruler(name: str, lon: float) -> bool:
    """ Whether the passed planet is the term ruler
    in the passed longitude. """
    sign_lon = int(lon % 30)

    for planet, lon_range in const.ESSENTIAL_DIGNITIES[chart.sign(lon)][const.TERM_RULER].items():
        if name == planet and lon_range[0] <= sign_lon < lon_range[1]:
            return True

    return False


def is_face_ruler(name: str, lon: float) -> bool:
    """ Whether the passed planet is the decan ruler
    in the passed longitude. """
    return name in const.ESSENTIAL_DIGNITIES[chart.sign(lon)][const.FACE_RULER][int((lon % 30) // 10)]