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
from immanuel.items import Item
from immanuel.serializable import Serializable, SerializableBoolean


class Aspect(Serializable):
    """ Main class for encapsulating a chart aspect. This will specify
    which is the active and which is the passive partner in the aspect,
    and provides extra data such as associate/dissociate condition, and
    separative/applicative movement.

    """

    def __init__(self, aspecting: Item, aspected: Item, aspect_type: str, orb: float):
        self._aspecting_item = aspecting
        self._aspected_item = aspected
        self.aspecting = aspecting.name
        self.aspected = aspected.name
        self.type = aspect_type
        self.aspect = const.ASPECTS[aspect_type]
        self.distance = aspecting.distance_to(aspected)
        self.orb = Angle(orb)
        self.role = self._role()
        self.movement = self._movement()
        self.condition = self._condition()

    def _role(self):
        """ Determine whether the aspecting item is active or passive. """
        return SerializableBoolean().data({
            const.ACTIVE: self._aspecting_item.speed > self._aspected_item.speed,
            const.PASSIVE: self._aspecting_item.speed < self._aspected_item.speed,
        })

    def _movement(self):
        """ Determine if the active body is approaching, exactly on,
        or leaving its aspect with the passive body.
        """
        aspect_exact_longitude = (self._aspected_item.longitude + (self.aspect if self.distance >= 0 else -self.aspect)) % 360

        return SerializableBoolean().data({
            const.SEPARATIVE: self._aspecting_item.longitude > aspect_exact_longitude + const.EXACT_ORB,
            const.EXACT: aspect_exact_longitude - const.EXACT_ORB <= self._aspecting_item.longitude <= aspect_exact_longitude + const.EXACT_ORB,
            const.APPLICATIVE: self._aspecting_item.longitude < aspect_exact_longitude - const.EXACT_ORB,
        })

    def _condition(self):
        """ Determine if the orb pushes the aspected item out of sign. """
        aspect_exact_longitude = (self._aspecting_item.longitude + (self.aspect if self.distance >= 0 else -self.aspect)) % 360
        associate = position.sign(aspect_exact_longitude) == position.sign(self._aspected_item.longitude)

        return SerializableBoolean().data({
            const.ASSOCIATE: associate,
            const.DISSOCIATE: not associate,
        })

    def __str__(self):
        return f'{self.aspecting} {self.aspected} {self.type.lower()} within {self.orb} ({self.role} / {self.movement} / {self.condition})'


def find(aspecting: Item, aspected: Item):
    """ Find an aspect between two chart item pairs. """
    for aspect_type in const.DEFAULT_ASPECTS:
        aspect_angle = const.ASPECTS[aspect_type]
        orb = max(const.ORBS[aspecting.name][aspect_type], const.ORBS[aspected.name][aspect_type])
        distance = abs(aspecting.distance_to(aspected))

        if aspect_angle-orb <= distance <= aspect_angle+orb:
            return Aspect(aspecting, aspected, aspect_type, distance-aspect_angle)

    return None
