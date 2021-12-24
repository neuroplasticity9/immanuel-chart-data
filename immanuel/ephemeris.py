"""
    This file is part of immanuel - (C) The Rift Lab
    Author: Robert Davies (robert@theriftlab.com)


    This module sets the ephemeris file path(s).

"""

import os
import swisseph as swe


def set_path(path: str = None) -> None:
    ephemeris_path = f'{os.path.dirname(__file__)}{os.sep}resources{os.sep}ephemeris'

    if path:
        ephemeris_path += f';{path}'

    swe.set_ephe_path(ephemeris_path)