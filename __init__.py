from rich import print

settings = {}
settings['combat_seconds'] = 165
settings['per_second'] = 0.1
settings['iterations'] = 20
settings['execute_range'] = 20
settings['latency'] = 0

from classes.actions import *
from structs import *
from armory import *

from classes.hitTable import *

from cooldowns import *
from enchants import *
from buffs import *
from procs import *
from abilities import *
from character import *
from target import *
from functions import *