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
from immanuel.serializable import Serializable, SerializableBoolean, SerializableDict, SerializableList


class Chart(Serializable):
    def __init__(self, dt, lat, lon, hsys, aspects = None, orbs = None, asteroids = None, fixed_stars = None):
        self._jd = dt.jd
        self._lat = lat
        self._lon = lon
        self._hsys = const.HOUSE_SYSTEMS[hsys if hsys is not None else const.PLACIDUS]
        self._swe_houses_angles = self._get_swe_houses_angles()

        self.type = self._type()
        self.houses = self._houses()
        self.angles = self._angles()
        self.planets = self._planets()
        self.points = self._points()
        self.asteroids = self._asteroids()
        self.fixed_stars = self._fixed_stars()
        self.aspects = self._aspects()
        # self._aspects = {}   # TODO: default list
        # self._orbs = {}      # TODO: default list

    def _get_swe_houses_angles(self):
        """ This must be called before _houses() and _angles(). """
        return dict(zip(('cusps', 'ascmc', 'cuspsspeed', 'ascmcspeed'), swe.houses_ex2(self._jd, self._lat, self._lon, self._hsys)))

    def _type(self):
        """ Determine whether this is a day or a night chart. """
        sun = swe.calc_ut(self._jd, const.PLANETS[const.SUN])[0][0]
        asc = self._swe_houses_angles['ascmc'][const.ANGLES[const.ASC]]
        distance = swe.difdeg2n(sun, asc)

        return SerializableBoolean({
            const.DIURNAL: distance < 0,
            const.NOCTURNAL: distance >= 0,
        })

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
                lon = swe.degnorm(Decimal(str(lon)) - 180)

            angles[name] = AxisAngle(name, lon, speed)

        return angles

    def _planets(self):
        """ Get the ten main planets. """
        planets = SerializableDict()

        for name, planet in const.PLANETS.items():
            ec_res, _ = swe.calc_ut(self._jd, planet)
            eq_res, _ = swe.calc_ut(self._jd, planet, swe.FLG_EQUATORIAL)
            lon, lat, dist, speed = ec_res[:4]
            dec = eq_res[1]
            house = self._get_house(lon)
            planets[name] = Planet(name, house, lon, lat, dist, speed, dec)

        return planets

    def _points(self):
        """ Get the main calculated points. """
        points = SerializableDict()

        """ Get the mean nodes. """
        res, _ = swe.calc_ut(self._jd, const.POINTS[const.NORTH_NODE])
        lon, _, _, speed = res[:4]
        house = self._get_house(lon)
        points[const.NORTH_NODE] = Point(const.NORTH_NODE, house, lon, speed)

        lon = swe.degnorm(Decimal(str(lon)) - 180)
        house = self._get_house(lon)
        points[const.SOUTH_NODE] = Point(const.SOUTH_NODE, house, lon, speed)

        """ Get the true nodes. """
        res, _ = swe.calc_ut(self._jd, const.POINTS[const.TRUE_NORTH_NODE])
        lon, _, _, speed = res[:4]
        house = self._get_house(lon)
        points[const.TRUE_NORTH_NODE] = Point(const.TRUE_NORTH_NODE, house, lon, speed)

        lon = swe.degnorm(Decimal(str(lon)) - 180)
        house = self._get_house(lon)
        points[const.TRUE_SOUTH_NODE] = Point(const.TRUE_SOUTH_NODE, house, lon, speed)

        """ Get the vertex. """
        ascmc, ascmcspeed = itemgetter('ascmc', 'ascmcspeed')(self._swe_houses_angles)
        lon = ascmc[const.POINTS[const.VERTEX]]
        speed = ascmcspeed[const.POINTS[const.VERTEX]]
        house = self._get_house(lon)
        points[const.VERTEX] = Point(const.VERTEX, house, lon, speed)

        """ Get the latest pre-natal full/new moon. """
        distance = self.planets[const.SUN].distance_to(self.planets[const.MOON])
        jd = transits.previous_new_moon(self._jd) if distance > 0 else transits.previous_full_moon(self._jd)
        res, _ = swe.calc_ut(jd, const.PLANETS[const.MOON])
        lon, _, _, speed = res[:4]
        house = self._get_house(lon)
        points[const.SYZYGY] = Point(const.SYZYGY, house, lon, speed)

        """ Get the part of fortune. """
        if self.type[const.DIURNAL]:
            formula = self.angles[const.ASC].longitude + self.planets[const.MOON].longitude - self.planets[const.SUN].longitude
        elif self.type[const.NOCTURNAL]:
            formula = self.angles[const.ASC].longitude + self.planets[const.SUN].longitude - self.planets[const.MOON].longitude

        lon = swe.degnorm(formula)
        house = self._get_house(lon)
        points[const.PARS_FORTUNA] = Point(const.PARS_FORTUNA, house, lon, 0)

        """ Get the Liliths. """
        res, _ = swe.calc_ut(self._jd, const.POINTS[const.LILITH])
        lon, _, _, speed = res[:4]
        house = self._get_house(lon)
        points[const.LILITH] = Point(const.LILITH, house, lon, speed)

        res, _ = swe.calc_ut(self._jd, const.POINTS[const.TRUE_LILITH])
        lon, _, _, speed = res[:4]
        house = self._get_house(lon)
        points[const.TRUE_LILITH] = Point(const.TRUE_LILITH, house, lon, speed)

        return points

    def _asteroids(self):
        return {}

    def _fixed_stars(self):
        return {}

    def _aspects(self):
        """ Calculate all requested aspects between chart items. """
        item_aspects = SerializableDict({v: SerializableList([]) for v in const.CHART_ITEMS.keys()})
        aspect_items = {**self.planets, **self.points}

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
