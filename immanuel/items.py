"""
    This file is part of immanuel - (C) The Rift Lab
    Author: Robert Davies (robert@theriftlab.com)


    This module provides clases for each chart item.

    Planets, houses, axis angles, calculated points,
    asteroids and fixed stars are encapsulated here.

"""

from immanuel import position
from immanuel.angles import Angle, SignAngle
from immanuel.position import Movement, Motion, Dignity
from immanuel.serializable import Serializable


class Item(Serializable):
    def __init__(self, name, lon, speed):
        self.name = name
        self.sign = position.sign(lon)
        self.longitude = SignAngle(lon)
        self.speed = Angle(speed)

    def __str__(self):
        return f'{self.name} {self.sign} {self.longitude}'


class AxisAngle(Item):
    def __init__(self, name, lon, speed):
        super().__init__(name, lon, speed)


class House(Item):
    def __init__(self, number, cusp, size, speed):
        super().__init__(number, cusp, speed)
        self.size = size


class Planet(Item):
    def __init__(self, name, house, lon, lat, dist, speed, dec):
        super().__init__(name, lon, speed)
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
        return f'{super().__str__()} house {self.house}'

    def _score(self):
        # TODO
        return 0


class Point(Item):
    def __init__(self, name, lon, speed):
        super().__init__(name, lon, speed)


class Asteroid(Item):
    def __init__(self, name, lon, speed):
        super().__init__(name, lon, speed)


class FixedStar(Item):
    def __init__(self, name, lon, speed):
        super().__init__(name, lon, speed)
