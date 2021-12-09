"""
    This file is part of immanuel - (C) The Rift Lab
    Author: Robert Davies (robert@theriftlab.com)

"""

import os
import swisseph as swe

EPHE_PATH = os.path.dirname(__file__) + os.sep + 'resources' + os.sep  + 'pyswisseph'
swe.set_ephe_path(EPHE_PATH)