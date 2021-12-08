"""
    This file is part of immanuel - (C) The Rift Lab
    Author: Robert Davies (robert@theriftlab.com)


    This module provides conversions between D:M:S and decimal.

    These functions perform simple conversions between the base-12 data used
    by astrology (ie. angles, coordinates, and time) in list format,
    and decimal numbers in float format.

"""

from decimal import Decimal


def dms_to_dec(dms: list):
    """ Returns the decimal conversion of a D:M:S list. """
    dec = sum([float(v) / 60**k for k, v in enumerate(dms[1:])])
    return dec if dms[0] == '+' else -dec


def dec_to_dms(dec: float):
    """ Returns the rounded D:M:S conversion of a decimal float. """
    dms = ['-' if dec < 0 else '+', abs(dec)]

    for i in range(1, 3):
        dms.append(Decimal(str(dms[i])) % 1 * 60)
        dms[i] = int(dms[i])

    dms[3] = round(dms[3])

    for i in range(3, 1, -1):
        if dms[i] == 60:
            dms[i-1] += 1
            dms[i] = 0

    return dms


def coords_to_dec(lat, lon):
    """ Ensures the passed values are in decimal format. """
    return [_coord_to_dec(v) for v in [lat, lon]]

def _coord_to_dec(coord):
    """ Takes either a float, a float-as-string, or a '12w34.56' type string,
    and returns a float. """
    try:
        return float(coord)
    except ValueError:
        direction = next(filter(str.isalpha, coord))
        dms = ['-' if direction.upper() in 'SW' else '+'] + coord.split(direction)
        return dms_to_dec(dms)
