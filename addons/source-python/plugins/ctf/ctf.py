'''

    Main loading file for capture the flag.

'''

## =================== IMPORTS ======================

from .flags import Flags
from .scores import Manager

from engines.server import global_vars
from entities.datamaps import InputData
from entities.helpers import index_from_pointer
from entities.hooks import EntityCondition
from entities.hooks import EntityPreHook
from events import Event
from listeners import OnLevelInit
from listeners.tick import Delay
from memory import make_object
from players.entity import Player
from players.helpers import index_from_userid
from players.teams import teams_by_number

## ============= MANAGER GENERATION =================

score_managers = {
    'ct':   Manager('CT'),
    't':    Manager('TERRORIST'),
}

flag_manager = Flags(global_vars.map_name)

@OnLevelInit
def _on_level_init_generate_managers(*_):
    global score_managers, flag_manager
    score_managers = {
        'ct':   Manager('CT'),
        't':    Manager('TERRORIST'),
    }

    flag_manager = Flags(global_vars.map_name)

## ================ FLAG SPAWNING ===================

@Event('round_start')
def _on_round_start_spawn_flags(*_):
    flag_manager.spawn_flags()


## ================ FLAG REMOVING ===================

@Event('enter_buyzone')
def _on_enter_buy_zone(event):
    player = Player(index_from_userid(event['userid']))
    flag = flag_manager.find_by_carrier(player.index)

    if flag:
        flag_manager.on_enter_buy_zone(flag)
        score_managers[teams_by_number[player.team]].score += 3

@Event('player_death')
def _on_player_death(event):
    player = Player(index_from_userid(event['userid']))
    flag = flag_manager.find_by_carrier(player.index)

    if flag:
        flag_manager.on_carried_death(flag)
        score_managers[teams_by_number[5-player.team]].score += 1


## =================== HOOKS =======================

@EntityPreHook(EntityCondition.equals_entity_classname('prop_physics_override'), 'use')
def _on_entity_use(stack):
    entity_index = index_from_pointer(stack[0])
    player_index = make_object(InputData, stack[1]).activator.index

    flag = flag_manager.find(entity_index)
    other = flag_manager.find_by_carrier(player_index)

    if flag and not other:
        Delay(0.1, flag_manager.on_carrier_pickup, flag, Player(player_index))