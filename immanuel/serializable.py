"""
    This file is part of immanuel - (C) The Rift Lab
    Author: Robert Davies (robert@theriftlab.com)


    This module provides base classes for easily-serializable objects.

    Objects inheriting from the Serializable class can be turned into dicts.
    These objects are also iterable, using the same public members.
    SerializableDict and SerializableList are designed to be standard
    dicts and lists but capable of recurively serializing any members
    which are serializable.

"""

from abc import ABC, abstractmethod


class SerializableBase(ABC):
    """ Serves as a standard base class for all serializable classes.
    The idea is to have a standard, recursive method of serializing
    class objects into dicts, or dicts/lists of dicts, suitable for
    JSON output.

    """

    @abstractmethod
    def serialize(self):
        """ It is up to each child class's implementation what serialize()
        will return, but it should be either a dict or a dict/list of dicts.
        """
        pass


class Serializable(SerializableBase):
    """ Provides inheriting classes with a serialize() implementation that
    recursively serializes their public members (not beginning with '_')
    into a dict, and an iterator for the same data.

    """

    def serialize(self) -> dict:
        """ Returns a dict of all public members. """
        return {k: v.serialize() if isinstance(v, SerializableBase) else v for k, v in self._public_items()}

    def _public_items(self) -> dict:
        """ Returns all members not starting with '_'. """
        return {k: v for k, v in self.__dict__.items() if k[0] != '_'}.items()

    def __iter__(self) -> iter:
        """ Simple iterator for public members. """
        for item in self._public_items():
            yield item


class SerializableBoolean(Serializable):
    """ Allows the inheriting objects' __str__() to return the names of
    whichever members are True, useful for objects that contain only
    boolean members.

    """

    def __init__(self, data: dict = {}):
        self.__dict__.update(data)

    def data(self, data: dict):
        self.__dict__.update(data)

    def __getitem__(self, key):
        return self.__dict__.get(key, None)

    def __str__(self) -> str:
        return ', '.join((k.title() for k, v in self if isinstance(v, bool) and v))


class SerializableDict(SerializableBase, dict):
    """ Allows a dict of Serializable objects to be serialized. """
    def serialize(self) -> dict:
        return {k: v.serialize() if isinstance(v, SerializableBase) else v for k, v in self.items()}


class SerializableList(SerializableBase, list):
    """ Allows a list of Serializable objects to be serialized. """
    def serialize(self) -> list:
        return [v.serialize() if isinstance(v, SerializableBase) else v for v in self]