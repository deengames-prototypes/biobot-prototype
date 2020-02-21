from constants import POISON_TRAP_TURNS
import palette
from game import Game
from model.entities.game_object import GameObject
from model.helper_functions.message import message

class Trap(GameObject):
    """
    a trap that can be stepped on, at your peril!
    """
    def __init__(self, x, y, char, name, color, trap_function=None):
        super().__init__(x, y, char, name, color)
        self.trap_function = trap_function
        Game.instance.event_bus.bind('on_entity_move', self.on_entity_move, self)

    def on_entity_move(self, entity):
        if (entity.x, entity.y) == (self.x, self.y):
            fighter = Game.instance.fighter_system.get(entity)
            if fighter != None:
                self.trap_function(entity)
                Game.instance.event_bus.trigger('on_trap_triggered', entity)

