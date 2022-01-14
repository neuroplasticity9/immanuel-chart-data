"""
    This file is part of immanuel - (C) The Rift Lab
    Author: Robert Davies (robert@theriftlab.com)


    This module defines constants for chart object & aspect data.

"""

import swisseph as swe


""" Chart types. """

DIURNAL = 'diurnal'
NOCTURNAL = 'nocturnal'


""" Chart item types. """

HOUSE = 'house'
ANGLE = 'angle'
PLANET = 'planet'
POINT = 'point'
ASTEROID = 'asteroid'
FIXED_STAR = 'fixed star'


""" Signs. """

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


""" House systems. """

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


""" Main angles. """

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


""" Planets. """

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


""" Moon phases & their end positions relative to the Sun. """

NEW_MOON = 'new_moon'
WAXING_CRESCENT = 'waxing_crescent'
FIRST_QUARTER = 'first_quarter'
WAXING_GIBBOUS = 'waxing_gibbous'
FULL_MOON = 'full_moon'
DISSEMINATING = 'disseminating'
THIRD_QUARTER = 'third_quarter'
BALSAMIC = 'balsamic'

MOON_PHASES = {
    NEW_MOON: 45,
    WAXING_CRESCENT: 90,
    FIRST_QUARTER: 135,
    WAXING_GIBBOUS: 180,
    FULL_MOON: 225,
    DISSEMINATING: 270,
    THIRD_QUARTER: 315,
    BALSAMIC: 360,
}


""" Points. """

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


""" Main asteroids available without extra ephemeris files. """

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


""" Default items to return. """

DEFAULT_ITEMS = [
    ASC, DESC, MC, IC,
    SUN, MOON, MERCURY, VENUS, MARS, JUPITER, SATURN, URANUS, NEPTUNE, PLUTO,
    NORTH_NODE, SOUTH_NODE, PARS_FORTUNA, VERTEX,
    CHIRON
]


""" All available items. """

CHART_ITEMS = {
    **ANGLES,
    **PLANETS,
    **POINTS,
    **ASTEROIDS,
}


""" Astrological constants. """

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


""" Movement & motion. """

RETROGRADE = 'retrograde'
STATION = 'station'
DIRECT = 'direct'

SLOW = 'slow'
FAST = 'fast'


""" Main essential dignities """

DOMICILE = 'domicile'
EXALTED = 'exalted'
DETRIMENT = 'detriment'
FALL = 'fall'
FACE_RULER = 'face_ruler'
TERM_RULER = 'term_ruler'
TRIPLICITY_RULER = 'triplicity_ruler'

