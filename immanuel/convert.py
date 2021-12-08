"""
    This file is part of immanuel - (C) The Rift Lab
    Author: Robert Davies (robert@theriftlab.com)


    This module provides conversions between D:M:S and decimal.

    These functions perform simple conversions between the base-12 data used
    by astrology (ie. angles, coordinates, and time) in string/list format,
    and decimal numbers in float format.

"""

import re
from decimal import Decimal


FORMAT_TIME = 0
FORMAT_DMS = 1


def dms_to_dec(dms: list):
    """ Returns the decimal conversion of a D:M:S list. """
    dec = sum([float(v) / 60**k for k, v in enumerate(dms[1:])])
    return dec if dms[0] == '+' else -dec


def dms_to_string(dms: list, format: int = FORMAT_DMS):
    """ Returns a D:M:S list as either a D:M:S or a D°M'S" string. """
    if format == FORMAT_TIME:
        return dms[0] + ':'.join(['%02d' % v for v in dms[1:]])
    elif format == FORMAT_DMS:
        return dms[0] + ''.join(['%02d' % v + [u'\N{DEGREE SIGN}', "'", '"'][k] for k, v in enumerate(dms[1:])])


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


def dec_to_string(dec: float, format: int = FORMAT_DMS):
    """ Returns a decimal float as either a D:M:S or a D°M'S" string. """
    return dms_to_string(dec_to_dms(dec), format)


def coords_to_dec(lat, lon):
    """ Converts the passed values to decimal format if necessary. """
    return [_coord_to_dec(v) for v in [lat, lon]]


def _coord_to_dec(coord):
    """ Takes either a float, a float-as-string, a 12w34.56-type string,
    or a 12°34'56.78"-type string, and returns a float. """
    try:
        return float(coord)
    except ValueError:
        digits = re.findall(r'[0-9\.-]+', coord)
        char = coord[len(digits[0])].upper()
        floats = [float(v) for v in digits]

        if char in 'NESW':
            dms = ['-' if char in 'SW' else '+'] + floats
        elif char == u'\N{DEGREE SIGN}':
            dms = ['-' if floats[0] < 0 else '+', abs(floats[0])] + floats[1:]

        return dms_to_dec(dms)
