"""
    This file is part of immanuel - (C) The Rift Lab
    Author: Robert Davies (robert@theriftlab.com)


    This module provides a base class for easily-serializable objects.

    Objects inheriting from the Serializable class can be turned into dicts.
    These objects are also iterable, using the same public members.

"""

# TODO: make this abstract
class SerializableBase:
    def serialize(self) -> dict:
        pass


class Serializable(SerializableBase):
    """ Provides inheriting classes with the serialize() method to
    recursively serialize their public members (not beginning with '_')
    into a dict, and to iterate over the same data.

    """

    def serialize(self) -> dict:
        """ Returns a dict of all public members. """
        return {k: v.serialize() if isinstance(v, SerializableBase) else v for k, v in self._public_items()}

    def _public_items(self) -> dict:
        """ Returns all members not starting with '_'. """
        return {k: v for k, v in self.__dict__.items() if k[0] != '_'}.items()

    def __iter__(self):
        """ Simple iterator for public members. """
        for item in self._public_items():
            yield item


class SerializableBoolean(Serializable):
    """ Simple extension allows a stringified version to return
    whichever members are True, useful for objects that contain
    only boolean members.

    """

    def data(self, data: dict) -> Serializable:
        """ Sets the object's members to the passed dict and returns
        self for easy instantiation with a dict.
        """
        self.__dict__.update(data)
        return self

    def __str__(self):
        return ', '.join((k.title() for k, v in self if v))


class SerializableDict(SerializableBase, dict):
    def serialize(self) -> dict:
        return {k: v.serialize() if isinstance(v, SerializableBase) else v for k, v in self.items()}


class SerializableList(SerializableBase, list):
    def serialize(self) -> list:
        return [v.serialize() if isinstance(v, SerializableBase) else v for v in self]