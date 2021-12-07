"""
    This file is part of immanuel - (C) The Rift Lab
    Author: Robert Davies (robert@theriftlab.com)

"""

import os
import swisseph

EPHE_PATH = os.path.dirname(__file__) + os.sep + 'resources' + os.sep  + 'pyswisseph'
swisseph.set_ephe_path(EPHE_PATH)