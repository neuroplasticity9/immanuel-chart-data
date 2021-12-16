from immanuel import position
from immanuel.angle import Angle, ChartAngle
from immanuel.position import Movement, Motion, Dignity


class Item:
    def __init__(self, name, lon, speed):
        self.name = name
        self.sign = position.sign(lon)
        self.longitude = ChartAngle(lon)
        self.speed = Angle(speed)

    def __str__(self):
        return f'{self.name} {self.sign} {self.longitude}'


class AxisPoint(Item):
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

    def _score(self):
        # TODO
        return 0
