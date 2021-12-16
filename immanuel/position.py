"""
    This file is part of immanuel - (C) The Rift Lab
    Author: Robert Davies (robert@theriftlab.com)


    This module provides data for a planet's position.

    These classes provide simple serializable, stringable objects
    for various positional data such as movement, motion, and dignity,
    as well as helper functions.

"""

from immanuel import const


class PositionData(dict):
    def __init__(self, data):
        super().__init__(data)

    def __str__(self):
        for k, v in self.items():
            if v:
                return k.title()

        return 'None'


class Movement(PositionData):
    def __init__(self, speed):
        movement = {
            const.RETROGRADE: False,
            const.STATION: False,
            const.DIRECT: False,
        }

        if abs(speed) <= const.STATION_SPEED:
            movement[const.STATION] = True
        elif speed < -const.STATION_SPEED:
            movement[const.RETROGRADE] = True
        elif speed > const.STATION_SPEED:
            movement[const.DIRECT] = True

        super().__init__(movement)


class Motion(PositionData):
    def __init__(self, speed, name):
        motion = {
            const.SLOW: False,
            const.FAST: False,
        }

        if abs(speed) < const.MEAN_MOTIONS[name]:
            motion[const.SLOW] = True
        elif abs(speed) >= const.MEAN_MOTIONS[name]:
            motion[const.FAST] = True

        super().__init__(motion)


class Dignity(PositionData):
    def __init__(self, sign, name):
        dignity = {
            const.DOMICILE: False,
            const.EXALTED: False,
            const.DETRIMENT: False,
            const.FALL: False,
        }

        for dignity_type, dignity_sign in const.ESSENTIAL_DIGNITIES[name].items():
            if isinstance(sign, tuple):
                if sign in dignity_sign:
                    dignity[dignity_type] = True
            elif sign == dignity_sign:
                dignity[dignity_type] = True

        super().__init__(dignity)


def sign(lon):
    return const.SIGNS[int(lon/30)]


def is_out_of_bounds(dec):
    return not -const.DECLINATION_BOUND < dec < const.DECLINATION_BOUND