from decimal import Decimal

import swisseph as swe

from immanuel import const, convert
from immanuel.angle import Angle
from immanuel.items import AxisPoint, House, Planet


class Chart:
    def __init__(self, dt, lat, lon, hsys):
        self.jd = dt.jd
        self.lat = lat
        self.lon = lon
        self.hsys = const.HOUSE_SYSTEMS[hsys if hsys is not None else const.PLACIDUS]
        self.aspects = {}   # TODO: default list
        self.orbs = {}      # TODO: default list
        self.houses = {}
        self.axis = {}
        self.points = {}
        self.planets = {}
        self.asteroids = {}
        self.fixed_stars = {}
        self._swe_axis = ()
        self._houses()
        self._axis()
        self._points()
        self._planets()


    def _houses(self):
        """ This must be called before _axis() since pywisseph provides the
        house cusps and axis point angles with the same function call. """
        cusps, ascmc, cuspsspeed, ascmcspeed = swe.houses_ex2(self.jd, self.lat, self.lon, self.hsys)
        self._swe_axis = (ascmc, ascmcspeed)

        for i, cusp in enumerate(cusps):
            house_number = i + 1
            size = abs(float((Decimal(str(cusps[i+1 if i < 11 else 0])) - Decimal(str(cusp))) % 360))
            self.houses[house_number] = House(house_number, cusp, size, cuspsspeed[i])


    def _axis(self):
        """ Get the main axis points from _swe_axis stored by _houses(). """
        for name, swe_index in const.ANGLES.items():
            lon = self._swe_axis[0][swe_index]
            speed = self._swe_axis[1][swe_index]

            if name in [const.DESC, const.IC]:
                lon = abs((lon - 180) % 360)

            self.axis[name] = AxisPoint(name, lon, speed)


    def _points(self):
        # Nodes
        # Syzygy
        # Pars Fortuna
        # Liliths
        # Vertex
        return {}


    def _planets(self):
        """ Get the ten main planets. """
        for name, planet in const.PLANETS.items():
            ec_res, ec_flg = swe.calc_ut(self.jd, planet)
            eq_res, eq_flg = swe.calc_ut(self.jd, planet, swe.FLG_EQUATORIAL)
            lon, lat, dist, speed = ec_res[:4]
            dec = eq_res[1]
            house = self._get_house(lon)
            self.planets[name.lower()] = Planet(name, house, lon, lat, dist, speed, dec)


    def asteroids(self, asteroids):
        return {}


    def fixed_stars(self, fixed_stars):
        return {}


    def _get_house(self, lon):
        for house in self.houses.values():
            if lon >= house.longitude and lon < house.longitude + house.size:
                return house.name
        return None
