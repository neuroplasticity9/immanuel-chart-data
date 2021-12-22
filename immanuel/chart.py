"""
    This file is part of immanuel - (C) The Rift Lab
    Author: Robert Davies (robert@theriftlab.com)


    This module contains the main Chart class for producing chart data.

    Given a localised date/time and lat/lon coordinates, this class
    will gather all relevant data to create a chart, and is
    fully serialisable for JSON output.

"""

from decimal import Decimal
from operator import itemgetter

import swisseph as swe

from immanuel import aspects, const, convert, transits
from immanuel.items import AxisAngle, House, Planet, Point
from immanuel.serializable import Serializable, SerializableDict, SerializableList


class Chart(Serializable):
    def __init__(self, dt, lat, lon, hsys, aspects = None, orbs = None, asteroids = None, fixed_stars = None):
        self._jd = dt.jd
        self._lat = lat
        self._lon = lon
        self._hsys = const.HOUSE_SYSTEMS[hsys if hsys is not None else const.PLACIDUS]
        self._swe_houses_angles = self._get_swe_houses_angles()

        self.houses = self._houses()
        self.angles = self._angles()
        self.planets = self._planets()
        self.points = self._points()
        self.asteroids = {}
        self.fixed_stars = {}
        self.aspects = self._aspects()
        # self._aspects = {}   # TODO: default list
        # self._orbs = {}      # TODO: default list

        # TODO: serializable list

    def _get_swe_houses_angles(self):
        """ This must be called before _houses() and _angles(). """
        return dict(zip(('cusps', 'ascmc', 'cuspsspeed', 'ascmcspeed'), swe.houses_ex2(self._jd, self._lat, self._lon, self._hsys)))

    def _houses(self):
        """ Get the house cusps from _swe_houses_angles. """
        houses = SerializableDict()
        cusps, cuspsspeed = itemgetter('cusps', 'cuspsspeed')(self._swe_houses_angles)

        for i, cusp in enumerate(cusps):
            house_number = i + 1
            size = abs(float((Decimal(str(cusps[i+1 if i < 11 else 0])) - Decimal(str(cusp))) % 360))
            houses[house_number] = House(house_number, cusp, size, cuspsspeed[i])

        return houses

    def _angles(self):
        """ Get the main axis angles from _swe_houses_angles. """
        angles = SerializableDict()
        ascmc, ascmcspeed = itemgetter('ascmc', 'ascmcspeed')(self._swe_houses_angles)

        for name, swe_index in const.ANGLES.items():
            lon = ascmc[swe_index]
            speed = ascmcspeed[swe_index]

            if name in [const.DESC, const.IC]:
                lon = (lon - 180) % 360

            angles[name] = AxisAngle(name, lon, speed)

        return angles

    def _planets(self):
        """ Get the ten main planets. """
        planets = SerializableDict()

        for name, planet in const.PLANETS.items():
            ec_res, ec_flg = swe.calc_ut(self._jd, planet)
            eq_res, eq_flg = swe.calc_ut(self._jd, planet, swe.FLG_EQUATORIAL)
            lon, lat, dist, speed = ec_res[:4]
            dec = eq_res[1]
            house = self._get_house(lon)
            planets[name] = Planet(name, house, lon, lat, dist, speed, dec)

        return planets

    def _points(self):
            # Nodes
            # Syzygy
        # Pars Fortuna
        # Liliths
            # Vertex
        """ Get the main calculated points. """
        points = SerializableDict()

        """ Get the nodes. """
        res, flg = swe.calc_ut(self._jd, const.POINTS[const.NORTH_NODE])
        lon, lat, dist, speed = res[:4]
        house = self._get_house(lon)
        points[const.NORTH_NODE] = Point(const.NORTH_NODE, house, lon, speed)

        lon = (lon - 180) % 360
        house = self._get_house(lon)
        points[const.SOUTH_NODE] = Point(const.SOUTH_NODE, house, lon, speed)

        """ Get the vertex. """
        ascmc, ascmcspeed = itemgetter('ascmc', 'ascmcspeed')(self._swe_houses_angles)
        lon = ascmc[const.POINTS[const.VERTEX]]
        speed = ascmcspeed[const.POINTS[const.VERTEX]]
        house = self._get_house(lon)
        points[const.VERTEX] = Point(const.VERTEX, house, lon, speed)

        """ Get the latest pre-natal full/new moon. """
        distance = self.planets[const.SUN].distance_to(self.planets[const.MOON])
        jd = transits.previous_new_moon(self._jd) if distance > 0 else transits.previous_full_moon(self._jd)
        res, flg = swe.calc_ut(jd, const.PLANETS[const.MOON])
        lon, lat, dist, speed = res[:4]
        house = self._get_house(lon)
        points[const.SYZYGY] = Point(const.SYZYGY, house, lon, speed)

        return points

    def asteroids(self, asteroids):
        return {}

    def fixed_stars(self, fixed_stars):
        return {}

    def _aspects(self):
        """ Calculate all requested aspects between chart items. """
        item_aspects = SerializableDict({v: SerializableList([]) for v in const.PLANETS.keys()})
        aspect_items = self.planets

        for aspecting_name, aspecting_item in aspect_items.items():
            for aspected_name, aspected_item in aspect_items.items():
                if aspecting_name == aspected_name:
                    continue

                aspect = aspects.find(aspecting_item, aspected_item)

                if aspect is not None:
                    item_aspects[aspecting_item.name].append(aspect)

        return item_aspects

    def _get_house(self, lon):
        for house in self.houses.values():
            if house.longitude <= lon < house.longitude + house.size:
                return house.name
        return None
