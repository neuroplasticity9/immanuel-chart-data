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

import swisseph as swe

from immanuel import const, position
from immanuel.angles import Angle
from immanuel.items import Item
from immanuel.serializable import Serializable, SerializableBoolean


class Aspect(Serializable):
    """ Main class for encapsulating a chart aspect. This will specify
    which is the active and which is the passive partner in the aspect,
    and provide extra data such as associate/dissociate condition, and
    separative/applicative movement.

    """

    def __init__(self, active: Item, passive: Item, aspect_type: str, distance: Angle):
        self.active = active
        self.passive = passive
        self.type = aspect_type
        self.aspect = const.ASPECTS[aspect_type]
        self.distance = distance
        self._aspect_exact_lon = Angle(swe.degnorm(self.passive.longitude + (self.aspect if distance < 0 else -self.aspect)))
        self.orb = Angle(abs(distance) - self.aspect)
        self.movement = self._movement()
        self.condition = self._condition()

    def _movement(self) -> SerializableBoolean:
        """ Determine if the active body is approaching, exactly on,
        or leaving its aspect with the passive body.
        """
        exact = self._aspect_exact_lon-const.EXACT_ORB <= self.active.longitude <= self._aspect_exact_lon+const.EXACT_ORB
        applicative = not exact and (self.orb < 0 or self.active.movement[const.RETROGRADE])
        separative = not exact and not applicative

        return SerializableBoolean({
            const.APPLICATIVE: applicative,
            const.EXACT: exact,
            const.SEPARATIVE: separative,
        })

    def _condition(self) -> SerializableBoolean:
        """ Determine if the orb has pushed the aspected item out of sign. """
        associate = position.sign(self._aspect_exact_lon) == position.sign(self.active.longitude)

        return SerializableBoolean({
            const.ASSOCIATE: associate,
            const.DISSOCIATE: not associate,
        })

    def __str__(self):
        return f'{self.active.name} {self.passive.name} {self.type.lower()} within {self.orb} ({self.movement} / {self.condition})'


def active_passive(item1: Item, item2: Item) -> tuple:
    """ Returns active (fastest) then passive (slowest) chart item. """
    return (item1, item2) if abs(item1.speed) > abs(item2.speed) else (item2, item1)
