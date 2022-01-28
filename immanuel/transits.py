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

    The previous/next new and full moon functions are designed to
    fast-rewind and fast-forward to a close approximation of each aspect
    before handing off to _find()'s loop. Since the Sun and Moon have
    relatively stable daily motions and never retrograde, these are the only
    two bodies predictable enough to safely perform this with.

"""

import math

import swisseph as swe

from immanuel import const
from immanuel.items import Item


PREVIOUS = 0
NEXT = 1


def previous(first: str, second: str, aspect: str, jd: float) -> float:
    """ Returns the Julian day of the requested transit previous
    to the passed Julian day. """
    return _find(first, second, aspect, jd, PREVIOUS)


def next(first: str, second: str, aspect: str, jd: float) -> float:
    """ Returns the Julian day of the requested transit after
    the passed Julian day. """
    return _find(first, second, aspect, jd, NEXT)


def previous_new_moon(jd: float) -> float:
    """ Fast rewind to approximate conjunction. """
    sun_lon = swe.calc_ut(jd, const.PLANETS[const.SUN])[0][0]
    moon_lon = swe.calc_ut(jd, const.PLANETS[const.MOON])[0][0]
    distance = swe.difdegn(moon_lon, sun_lon)
    jd -= math.floor(distance) / math.ceil(const.MEAN_MOTIONS[const.MOON])
    return previous(const.SUN, const.MOON, const.CONJUNCTION, jd)


def previous_full_moon(jd: float) -> float:
    """ Fast rewind to approximate opposition. """
    sun_lon = swe.calc_ut(jd, const.PLANETS[const.SUN])[0][0]
    moon_lon = swe.calc_ut(jd, const.PLANETS[const.MOON])[0][0]
    distance = swe.difdeg2n(moon_lon, sun_lon) + 180
    jd -= math.floor(distance) / math.ceil(const.MEAN_MOTIONS[const.MOON])
    return previous(const.SUN, const.MOON, const.OPPOSITION, jd)


def next_new_moon(jd: float) -> float:
    """ Fast forward to approximate conjunction. """
    sun_lon = swe.calc_ut(jd, const.PLANETS[const.SUN])[0][0]
    moon_lon = swe.calc_ut(jd, const.PLANETS[const.MOON])[0][0]
    distance = swe.difdegn(sun_lon, moon_lon)
    jd += math.floor(distance) / math.ceil(const.MEAN_MOTIONS[const.MOON])
    return next(const.SUN, const.MOON, const.CONJUNCTION, jd)


def next_full_moon(jd: float) -> float:
    """ Fast forward to approximate opposition. """
    sun_lon = swe.calc_ut(jd, const.PLANETS[const.SUN])[0][0]
    moon_lon = swe.calc_ut(jd, const.PLANETS[const.MOON])[0][0]
    distance = swe.difdeg2n(sun_lon, moon_lon) + 180
    jd += math.floor(distance) / math.ceil(const.MEAN_MOTIONS[const.MOON])
    return next(const.SUN, const.MOON, const.OPPOSITION, jd)


def _find(first: str, second: str, aspect: str, jd: float, direction: int) -> float:
    """ Returns the Julian date of the previous/next requested aspect.
    Accurate to within one second of a degree. """
    while True:
        first_lon = swe.calc_ut(jd, const.CHART_ITEMS[first])[0][0]
        second_lon = swe.calc_ut(jd, const.CHART_ITEMS[second])[0][0]
        distance = abs(swe.difdeg2n(first_lon, second_lon))
        diff = abs(const.ASPECTS[aspect] - distance)

        if diff <= const.MAX_ERROR:
            return jd

        jd += (1 if direction == NEXT else -1) / max(180 / diff, 24)
