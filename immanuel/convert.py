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
    return float(f'{dms[0]}{dec}')


def dec_to_dms(dec: float, resolution: int = 2):
    """ Returns the D:M:S conversion of a decimal float. """
    values = [abs(dec)]

    for i in range(resolution):
        values.append(Decimal(str(values[i])) % 1 * 60)

    # Round up last digit if it's not a M or S that would round to 60.
    if resolution == 0 or values[resolution] < 59.5:
        values[resolution] = round(values[resolution])
    # Otherwise work backwards zeroing 60 digits & rounding up pre-60 digits.
    else:
        for i in range(resolution, 0, -1):
            if values[i] >= 59.5:
                values[i-1] += 1
                values[i:] = [0 for x in values[i:]]
                if values[i-1] < 59.5:
                    break

    return ['-' if dec < 0 else '+'] + [int(v) for v in values]


def coords_to_dec(lat, lon):
    """ Ensures the passed values are in decimal format. """
    return [_coord_to_dec(v) for v in [lat, lon]]

def _coord_to_dec(coord):
    """ Takes either a float, a float-as-string, or a 'XXyZZ' string,
    and returns a float. """
    if isinstance(coord, float):
        return coord

    try:
        return float(coord)
    except ValueError:
        direction = next(filter(str.isalpha, coord))
        dms = ['-' if direction.upper() in 'SW' else '+'] + coord.split(direction)
        return dms_to_dec(dms)
