"""
    This file is part of immanuel - (C) The Rift Lab
    Author: Robert Davies (robert@theriftlab.com)


    This module defines constants for chart object & aspect data.

"""

import swisseph as swe


# Signs

ARIES = 'Aries'
TAURUS = 'Taurus'
GEMINI = 'Gemini'
CANCER = 'Cancer'
LEO = 'Leo'
VIRGO = 'Virgo'
LIBRA = 'Libra'
SCORPIO = 'Scorpio'
SAGITTARIUS = 'Sagittarius'
CAPRICORN = 'Capricorn'
AQUARIUS = 'Aquarius'
PISCES = 'Pisces'

SIGNS = [
    ARIES, TAURUS, GEMINI, CANCER, LEO, VIRGO, LIBRA,
    SCORPIO, SAGITTARIUS, CAPRICORN, AQUARIUS, PISCES
]

# Planets

SUN = 'Sun'
MOON = 'Moon'
MERCURY = 'Mercury'
VENUS = 'Venus'
MARS = 'Mars'
JUPITER = 'Jupiter'
SATURN = 'Saturn'
URANUS = 'Uranus'
NEPTUNE = 'Neptune'
PLUTO = 'Pluto'

PLANETS = {
    SUN: swe.SUN,
    MOON: swe.MOON,
    MERCURY: swe.MERCURY,
    VENUS: swe.VENUS,
    MARS: swe.MARS,
    JUPITER: swe.JUPITER,
    SATURN: swe.SATURN,
    URANUS: swe.URANUS,
    NEPTUNE: swe.NEPTUNE,
    PLUTO: swe.PLUTO,
}

# Main angles

ASC = 'Asc'
DESC = 'Desc'
MC = 'MC'
IC = 'IC'

ANGLES = {
    ASC: swe.ASC,
    DESC: swe.ASC,
    MC: swe.MC,
    IC: swe.MC,
}

# House systems

HSYS_ALCABITUS = 'Alcabitus'
HSYS_AZIMUTHAL = 'Azimuthal'
HSYS_CAMPANUS = 'Campanus'
HSYS_EQUAL = 'Equal'
HSYS_KOCH = 'Koch'
HSYS_MERIDIAN = 'Meridian'
HSYS_MORINUS = 'Morinus'
HSYS_PLACIDUS = 'Placidus'
HSYS_POLICH_PAGE = 'Polich Page'
HSYS_PORPHYRIUS = 'Porphyrius'
HSYS_REGIOMONTANUS = 'Regiomontanus'
HSYS_VEHLOW_EQUAL = 'Vehlow Equal'
HSYS_WHOLE_SIGN = 'Whole Sign'

HOUSE_SYSTEMS = {
    HSYS_ALCABITUS: b'B',
    HSYS_AZIMUTHAL: b'H',
    HSYS_CAMPANUS: b'C',
    HSYS_EQUAL: b'A',
    HSYS_KOCH: b'K',
    HSYS_MERIDIAN: b'X',
    HSYS_MORINUS: b'M',
    HSYS_PLACIDUS: b'P',
    HSYS_POLICH_PAGE: b'T',
    HSYS_PORPHYRIUS: b'O',
    HSYS_REGIOMONTANUS: b'R',
    HSYS_VEHLOW_EQUAL: b'V',
    HSYS_WHOLE_SIGN: b'W',
}

# Astrological constants

DEC_LOWER_BOUND = -23.45
DEC_UPPER_BOUND = 23.45

MEAN_MOTIONS = {
    'Sun': 0.985556,
    'Moon': 13.176389,
    'Mercury': 1.383333,
    'Venus': 1.2,
    'Mars': 0.524167,
    'Ceres': 0.211111,
    'Jupiter': 0.083056,
    'Saturn': 0.033611,
    'Uranus': 0.011667,
    'Neptune': 0.006667,
    'Pluto': 0.004167,
}

STATION_SPEED = 0.0003      # ~1 second of movement

# Movement & motion

MOVEMENT_RETROGRADE = 'Retrograde'
MOVEMENT_STATION = 'Station'
MOVEMENT_DIRECT = 'Direct'

MOTION_SLOW = 'Slow'
MOTION_FAST = 'Fast'