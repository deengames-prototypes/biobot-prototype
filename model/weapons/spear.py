import math

from model.weapons.base import Weapon
from model.config import config


class Spear(Weapon):
    def attack(self, target, game, **kwargs):
        if not kwargs.get('recurse', True):
            return

        dx = (target.x - self.owner.x) * config.data.weapons.spear.pierceRange
        dy = (target.y - self.owner.y) * config.data.weapons.spear.pierceRange

        if dx == 0:
            affected_tiles = [
                (self.owner.x, self.owner.y + y)
                for y in range(0, dy, int(math.copysign(1, dy)))
            ]
        else:
            affected_tiles = [
                (self.owner.x + x, self.owner.y)
                for x in range(0, dx, int(math.copysign(1, dx)))
            ]

        owner_fighter = game.fighter_system.get(self.owner)

        for tile in affected_tiles:
            obj = game.area_map.get_blocking_object_at(*tile)
            if (obj is not None
                    and obj is not target
                    and game.fighter_system.has(obj)
                    and game.fighter_system.get(obj).hostile):
                owner_fighter.attack(obj, recurse=False)
