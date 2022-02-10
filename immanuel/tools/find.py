"""
    This file is part of immanuel - (C) The Rift Lab
    Author: Robert Davies (robert@theriftlab.com)


    This module calculates past and future transits relative
    to a passed Julian day.

    previous() and next() take two chart objects (such as planets),
    a Julian day, and an aspect. The functions will then find & return
    the last/next Julian day before/after the passed one where the
    requested aspect took place. This calculation can be expensive for
    slow planets.

    The previous/next new and full moon functions are designed to
    fast-rewind and fast-forward to a close approximation of each aspect
    before handing off to _find()'s loop. Since the Sun and Moon have
    relatively stable daily motions and never retrograde, these are the only
    two bodies predictable enough to safely perform this with.

"""

import math

import swisseph as swe

from immanuel.const import aspects, defaults, planets
from immanuel.tools import convert, eph
from immanuel.tools.dates import DateTime


PREVIOUS = 0
NEXT = 1


def previous(first: int, second: int, aspect: float, jd: float) -> float:
    """ Returns the Julian day of the requested transit previous
    to the passed Julian day. """
    return _find(first, second, aspect, jd, PREVIOUS)


def next(first: int, second: int, aspect: float, jd: float) -> float:
    """ Returns the Julian day of the requested transit after
    the passed Julian day. """
    return _find(first, second, aspect, jd, NEXT)


def previous_new_moon(jd: float) -> float:
    """ Fast rewind to approximate conjunction. """
    sun = eph.planet(jd, planets.SUN)
    moon = eph.planet(jd, planets.MOON)
    distance = swe.difdegn(moon['lon'], sun['lon'])
    jd -= math.floor(distance) / math.ceil(planets.MEAN_MOTIONS[planets.MOON])
    return previous(planets.SUN, planets.MOON, aspects.CONJUNCTION, jd)


def previous_full_moon(jd: float) -> float:
    """ Fast rewind to approximate opposition. """
    sun = eph.planet(jd, planets.SUN)
    moon = eph.planet(jd, planets.MOON)
    distance = swe.difdeg2n(moon['lon'], sun['lon']) + 180
    jd -= math.floor(distance) / math.ceil(planets.MEAN_MOTIONS[planets.MOON])
    return previous(planets.SUN, planets.MOON, aspects.OPPOSITION, jd)


def next_new_moon(jd: float) -> float:
    """ Fast forward to approximate conjunction. """
    sun = eph.planet(jd, planets.SUN)
    moon = eph.planet(jd, planets.MOON)
    distance = swe.difdegn(sun['lon'], moon['lon'])
    jd += math.floor(distance) / math.ceil(planets.MEAN_MOTIONS[planets.MOON])
    return next(planets.SUN, planets.MOON, aspects.CONJUNCTION, jd)


def next_full_moon(jd: float) -> float:
    """ Fast forward to approximate opposition. """
    sun = eph.planet(jd, planets.SUN)
    moon = eph.planet(jd, planets.MOON)
    distance = swe.difdegn(sun['lon'], moon['lon']) + 180
    jd += math.floor(distance) / math.ceil(planets.MEAN_MOTIONS[planets.MOON])
    return next(planets.SUN, planets.MOON, aspects.OPPOSITION, jd)


def solar_return(dt: DateTime, year: int, lat: float = None, lon: float = None) -> float:
    """ Returns a DateTime object of the given year's solar return. """
    year_diff = year - dt.datetime.year
    sr_jd = dt.jd + year_diff * defaults.YEAR_DAYS
    natal_sun = eph.planet(dt.jd, planets.SUN)

    while True:
        sr_sun = eph.planet(sr_jd, planets.SUN)
        distance = swe.difdeg2n(natal_sun['lon'], sr_sun['lon'])
        if abs(distance) <= defaults.MAX_ERROR:
            break
        sr_jd += distance / sr_sun['speed']

    lat, lon = (convert.string_to_dec(v) for v in (lat, lon)) if lat and lon else (dt.lat, dt.lon)
    return DateTime(sr_jd, lat, lon)


def _find(first: int, second: int, aspect: float, jd: float, direction: int) -> float:
    """ Returns the Julian date of the previous/next requested aspect.
    Accurate to within one second of a degree. """
    while True:
        first_obj = eph.planet(jd, first)
        second_obj = eph.planet(jd, second)
        distance = abs(swe.difdeg2n(first_obj['lon'], second_obj['lon']))
        diff = abs(aspect - distance)

        if diff <= defaults.MAX_ERROR:
            return jd

        jd += (1 if direction == NEXT else -1) / max(180 / diff, 24)
