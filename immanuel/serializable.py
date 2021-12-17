"""
    This file is part of immanuel - (C) The Rift Lab
    Author: Robert Davies (robert@theriftlab.com)


    This module provides a base class for easily-serializable objects.

    Objects inheriting from the Serializable class can be turned into dicts.
    These objects are also iterable, using the same public members.

"""


class Serializable:
    """ Provides inheriting classes with the serialized() method to
    recursively serialize their public members (not beginning with '_')
    into a dict, and to iterate over the same data.

    """

    def serialized(self) -> dict:
        """ Returns a dict of all public members. """
        return {k:v.serialized() if isinstance(v, Serializable) else v for k, v in self._public_items()}

    def _public_items(self) -> dict:
        """ Returns all members not starting with '_'. """
        return {k:v for k, v in self.__dict__.items() if k[0] != '_'}.items()

    def __iter__(self):
        """ Simple iterator for public members. """
        for item in self._public_items():
            yield item
