import swisseph
import os

EPHE_PATH = os.path.dirname(__file__) + os.sep + 'resources' + os.sep  + 'pyswisseph'
swisseph.set_ephe_path(EPHE_PATH)