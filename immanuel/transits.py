"""
    This file is part of immanuel - (C) The Rift Lab
    Author: Robert Davies (robert@theriftlab.com)


    This module calculates past and future transits relative
    to a passed Julian day.

    previous() and next() take two chart items (such as planets),
    a Julian day, and an aspect. The functions will then return
    the last/next Julian day before/after the passed one where the
    requested aspect took place. This calculation tends to be expensive,
    especially for slow planets.

    The previous new and full moon functions are designed to fast-forward
    to the closest approximation of each aspect before handing off to
    _find()'s loop. Since the Sun and Moon have relatively stable daily
    motions and never retrograde, these are the only two bodies predictable
    enough to safely perform this with.

"""

import math

import swisseph as swe

from immanuel import const
from immanuel.items import Item


PREVIOUS = 0
NEXT = 1

def previous(first: str, second: str, jd: float, aspect: str) -> float:
    """ Returns the Julian day of the requested transit previous
    to the passed Julian day. """
    return _find(first, second, aspect, jd, PREVIOUS)


def next(first: str, second: str, jd: float, aspect: str) -> float:
    """ Returns the Julian day of the requested transit after
    the passed Julian day. """
    return _find(first, second, aspect, jd, NEXT)


def _find(first: str, second: str, aspect: str, jd: float, direction: int) -> float:
    """ Polls the ephemeris with minute-by-minute Julian dates until a close
    aspect match is found - accurate to within a few seconds of a degree. """
    step = (1 if direction == NEXT else -1) / 1440

    while True:
        first_lon = swe.calc_ut(jd, const.CHART_ITEMS[first])[0][0]
        second_lon = swe.calc_ut(jd, const.CHART_ITEMS[second])[0][0]
        distance = abs(swe.difdeg2n(first_lon, second_lon))

        if round(distance, 2) == const.ASPECTS[aspect]:
            return jd

        jd += step


def previous_new_moon(jd: float):
    """ Fast rewind to approximate conjunction. """
    sun_lon = swe.calc_ut(jd, const.PLANETS[const.SUN])[0][0]
    moon_lon = swe.calc_ut(jd, const.PLANETS[const.MOON])[0][0]
    distance = swe.difdegn(moon_lon, sun_lon)
    jd -= math.floor(distance) / math.floor(const.MEAN_MOTIONS[const.MOON])
    return _find(const.SUN, const.MOON, const.CONJUNCTION, jd, PREVIOUS)


def previous_full_moon(jd: float):
    """ Fast rewind to approximate opposition. """
    sun_lon = swe.calc_ut(jd, const.PLANETS[const.SUN])[0][0]
    moon_lon = swe.calc_ut(jd, const.PLANETS[const.MOON])[0][0]
    distance = swe.difdegn(moon_lon, sun_lon)
    distance += 180 if distance < 180 else -180
    jd -= math.floor(distance) / math.floor(const.MEAN_MOTIONS[const.MOON])
    return _find(const.SUN, const.MOON, const.OPPOSITION, jd, PREVIOUS)
