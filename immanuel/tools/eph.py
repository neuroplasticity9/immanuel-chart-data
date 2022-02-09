"""
    This file is part of immanuel - (C) The Rift Lab
    Author: Robert Davies (robert@theriftlab.com)


    This module provides easy access to pyswisseph data.

    Relevant data on the main angles, houses, points and planets are
    available using the module's functions. Behind the scenes the data
    is stored in the ChartData class after being retrieved from the
    ephemeris.

"""

import json
from decimal import Decimal

import swisseph as swe

from immanuel.const import angles, defaults, planets, points


class ChartData:
    angles = {}
    houses = {}
    planets = {}
    points = {}


def angle(jd: float, lat: float, lon: float, hsys: bytes, index: int) -> dict:
    key = _get_key(jd, lat, lon, hsys)

    if key not in ChartData.angles:
        _set_angles_houses(jd, lat, lon, hsys)

    return ChartData.angles[key][index]


def house(jd: float, lat: float, lon: float, hsys: bytes, index: int) -> dict:
    key = _get_key(jd, lat, lon, hsys)

    if key not in ChartData.houses:
        _set_angles_houses(jd, lat, lon, hsys)

    return ChartData.houses[key][index]


def point(jd: float, lat: float, lon: float, hsys: bytes, index: int) -> dict:
    key = _get_key(jd, lat, lon, hsys)

    if key not in ChartData.points:
        if index == points.VERTEX:
            _set_angles_houses(jd, lat, lon, hsys)
            return ChartData.points[key][index]

        ChartData.points[key] = {}

    if index not in ChartData.points[key]:
        calculated = index in (points.SOUTH_NODE, points.TRUE_SOUTH_NODE)
        swe_index = index if not calculated else index - defaults.CALCULATED_OFFSET
        p = planet(jd, swe_index)
        ChartData.points[key][index] = {
            'lon': p['lon'] if not calculated else swe.degnorm(Decimal(str(p['lon'])) - 180),
            'speed': p['speed'],
        }

    return ChartData.points[key][index]


def planet(jd: float, index: int) -> dict:
    key = _get_key(jd, index)

    if key not in ChartData.planets:
        ec_res = swe.calc_ut(jd, index)[0]
        eq_res = swe.calc_ut(jd, index, swe.FLG_EQUATORIAL)[0]
        ChartData.planets[key] = {
            'lon': ec_res[0],
            'lat': ec_res[1],
            'dist': ec_res[2],
            'speed': ec_res[3],
            'dec': eq_res[1],
        }

    return ChartData.planets[key]


def _set_angles_houses(jd: float, lat: float, lon: float, hsys: bytes) -> None:
    """ Since angles, houses and certain calculated points are all available
    from the same function call, Immanuel will store them all at the same
    time in this setup function. """
    cusps, ascmc, cuspsspeed, ascmcspeed = swe.houses_ex2(jd, lat, lon, hsys)
    key = _get_key(jd, lat, lon, hsys)
    ChartData.angles[key] = {}
    ChartData.houses[key] = {}
    ChartData.points[key] = {}

    # Angles
    for i, lon in enumerate(ascmc):
        ChartData.angles[key][i] = {
            'lon': lon,
            'speed': ascmcspeed[i],
        }

        if i in (angles.ASC, angles.MC):
            ChartData.angles[key][i + defaults.CALCULATED_OFFSET] = {
                'lon': swe.degnorm(Decimal(str(lon)) - 180),
                'speed': ascmcspeed[i],
            }

    # Houses
    for i, lon in enumerate(cusps):
        ChartData.houses[key][i+1] = {
            'lon': lon,
            'speed': cuspsspeed[i],
        }

    # Points (currently only vertex)
    ChartData.points[key][points.VERTEX] = {
        'lon': ascmc[points.VERTEX],
        'speed': ascmcspeed[points.VERTEX],
    }


def _get_key(*args) -> str:
    return json.dumps([str(v) for v in args], sort_keys=True)