ESSENTIAL_DIGNITIES = {
    ARIES: {
        DOMICILE: MARS,
        EXALTED: SUN,
        DETRIMENT: VENUS,
        FALL: SATURN,
        TRIPLICITY_RULER: (SUN, JUPITER, SATURN),
        FACE_RULER: (MARS, SUN, VENUS),
        TERM_RULER: {
            JUPITER: (0, 6),
            VENUS: (6, 12),
            MERCURY: (12, 20),
            MARS: (20, 25),
            SATURN: (25, 30),
        },
    },
    TAURUS: {
        DOMICILE: VENUS,
        EXALTED: MOON,
        DETRIMENT: PLUTO,
        FALL: URANUS,
        TRIPLICITY_RULER: (VENUS, MOON, MARS),
        FACE_RULER: (MERCURY, MOON, SATURN),
        TERM_RULER: {
            VENUS: (0, 8),
            MERCURY: (8, 14),
            JUPITER: (14, 22),
            SATURN: (22, 27),
            MARS: (27, 30),
        },
    },
    GEMINI: {
        DOMICILE: MERCURY,
        EXALTED: (),
        DETRIMENT: JUPITER,
        FALL: (),
        TRIPLICITY_RULER: (SATURN, MERCURY, JUPITER),
        FACE_RULER: (JUPITER, MARS, SUN),
        TERM_RULER: {
            MERCURY: (0, 6),
            JUPITER: (6, 12),
            VENUS: (12, 17),
            MARS: (17, 24),
            SATURN: (24, 30),
        },
    },
    CANCER: {
        DOMICILE: MOON,
        EXALTED: JUPITER,
        DETRIMENT: SATURN,
        FALL: MARS,
        TRIPLICITY_RULER: (VENUS, MARS, MOON),
        FACE_RULER: (VENUS, MERCURY, MOON),
        TERM_RULER: {
            MARS: (0, 7),
            VENUS: (7, 13),
            MERCURY: (13, 19),
            JUPITER: (19, 26),
            SATURN: (26, 30),
        },
    },
    LEO: {
        DOMICILE: SUN,
        EXALTED: NEPTUNE,
        DETRIMENT: URANUS,
        FALL: (),
        TRIPLICITY_RULER: (SUN, JUPITER, SATURN),
        FACE_RULER: (SATURN, JUPITER, MARS),
        TERM_RULER: {
            JUPITER: (0, 6),
            VENUS: (6, 11),
            SATURN: (11, 18),
            MERCURY: (18, 24),
            MARS: (24, 30),
        },
    },
    VIRGO: {
        DOMICILE: MERCURY,
        EXALTED: (MERCURY, PLUTO),
        DETRIMENT: NEPTUNE,
        FALL: VENUS,
        TRIPLICITY_RULER: (VENUS, MOON, MARS),
        FACE_RULER: (SUN, VENUS, MERCURY),
        TERM_RULER: {
            MERCURY: (0, 7),
            VENUS: (7, 17),
            JUPITER: (17, 21),
            MARS: (21, 28),
            SATURN: (28, 30),
        },
    },
    LIBRA: {
        DOMICILE: VENUS,
        EXALTED: SATURN,
        DETRIMENT: MARS,
        FALL: SUN,
        TRIPLICITY_RULER: (SATURN, MERCURY, JUPITER),
        FACE_RULER: (MOON, SATURN, JUPITER),
        TERM_RULER: {
            SATURN: (0, 6),
            MERCURY: (6, 14),
            JUPITER: (14, 21),
            VENUS: (21, 28),
            MARS: (28, 30),
        },
    },
    SCORPIO: {
        DOMICILE: (MARS, PLUTO),
        EXALTED: URANUS,
        DETRIMENT: (),
        FALL: MOON,
        TRIPLICITY_RULER: (VENUS, MARS, MOON),
        FACE_RULER: (MARS, SUN, VENUS),
        TERM_RULER: {
            MARS: (0, 7),
            VENUS: (7, 11),
            MERCURY: (11, 19),
            JUPITER: (19, 24),
            SATURN: (24, 30),
        },
    },
    SAGITTARIUS: {
        DOMICILE: JUPITER,
        EXALTED: (),
        DETRIMENT: MERCURY,
        FALL: (),
        TRIPLICITY_RULER: (SUN, JUPITER, SATURN),
        FACE_RULER: (MERCURY, MOON, SATURN),
        TERM_RULER: {
            JUPITER: (0, 12),
            VENUS: (12, 17),
            MERCURY: (17, 21),
            SATURN: (21, 26),
            MARS: (26, 30),
        },
    },
    CAPRICORN: {
        DOMICILE: SATURN,
        EXALTED: MARS,
        DETRIMENT: MOON,
        FALL: JUPITER,
        TRIPLICITY_RULER: (VENUS, MOON, MARS),
        FACE_RULER: (JUPITER, MARS, SUN),
        TERM_RULER: {
            MERCURY: (0, 7),
            JUPITER: (7, 14),
            VENUS: (14, 22),
            SATURN: (22, 26),
            MARS: (26, 30),
        },
    },
    AQUARIUS: {
        DOMICILE: (SATURN, URANUS),
        EXALTED: (),
        DETRIMENT: SUN,
        FALL: NEPTUNE,
        TRIPLICITY_RULER: (SATURN, MERCURY, JUPITER),
        FACE_RULER: (VENUS, MERCURY, MOON),
        TERM_RULER: {
            MERCURY: (0, 7),
            VENUS: (7, 13),
            JUPITER: (13, 20),
            MARS: (20, 25),
            SATURN: (25, 30),
        },
    },
    PISCES: {
        DOMICILE: (JUPITER, NEPTUNE),
        EXALTED: VENUS,
        DETRIMENT: (),
        FALL: (MERCURY, PLUTO),
        TRIPLICITY_RULER: (VENUS, MARS, MOON),
        FACE_RULER: (SATURN, JUPITER, MARS),
        TERM_RULER: {
            VENUS: (0, 12),
            JUPITER: (12, 16),
            MERCURY: (16, 19),
            MARS: (19, 28),
            SATURN: (28, 30),
        },
    },
}

