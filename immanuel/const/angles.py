"""
    This file is part of immanuel - (C) The Rift Lab
    Author: Robert Davies (robert@theriftlab.com)


    Defines indices for the main chart angles.

"""

import swisseph as swe

from immanuel.const import defaults


ASC = swe.ASC
DESC = swe.ASC + defaults.CALCULATED_OFFSET
MC = swe.MC
IC = swe.MC + defaults.CALCULATED_OFFSET
