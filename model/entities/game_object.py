import math
import random
from game import Game

class GameObject:
    """
    this is a generic object: the player, a monster, an item, the stairs...
    it's always represented by a character on screen.
    """
    def __init__(self, x, y, char, name, color, blocks=False):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks = blocks

    def move(self, dx, dy):
        # move by the given amount, if the destination is not blocked
        if Game.instance.area_map.is_walkable(self.x + dx, self.y + dy):
            self.x += dx
            self.y += dy
            Game.instance.event_bus.trigger('on_entity_move', self)
        else:
            return Game.instance.area_map.get_blocking_object_at(self.x + dx, self.y + dy)

    def move_towards(self, target_x, target_y):
        # Look at whether we should move in the x-axis, and y-axis; then pick one and go.
        # copysign(1, n) is what people write for math.sign(n) (which doesn't exist in Python)
        dx = int(math.copysign(1, target_x - self.x))
        dy = int(math.copysign(1, target_y - self.y))
        
        moves = []
        if (dx != 0):
            moves.append((dx, 0))
        if (dy != 0):
            moves.append((0, dy))
        
        x, y = random.choice(moves)
        return self.move(x, y)

    def distance_to(self, other):
        # return the distance to another object
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx ** 2 + dy ** 2)

    def distance(self, x, y):
        # return the distance to some coordinates
        return math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)

    def send_to_back(self):
        # make this object be drawn first, so all others appear above it if
        # they're in the same tile.
        if self in Game.instance.area_map.entities:
            Game.instance.area_map.entities.remove(self)
        Game.instance.area_map.entities.insert(0, self)

    def draw(self):
        # only show if it's visible to the player
        if (self.x, self.y) in Game.instance.renderer.visible_tiles:
            # draw the character that represents this object at its position
            Game.instance.ui.con.draw_str(self.x, self.y, self.char, self.color)

    def clear(self):
        # erase the character that represents this object
        Game.instance.ui.con.draw_str(self.x, self.y, ' ', self.color)

    def cleanup(self):
        if self in Game.instance.area_map.entities:
            Game.instance.area_map.entities.remove(self)
        Game.instance.event_bus.unregister(self)

    def default_death_function(self):
        self.cleanup()
        self.clear()
        self.name = ''
        self.blocks = False
