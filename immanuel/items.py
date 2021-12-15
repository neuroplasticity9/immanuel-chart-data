from immanuel import const
from immanuel.angle import Angle, ChartAngle


class Item:
    def __init__(self):
        self.name = ''
        self.sign = ''
        self.longitude = None
        self.speed = 0.0
        self.aspects = {}

    def _get_sign(self, longitude):
        return const.SIGNS[int(longitude/30)]

    def __str__(self):
        return f'{self.name} {self.sign} {self.longitude} {self.speed}'


class AxisPoint(Item):
    def __init__(self, name, lon, speed):
        self.name = name
        self.sign = self._get_sign(lon)
        self.longitude = ChartAngle(lon)
        self.speed = Angle(speed)


class House(Item):
    def __init__(self, number, cusp, size, speed):
        self.name = number
        self.sign = self._get_sign(cusp)
        self.longitude = ChartAngle(cusp)
        self.size = size
        self.speed = Angle(speed)


class Planet(Item):
    def __init__(self, name, house, lon, lat, dist, speed, dec):
        self.name = name
        self.sign = self._get_sign(lon)
        self.house = house
        self.latitude = Angle(lat)
        self.longitude = ChartAngle(lon)
        self.declination = Angle(dec)
        self.speed = Angle(speed)
        self.distance = dist
        self.movement = self._movement()
        self.motion = self._motion()
        self.modality = ''
        self.gender = ''
        self.dignity = ''
        self.out_of_bounds = not const.DEC_LOWER_BOUND < self.declination < const.DEC_UPPER_BOUND

    def _movement(self):
        if abs(self.speed) <= const.STATION_SPEED:
            return const.MOVEMENT_STATION
        elif self.speed < -const.STATION_SPEED:
            return const.MOVEMENT_RETROGRADE
        elif self.speed > const.STATION_SPEED:
            return const.MOVEMENT_DIRECT

    def _motion(self):
        if abs(self.speed) < const.MEAN_MOTIONS[self.name]:
            return const.MOTION_SLOW
        elif abs(self.speed) >= const.MEAN_MOTIONS[self.name]:
            return const.MOTION_FAST
