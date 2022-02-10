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
from immanuel.tools import find


class ChartData:
    """ This class serves as a simple static data store. """
    angles = {}
    houses = {}
    planets = {}
    points = {}
    diurnal = {}


def angle(jd: float, lat: float, lon: float, hsys: bytes, index: int) -> dict:
    """ Returns one of the four main chart angles & their speed. """
    key = _get_key(jd, lat, lon, hsys)

    if key not in ChartData.angles:
        _set_angles_houses(jd, lat, lon, hsys)

    return ChartData.angles[key][index]


def house(jd: float, lat: float, lon: float, hsys: bytes, index: int) -> dict:
    """ Returns a house cusp & cusp speed. """
    key = _get_key(jd, lat, lon, hsys)

    if key not in ChartData.houses:
        _set_angles_houses(jd, lat, lon, hsys)

    return ChartData.houses[key][index]


def point(jd: float, index: int, **kwargs) -> dict:
    """ Returns a calculated point by Julian date. Since the Vertex is
    returned with the houses / ascmc by pyswisseph, this has its own
    special case. """
    lat = kwargs.get('lat', None)
    lon = kwargs.get('lon', None)
    hsys = kwargs.get('hsys', None)
    key = _get_key(jd, lat, lon, hsys)

    if key not in ChartData.points:
        ChartData.points[key] = {}

    if index not in ChartData.points[key]:
        if index == points.VERTEX:
            # Get Vertex from house/ascmc calculation
            _set_angles_houses(jd, lat, lon, hsys)
        elif index == points.SYZYGY:
            # Calculate prenatal full/new moon
            sun = planet(jd, planets.SUN)
            moon = planet(jd, planets.MOON)
            distance = swe.difdeg2n(moon['lon'], sun['lon'])
            syzygy_jd = find.previous_new_moon(jd) if distance > 0 else find.previous_full_moon(jd)
            syzygy_moon = planet(syzygy_jd, planets.MOON)

            ChartData.points[key][points.SYZYGY] = {
                'lon': syzygy_moon['lon'],
                'speed': syzygy_moon['speed'],
            }
        elif index == points.PARS_FORTUNA:
            # Calculate part of furtune
            asc = angle(jd, lat, lon, hsys, angles.ASC)
            moon = planet(jd, planets.MOON)
            sun = planet(jd, planets.SUN)
            formula = (asc['lon'] + moon['lon'] - sun['lon']) if is_daytime(jd, lat, lon, hsys) else (asc['lon'] + sun['lon'] - moon['lon'])

            ChartData.points[key][points.PARS_FORTUNA] = {
                'lon': swe.degnorm(formula),
                'speed': 0,
            }
        else:
            # Get other available points
            calculated = index in (points.SOUTH_NODE, points.TRUE_SOUTH_NODE)
            swe_index = index if not calculated else index - defaults.CALCULATED_OFFSET
            p = planet(jd, swe_index)

            ChartData.points[key][index] = {
                'lon': p['lon'] if not calculated else swe.degnorm(Decimal(str(p['lon'])) - 180),
                'speed': p['speed'],
            }

    return ChartData.points[key][index]


def planet(jd: float, index: int) -> dict:
    """ Returns a pyswisseph object by Julian date. This can be used to
    find more than planets only since calc_ut() is used for many other
    objects too. """
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


def is_daytime(jd: float, lat: float, lon: float, hsys: bytes) -> bool:
    """ Returns whether it is daytime at the passed Julian date
    and position. """
    key = _get_key(jd, lat, lon, hsys)

    if key not in ChartData.diurnal:
        _set_angles_houses(jd, lat, lon, hsys)

    return ChartData.diurnal[key]


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

    # Whether the Sun is above the horizon
    sun = planet(jd, planets.SUN)
    asc = ChartData.angles[key][angles.ASC]
    ChartData.diurnal[key] = swe.difdeg2n(sun['lon'], asc['lon']) < 0


def _get_key(*args) -> str:
    """ Returns a simple unique key based on date/location arguments. """
    return json.dumps([str(v) for v in args], sort_keys=True)
