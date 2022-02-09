"""
    This file is part of immanuel - (C) The Rift Lab
    Author: Robert Davies (robert@theriftlab.com)


    Defines indices for the planets and certain asteroids, as supported
    by pyswisseph. Also defines the main planets' mean daily motions in
    degrees.

"""

import swisseph as swe


SUN = swe.SUN
MOON = swe.MOON
MERCURY = swe.MERCURY
VENUS = swe.VENUS
MARS = swe.MARS
JUPITER = swe.JUPITER
SATURN = swe.SATURN
URANUS = swe.URANUS
NEPTUNE = swe.NEPTUNE
PLUTO = swe.PLUTO
CHIRON = swe.CHIRON
PHOLUS = swe.PHOLUS
CERES = swe.CERES
PALLAS = swe.PALLAS
JUNO = swe.JUNO
VESTA  = swe.VESTA

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
