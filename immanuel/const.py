"""
    This file is part of immanuel - (C) The Rift Lab
    Author: Robert Davies (robert@theriftlab.com)


    This module defines constants for chart object & aspect data.

"""

import swisseph as swe


# Chart types

DIURNAL = 'diurnal'
NOCTURNAL = 'nocturnal'

# Chart item types

HOUSE = 'house'
ANGLE = 'angle'
PLANET = 'planet'
POINT = 'point'
ASTEROID = 'asteroid'
FIXED_STAR = 'fixed star'

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

SIGNS = (
    ARIES, TAURUS, GEMINI, CANCER, LEO, VIRGO, LIBRA,
    SCORPIO, SAGITTARIUS, CAPRICORN, AQUARIUS, PISCES
)

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

# Points

NORTH_NODE = 'North Node'
SOUTH_NODE = 'South Node'
TRUE_NORTH_NODE = 'True North Node'
TRUE_SOUTH_NODE = 'True South Node'
SYZYGY = 'Syzygy'
PARS_FORTUNA = 'Pars Fortuna'
VERTEX = 'Vertex'
LILITH = 'Dark Moon Lilith'             # Avoid key clashes with asteroid Lilith
TRUE_LILITH = 'True Lilith'

POINTS = {
    NORTH_NODE: swe.MEAN_NODE,
    SOUTH_NODE: None,                   # Calculated in chart
    TRUE_NORTH_NODE: swe.TRUE_NODE,
    TRUE_SOUTH_NODE: None,              # Calculated in chart
    SYZYGY: None,                       # Calculated in chart
    PARS_FORTUNA: None,                 # Calculated in chart
    VERTEX: swe.VERTEX,
    LILITH: swe.MEAN_APOG,
    TRUE_LILITH: swe.OSCU_APOG,
}

# Asteroids

CHIRON = 'Chiron'
PHOLUS = 'Pholus'
CERES = 'Ceres'
PALLAS = 'Pallas'
JUNO = 'Juno'
VESTA = 'Vesta'

ASTEROIDS = {
    CHIRON: swe.CHIRON,
    PHOLUS: swe.PHOLUS,
    CERES: swe.CERES,
    PALLAS: swe.PALLAS,
    JUNO: swe.JUNO,
    VESTA: swe.VESTA,
}

# Default items

DEFAULT_ITEMS = [
    ASC, DESC, MC, IC,
    SUN, MOON, MERCURY, VENUS, MARS, JUPITER, SATURN, URANUS, NEPTUNE, PLUTO,
    NORTH_NODE, SOUTH_NODE, PARS_FORTUNA, VERTEX,
    CHIRON
]

# All items

CHART_ITEMS = {
    **ANGLES,
    **PLANETS,
    **POINTS,
    **ASTEROIDS,
}

# Astrological constants

DECLINATION_BOUNDARY = 23.45

MEAN_MOTIONS = {
    SUN: 0.985556,
    MOON: 13.176389,
    MERCURY: 1.383333,
    VENUS: 1.2,
    MARS: 0.524167,
    JUPITER: 0.083056,
    SATURN: 0.033611,
    URANUS: 0.011667,
    NEPTUNE: 0.006667,
    PLUTO: 0.004167,
}

STATION_SPEED = 0.0003      # ~1 second of movement

# Movement & motion

RETROGRADE = 'retrograde'
STATION = 'station'
DIRECT = 'direct'

SLOW = 'slow'
FAST = 'fast'

# Main essential dignities

DOMICILE = 'domicile'
EXALTED = 'exalted'
DETRIMENT = 'detriment'
FALL = 'fall'

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

# Aspects & orbs

CONJUNCTION = 'Conjunction'
OPPOSITION = 'Opposition'
SQUARE = 'Square'
TRINE = 'Trine'
SEXTILE = 'Sextile'
SEPTILE = 'Septile'
SEMISQUARE = 'Semisquare'
SESQUISQUARE = 'Sesquisquare'
SEMISEXTILE = 'Semisextile'
QUINCUNX = 'Quincunx'
QUINTILE = 'Quintile'
BIQUINTILE = 'Biquintile'

DEFAULT_ASPECTS = (
    CONJUNCTION, OPPOSITION, SQUARE, TRINE, SEXTILE, QUINCUNX
)

ASPECTS = {
    CONJUNCTION: 0.0,
    OPPOSITION: 180.0,
    SQUARE: 90.0,
    TRINE: 120.0,
    SEXTILE: 60.0,
    SEPTILE: 51.43,
    SEMISQUARE: 45.0,
    SESQUISQUARE: 135.0,
    SEMISEXTILE: 30.0,
    QUINCUNX: 150.0,
    QUINTILE: 72.0,
    BIQUINTILE: 144.0,
}

ANGLE_ORBS = {
    CONJUNCTION: 1.0,
    OPPOSITION: 0.0,
    SQUARE: 0.0,
    TRINE: 0.0,
    SEXTILE: 0.0,
    SEPTILE: 0.0,
    SEMISQUARE: 0.0,
    SESQUISQUARE: 0.0,
    SEMISEXTILE: 0.0,
    QUINCUNX: 0.0,
    QUINTILE: 0.0,
    BIQUINTILE: 0.0,
}

PLANET_ORBS = {
    CONJUNCTION: 10.0,
    OPPOSITION: 10.0,
    SQUARE: 10.0,
    TRINE: 10.0,
    SEXTILE: 6.0,
    SEPTILE: 3.0,
    SEMISQUARE: 3.0,
    SESQUISQUARE: 3.0,
    SEMISEXTILE: 3.0,
    QUINCUNX: 3.0,
    QUINTILE: 2.0,
    BIQUINTILE: 2.0,
}

POINT_ORBS = {
    CONJUNCTION: 1.0,
    OPPOSITION: 0.0,
    SQUARE: 0.0,
    TRINE: 0.0,
    SEXTILE: 0.0,
    SEPTILE: 0.0,
    SEMISQUARE: 0.0,
    SESQUISQUARE: 0.0,
    SEMISEXTILE: 0.0,
    QUINCUNX: 0.0,
    QUINTILE: 0.0,
    BIQUINTILE: 0.0,
}

DEFAULT_ORB = 1.0
EXACT_ORB = 0.3

DEFAULT_ORBS = {
    ASC: ANGLE_ORBS,
    DESC: ANGLE_ORBS,
    MC: ANGLE_ORBS,
    IC: ANGLE_ORBS,

    SUN: PLANET_ORBS,
    MOON: PLANET_ORBS,
    MERCURY: PLANET_ORBS,
    VENUS: PLANET_ORBS,
    MARS: PLANET_ORBS,
    JUPITER: PLANET_ORBS,
    SATURN: PLANET_ORBS,
    URANUS: PLANET_ORBS,
    NEPTUNE: PLANET_ORBS,
    PLUTO: PLANET_ORBS,

    NORTH_NODE: POINT_ORBS,
    SOUTH_NODE: POINT_ORBS,
    TRUE_NORTH_NODE: POINT_ORBS,
    TRUE_SOUTH_NODE: POINT_ORBS,
    SYZYGY: POINT_ORBS,
    PARS_FORTUNA: POINT_ORBS,
    VERTEX: POINT_ORBS,
    LILITH: POINT_ORBS,
    TRUE_LILITH: POINT_ORBS,
}

ACTIVE = 'active'
PASSIVE = 'passive'

ASSOCIATE = 'associate'
DISSOCIATE = 'dissociate'

SEPARATIVE = 'separative'
EXACT = 'exact'
APPLICATIVE = 'applicative'