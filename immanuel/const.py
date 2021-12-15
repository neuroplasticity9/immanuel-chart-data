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

ALCABITUS = 'Alcabitus'
AZIMUTHAL = 'Azimuthal'
CAMPANUS = 'Campanus'
EQUAL = 'Equal'
KOCH = 'Koch'
MERIDIAN = 'Meridian'
MORINUS = 'Morinus'
PLACIDUS = 'Placidus'
POLICH_PAGE = 'Polich Page'
PORPHYRIUS = 'Porphyrius'
REGIOMONTANUS = 'Regiomontanus'
VEHLOW_EQUAL = 'Vehlow Equal'
WHOLE_SIGN = 'Whole Sign'

HOUSE_SYSTEMS = {
    ALCABITUS: b'B',
    AZIMUTHAL: b'H',
    CAMPANUS: b'C',
    EQUAL: b'A',
    KOCH: b'K',
    MERIDIAN: b'X',
    MORINUS: b'M',
    PLACIDUS: b'P',
    POLICH_PAGE: b'T',
    PORPHYRIUS: b'O',
    REGIOMONTANUS: b'R',
    VEHLOW_EQUAL: b'V',
    WHOLE_SIGN: b'W',
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

RETROGRADE = 'Retrograde'
STATION = 'Station'
DIRECT = 'Direct'

SLOW = 'Slow'
FAST = 'Fast'

# Main essential dignities

DOMICILE = 'Domicile'
EXALTED = 'Exalted'
DETRIMENT = 'Detriment'
FALL = 'Fall'

ESSENTIAL_DIGNITIES = {
    SUN: {
        DOMICILE: (LEO),
        EXALTED: ARIES,
        DETRIMENT: AQUARIUS,
        FALL: LIBRA,
    },
    MOON: {
        DOMICILE: (CANCER),
        EXALTED: TAURUS,
        DETRIMENT: CAPRICORN,
        FALL: SCORPIO,
    },
    MERCURY: {
        DOMICILE: (GEMINI, VIRGO),
        EXALTED: VIRGO,
        DETRIMENT: SAGITTARIUS,
        FALL: PISCES,
    },
    VENUS: {
        DOMICILE: (TAURUS, LIBRA),
        EXALTED: PISCES,
        DETRIMENT: ARIES,
        FALL: VIRGO,
    },
    MARS: {
        DOMICILE: (ARIES, SCORPIO),
        EXALTED: CAPRICORN,
        DETRIMENT: LIBRA,
        FALL: CANCER,
    },
    JUPITER: {
        DOMICILE: (SAGITTARIUS, PISCES),
        EXALTED: CANCER,
        DETRIMENT: GEMINI,
        FALL: CAPRICORN,
    },
    SATURN: {
        DOMICILE: (CAPRICORN, AQUARIUS),
        EXALTED: LIBRA,
        DETRIMENT: CANCER,
        FALL: ARIES,
    },
    URANUS: {
        DOMICILE: (AQUARIUS),
        EXALTED: SCORPIO,
        DETRIMENT: LEO,
        FALL: TAURUS,
    },
    NEPTUNE: {
        DOMICILE: (PISCES),
        EXALTED: LEO,
        DETRIMENT: VIRGO,
        FALL: AQUARIUS,
    },
    PLUTO: {
        DOMICILE: (SCORPIO),
        EXALTED: VIRGO,
        DETRIMENT: TAURUS,
        FALL: PISCES,
    }
}