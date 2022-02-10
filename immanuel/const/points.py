"""
    This file is part of immanuel - (C) The Rift Lab
    Author: Robert Davies (robert@theriftlab.com)


    Defines indices for the calculated points.

"""

import swisseph as swe

from immanuel.const import defaults


NORTH_NODE = swe.MEAN_NODE
SOUTH_NODE = swe.MEAN_NODE + defaults.CALCULATED_OFFSET
TRUE_NORTH_NODE = swe.TRUE_NODE
TRUE_SOUTH_NODE = swe.TRUE_NODE + defaults.CALCULATED_OFFSET
VERTEX = swe.VERTEX
LILITH = swe.MEAN_APOG
TRUE_LILITH = swe.OSCU_APOG
SYZYGY = 111
PARS_FORTUNA = 222
