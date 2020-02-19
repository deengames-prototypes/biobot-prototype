from game import Game
from model.helper_functions.message import message
from model.components.base import Component


class XPComponent(Component):
    def __init__(self, owner, level=1, xp=0, on_level_callback=None, xp_required_base=1):
        super().__init__(owner)
        self.level = level
        self.xp = xp
        self.on_level_callback = on_level_callback
        self.xp_required_base = xp_required_base

    def _xp_next_level(self):
        return 2 ** (self.level + 1) * self.xp_required_base

    def gain_xp(self, amount):
        self.xp += amount
        # XP doubles every level. 40, 80, 160, ...
        # First level = after four orcs. Yeah, low standards.
        # DRY ya'ne
        while self.xp >= self._xp_next_level():
            self.level += 1
            if self.on_level_callback is not None:
                self.on_level_callback(self.level)
            message(f"{self.owner.name.capitalize()} is now level {self.level}!")
            fighter = Game.instance.fighter_system.get(self.owner)
            fighter.heal(fighter.max_hp)
