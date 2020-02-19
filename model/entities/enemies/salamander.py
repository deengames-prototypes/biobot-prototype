from game import Game
from model.entities.fire import Fire
from model.entities.game_object import GameObject
from model.config import config


class Salamander(GameObject):
    def __init__(self, x, y, char, name, color, blocks=False):
        super().__init__(x, y, char, name, color, blocks=blocks)

        Game.instance.event_bus.bind('on_turn_pass', self.on_turn_passed, self)

    def on_turn_passed(self):
        if config.data.enemies.salamander.shootsFire:
            self.spawn_fire()

    def spawn_fire(self):
        tile = Game.instance.area_map.get_walkable_tile_around(self.x, self.y, config.data.enemies.salamander.fireRange)
        if tile is not None:
            Game.instance.area_map.entities.append(Fire(*tile))
