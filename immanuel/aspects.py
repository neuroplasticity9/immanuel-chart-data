"""
    This file is part of immanuel - (C) The Rift Lab
    Author: Robert Davies (robert@theriftlab.com)


    This module contains aspect calculations.

    The Aspect class is serializable, and is populated by the find()
    function, which also determines which of the aspecting pair is
    active and which is passive. By default it will only return
    aspects where the main aspecting planet in the chech is the
    active/initiating partner.

"""

from immanuel import const, position
from immanuel.angles import Angle
from immanuel.items import Item, Planet
from immanuel.serializable import Serializable, SerializableBoolean


ALL = 0
ACTIVE = 1
PASSIVE = 2


class Aspect(Serializable):
    """ Main class for encapsulating a chart aspect. This will specify
    which is the active and which is the passive partner in the aspect,
    and provides extra data such as associate/dissociate condition, and
    separative/applicative movement.

    """

    def __init__(self, active: Item, passive: Item, aspect_type: str, orb: float):
        self._active_item = active
        self._passive_item = passive
        self.active = active.name
        self.passive = passive.name
        self.type = aspect_type
        self.orb = Angle(orb)
        self.condition = self._condition()

    def _condition(self):
        """ Determine if the orb pushes the aspected item out of sign. """
        distance = self._active_item.distance_to(self._passive_item)
        exact_longitude =  (self._active_item.longitude + (const.ASPECTS[self.type] if distance >= 0 else -const.ASPECTS[self.type])) % 360
        exact_sign = position.sign(exact_longitude)
        actual_sign = position.sign(self._passive_item.longitude)
        condition = SerializableBoolean()

        condition.data({
            const.ASSOCIATE: exact_sign == actual_sign,
            const.DISSOCIATE: exact_sign != actual_sign,
        })

        return condition

    def __str__(self):
        return f'{self.active} {self.type} {self.passive} within {self.orb} ({self.condition})'


def find(aspecting: Item, aspected: Item, search: int = ACTIVE):
    """ Find an aspect between two active/passive chart item pairs.
    By default this will only return aspects where the item being
    checked ("aspecting") is the active partner.

    """
    for aspect_type in const.DEFAULT_ASPECTS:
        aspect_angle = const.ASPECTS[aspect_type]
        orb = const.ORBS[aspecting.name][aspect_type]
        distance = abs(aspecting.distance_to(aspected))

        if aspect_angle-orb <= distance <= aspect_angle+orb:
            active, passive = (aspecting, aspected) if aspecting.speed > aspected.speed else (aspected, aspecting)

            if (aspecting == active and search != PASSIVE) or (aspecting == passive and search != ACTIVE):
                return Aspect(active, passive, aspect_type, abs(distance-aspect_angle))

    return None