DIGNITY_SCORES = {
    DOMICILE: 5,
    EXALTED: 4,
    TRIPLICITY_RULER: 3,
    TERM_RULER: 2,
    FACE_RULER: 1,
    FALL: -4,
    DETRIMENT: -5,
}


""" Aspects. """

ASSOCIATE = 'associate'
DISSOCIATE = 'dissociate'

APPLICATIVE = 'applicative'
EXACT = 'exact'
SEPARATIVE = 'separative'

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

MAJOR_ASPECTS = (
    CONJUNCTION, OPPOSITION, SQUARE, TRINE, SEXTILE
)

MINOR_ASPECTS = (
    SEPTILE, SEMISQUARE, SESQUISQUARE, SEMISEXTILE, QUINCUNX, QUINTILE, BIQUINTILE
)

ALL_ASPECTS = MAJOR_ASPECTS + MINOR_ASPECTS

DEFAULT_ASPECTS = (*MAJOR_ASPECTS, QUINCUNX)


""" Rules for which items can initiate and receive which aspects. """

INITIATE = 'initiate'
RECEIVE = 'receive'

DEFAULT_ASPECT_RULE = {
    INITIATE: ALL_ASPECTS,
    RECEIVE: ALL_ASPECTS,
}

PLANET_ASPECT_RULE = {
    INITIATE: ALL_ASPECTS,
    RECEIVE: ALL_ASPECTS,
}

POINT_ASPECT_RULE = {
    INITIATE: (CONJUNCTION,),
    RECEIVE: ALL_ASPECTS,
}

DEFAULT_ASPECT_RULES = {
    ASC: POINT_ASPECT_RULE,
    DESC: POINT_ASPECT_RULE,
    MC: POINT_ASPECT_RULE,
    IC: POINT_ASPECT_RULE,

    SUN: PLANET_ASPECT_RULE,
    MOON: PLANET_ASPECT_RULE,
    MERCURY: PLANET_ASPECT_RULE,
    VENUS: PLANET_ASPECT_RULE,
    MARS: PLANET_ASPECT_RULE,
    JUPITER: PLANET_ASPECT_RULE,
    SATURN: PLANET_ASPECT_RULE,
    URANUS: PLANET_ASPECT_RULE,
    NEPTUNE: PLANET_ASPECT_RULE,
    PLUTO: PLANET_ASPECT_RULE,

    NORTH_NODE: POINT_ASPECT_RULE,
    SOUTH_NODE: POINT_ASPECT_RULE,
    TRUE_NORTH_NODE: POINT_ASPECT_RULE,
    TRUE_SOUTH_NODE: POINT_ASPECT_RULE,
    SYZYGY: POINT_ASPECT_RULE,
    PARS_FORTUNA: POINT_ASPECT_RULE,
    VERTEX: POINT_ASPECT_RULE,
    LILITH: POINT_ASPECT_RULE,
    TRUE_LILITH: POINT_ASPECT_RULE,
}


""" Orbs. """

DEFAULT_ORB = 1.0
EXACT_ORB = 0.3

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
    CONJUNCTION: 0.0,
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

DEFAULT_ORBS = {
    ASC: PLANET_ORBS,
    DESC: PLANET_ORBS,
    MC: PLANET_ORBS,
    IC: PLANET_ORBS,

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
