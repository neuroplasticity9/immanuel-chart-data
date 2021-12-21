"""
    This file is part of immanuel - (C) The Rift Lab
    Author: Robert Davies (robert@theriftlab.com)


    This module provides clases for each chart item.

    Planets, houses, axis angles, calculated points,
    asteroids and fixed stars are encapsulated here.

"""

from __future__ import annotations

from immanuel import const, position
from immanuel.angles import Angle, SignAngle
from immanuel.position import Movement, Motion, Dignity
from immanuel.serializable import Serializable


class Item(Serializable):
    """ Generic chart item. Specific item types (planets, angles etc.)
    inherit from this and add their own members & methods if necessary.

    """

    def __init__(self, name, lon, speed):
        self.type = None
        self.name = name
        self.sign = position.sign(lon)
        self.longitude = SignAngle(lon)
        self.speed = Angle(speed)

    def distance_to(self, other: Item):
        return self.longitude.diff(other.longitude)

    def __eq__(self, other: Item):
        """ Equality based on name. """
        return self.name == other.name

    def __ne__(self, other: Item):
        """ Inequality based on name. """
        return self.name != other.name

    def __str__(self):
        """ Simple string representation. """
        return f'{self.name} {self.sign} {self.longitude}'


class AxisAngle(Item):
    """ Asc, Desc, MC & IC. """
    def __init__(self, name, lon, speed):
        super().__init__(name, lon, speed)
        self.type = const.ANGLE


class House(Item):
    """ House position & size. """
    def __init__(self, number, cusp, size, speed):
        super().__init__(number, cusp, speed)
        self.type = const.HOUSE
        self.size = size


class Planet(Item):
    def __init__(self, name, house, lon, lat, dist, speed, dec):
        super().__init__(name, lon, speed)
        self.type = const.PLANET
        self.house = house
        self.latitude = Angle(lat)
        self.declination = Angle(dec)
        self.distance = dist
        self.out_of_bounds = position.is_out_of_bounds(dec)
        self.movement = Movement(speed)
        self.motion = Motion(speed, name)
        self.dignity = Dignity(self.sign, name)
        self.score = self._score()
        # TODO: extras for moon
        # void of course
        # phase
        # balsamic??

    def __str__(self):
        ordinal_suffix = ('st', 'nd', 'rd')[self.house-1] if self.house < 4 else 'th'
        return f'{super().__str__()} {self.movement} {self.house}{ordinal_suffix} house'

    def _score(self):
        # TODO
        return 0


class Point(Item):
    def __init__(self, name, house, lon, speed):
        super().__init__(name, lon, speed)
        self.type = const.POINT
        self.house = house


class Asteroid(Item):
    def __init__(self, name, house, lon, speed):
        super().__init__(name, lon, speed)
        self.type = const.ASTEROID
        self.house = house


class FixedStar(Item):
    def __init__(self, name, house, lon, speed):
        super().__init__(name, lon, speed)
        self.type = const.FIXED_STAR
        self.house = house
