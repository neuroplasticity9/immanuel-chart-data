"""
    This file is part of immanuel - (C) The Rift Lab
    Author: Robert Davies (robert@theriftlab.com)


    This module provides clases for each chart item.

    Planets, houses, axis angles, calculated points,
    asteroids and fixed stars are encapsulated here.

"""

from __future__ import annotations

from immanuel import angles, chart, const
from immanuel.angles import Angle, SignAngle
from immanuel.serializable import Serializable, SerializableBoolean


class Item(Serializable):
    """ Generic chart item. Specific item types (planets, angles etc.)
    inherit from this and add their own members & methods if necessary.

    """

    def __init__(self, name, lon, speed):
        self.type = None
        self.name = name
        self.house = 0
        self.sign = chart.sign(lon)
        self.longitude = SignAngle(lon)
        self.speed = Angle(speed)
        self.movement = self._movement()

    def _movement(self) -> SerializableBoolean:
        """ Retrograde, station or direct movement. """
        return SerializableBoolean({
            const.RETROGRADE: self.speed < -const.STATION_SPEED,
            const.STATION: abs(self.speed) <= const.STATION_SPEED,
            const.DIRECT: self.speed > const.STATION_SPEED,
        })

    def distance_to(self, other: Item, normalise: int = angles.SHORTEST) -> Angle:
        """ Chart angle distance between two chart items. """
        return self.longitude.diff(other.longitude, normalise)

    def __eq__(self, other: Item) -> bool:
        """ Equality based on name. """
        return self.name == other.name

    def __ne__(self, other: Item) -> bool:
        """ Inequality based on name. """
        return self.name != other.name

    def __str__(self) -> str:
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
    """  """
    def __init__(self, name, house, lon, lat, dist, speed, dec, out_of_bounds):
        super().__init__(name, lon, speed)
        self.type = const.PLANET
        self.house = house
        self.latitude = Angle(lat)
        self.declination = Angle(dec)
        self.distance = dist
        self.out_of_bounds = out_of_bounds
        self.motion = self._motion()
        self.mutual_reception = None
        self.mutual_reception_house = None
        self.mutual_reception_exaltion = None
        self.dignities = None
        self.debilities = None
        self.score = 0

    def _motion(self) -> SerializableBoolean:
        """ Fast or slow movement. """
        return SerializableBoolean({
            const.SLOW: abs(self.speed) < const.MEAN_MOTIONS[self.name],
            const.FAST: abs(self.speed) >= const.MEAN_MOTIONS[self.name],
        })

    def __str__(self) -> str:
        ordinal_suffix = ('st', 'nd', 'rd')[self.house-1] if self.house < 4 else 'th'
        return f'{super().__str__()} {self.movement} {self.house}{ordinal_suffix} house {self.score:+}'


class Point(Item):
    """  """
    def __init__(self, name, house, lon, speed):
        super().__init__(name, lon, speed)
        self.type = const.POINT
        self.house = house


class Asteroid(Item):
    """  """
    def __init__(self, name, house, lon, dist, speed):
        super().__init__(name, lon, speed)
        self.type = const.ASTEROID
        self.house = house
        self.distance = dist


class FixedStar(Item):
    """  """
    def __init__(self, name, house, lon, dist, speed):
        super().__init__(name, lon, speed)
        self.type = const.FIXED_STAR
        self.house = house
        self.distance = dist
