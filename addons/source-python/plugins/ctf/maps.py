'''

	Flag location manager, which will
	decide where to spawn the flag upon
	round start.

'''

## =============== ALL DECLARTION ===================

__all__ = (
	'get_flag_locations_from_map',
)

## ============== OBTAIN MAP FLAGS ==================

from configparser import ConfigParser
from paths import PLUGIN_PATH
from mathlib import Vector

parser = ConfigParser()
parser.read(PLUGIN_PATH / 'ctf' / 'locations.ini')

def get_flag_locations_from_map(mapname):
    if mapname in parser:
    	for location in parser.options(mapname):
    		yield Vector(*map(float, parser.get(mapname, location).split(',')))