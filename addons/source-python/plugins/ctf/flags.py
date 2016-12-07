'''

    Flag entity manager. Controls all
    flag interaction with players.

'''

## =============== ALL DECLARTION ===================

__all__ = (
    'Flags'
)

## =================== IMPORTS ======================

from .maps import get_flag_locations_from_map

from colors import Color
from entities.entity import Entity

## ============== FLAGS DECLARTION ==================

class Flags(dict):
    """
    Flags dictionary to manage all flags on a specific map.

    :param str mapname:
    """

    PICKUP_MODEL = None
    STATIONARY_MODEL = None
    EFFECT_MATERIAL = None

    def __init__(self, mapname, *args):
        "Initiate the Flags dictionary and generate all flag locations for the map."
        super().__init__(*args)

        for vector in get_flag_locations_from_map(mapname):
            self.add_flag(vector)

    def clear(self):
        "Cycle through all available flags, killing each one, and removing them."
        for vector, flag in self.values():
            if flag:
                flag.remove()
            del self[vector]

    def find(self, index):
        "Find a flags entity instance from its current index."
        for vector in self:
            if self[vector] and self[vector].index == index:
                return self[vector]
        return None

    def find_by_carrier(self, index):
        "Find a flags entity instance from its current carrier index."
        for vector in self:
            if self[vector] and index == self[vector].carrier.index:
                return self[vector]
        return None

    def add_flag(self, vector):
        "Add a flag vector location to the dictionary for further usage."
        self[vector] = None

    def spawn_flag(self, vector):
        "Spawn a flag onto the map from a vector instance."
        # Creating a flag prop.
        flag = Entity.create('prop_physics_override')
        flag.origin = vector
        flag.model = Flags.STATIONARY_MODEL
        flag.spawn_flags = 265
        flag.carrier = None
        flag.home = vector
        flag.spawn()

        # Simple Effect to mark Flags.
        entity = Entity.create('env_smokestack')
        entity.teleport(vector, None, None)
        entity.base_spread = 10
        entity.spread_speed = 75
        entity.initial_state = 0
        entity.speed = 105
        entity.rate = 100
        entity.start_size = 8
        entity.end_size = 4
        entity.twist = 360
        entity.jet_length = 100
        entity.render_mode = 18
        entity.render_amt = 100
        entity.render_color = Color(3, 5, 253)
        entity.add_output('SmokeMaterial {}'.format(Flags.EFFECT_MATERIAL))
        entity.turn_on()
        entity.set_parent(self[vector].pointer, -1)

        flag.effect = entity

        self[vector] = flag

    def spawn_flags(self):
        "Spawns all flags onto the map that exist in the dictionary."
        for vector in self:
            self.spawn_flag(vector)

    def on_round_start(self):
        "Called upon round start, and spawns all flags."
        self.spawn_flags()

    def on_round_end(self):
        "Called upon round end, and redefines all flags."
        for vector in self:
            self[vector] = None

    def on_enter_buy_zone(self, flag):
        "Called upon entering the buyzone, and respawns the flag home."
        flag.remove()
        self.spawn_flag(flag.home)

    def on_carrier_death(self, flag):
        "Called upon a carrier dying, and respawns the flag home."
        flag.remove()
        self.spawn_flag(flag.home)

    def on_carrier_pickup(self, flag, player):
        "Called upon a player picking up a flag."
        flag.carrier = player
        flag.origin = player.origin
        flag.set_parent(player.pointer, -1)
        flag.model = Flag.PICKUP_MODEL