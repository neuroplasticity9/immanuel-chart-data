"""
    This file is part of immanuel - (C) The Rift Lab
    Author: Robert Davies (robert@theriftlab.com)


    This module provides conversions between D:M:S and decimal.

    These functions perform simple conversions between the base-12 data used
    by astrology (ie. angles, coordinates, and time) in string/list format,
    and decimal numbers in float format.

"""

import math
import re
from decimal import Decimal


FORMAT_TIME = 0
FORMAT_DMS = 1
FORMAT_LAT = 2
FORMAT_LON = 3


def dms_to_dec(dms: list) -> float:
    """ Returns the decimal conversion of a D:M:S list. """
    dec = sum([float(v) / 60**k for k, v in enumerate(dms[1:])])
    return dec if dms[0] == '+' else -dec


def dec_to_dms(dec: float) -> list[str | int]:
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


def dms_to_string(dms: list, format: int = FORMAT_DMS) -> str:
    """ Returns a D:M:S list as either a D:M:S, D°M'S" or
    coordinate string. """
    if format == FORMAT_DMS or format == FORMAT_TIME:
        if format == FORMAT_DMS:
            symbols = (u'\N{DEGREE SIGN}', "'", '"')
            string = ''.join(['%02d' % v + symbols[k] for k, v in enumerate(dms[1:])])
        elif format == FORMAT_TIME:
            string = ':'.join(['%02d' % v for v in dms[1:]])
        if dms[0] == '-':
            string = '-' + string
    elif format == FORMAT_LAT or format == FORMAT_LON:
        if format == FORMAT_LAT:
            dir = 'S' if dms[0] == '-' else 'N'
        elif format == FORMAT_LON:
            dir = 'W' if dms[0] == '-' else 'E'
        minutes = dms[2] + math.ceil(((dms[3]/60)*100))/100
        string = f'{dms[1]}{dir}{minutes}'
    else:
        string = ''

    return string


def string_to_dms(string: str) -> list[str | int]:
    """ Takes either a float, a float-as-string, a 12w34.56-type string,
    or a 12°34'56.78" / 12:34:56.78-type string, and returns a float. """
    try:
        return float(string)
    except ValueError:
        digits = re.findall(r'[0-9\.-]+', string)
        floats = [float(v) for v in digits]
        char = string[len(digits[0])].upper()

        if char in 'NESW':
            return ['-' if char in 'SW' else '+'] + floats
        else:
            return ['-' if floats[0] < 0 else '+', abs(floats[0])] + floats[1:]


def dec_to_string(dec: float, format: int = FORMAT_DMS) -> str:
    """ Returns a decimal float as either a D:M:S or a D°M'S" string. """
    return dms_to_string(dec_to_dms(dec), format)


def string_to_dec(string: str) -> str:
    return dms_to_dec(string_to_dms(string))