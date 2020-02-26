import math
import random
from game import Game
from model.helper_functions.message import message
from model.maps.map_tile import MapTile

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
        self.turns_stuck = 0

    def move(self, dx, dy):
        if self.turns_stuck > 0:
            self.turns_stuck -= 1
            message("{} can't move!".format(self.name))
            return False
        
        target_x, target_y = self.x, self.y

        # Apply env stuff
        if Game.instance.area_map.tiles[self.x][self.y].character == MapTile.WATER_CHARACTER:
            target_x, target_y = Game.instance.area_map.mutate_position_if_walkable(self.x, self.y)
            message('{} is swept away in the current!'.format(self.name))
        # move by the given amount, if the destination is not blocked
        elif Game.instance.area_map.is_walkable(self.x + dx, self.y + dy):
            target_x += dx
            target_y += dy
        
        if target_x != self.x or target_y != self.y:
            self.x = target_x
            self.y = target_y
            Game.instance.event_bus.trigger('on_entity_move', self)

            if Game.instance.area_map.is_environment_obstacle(self.x, self.y):
                Game.instance.event_bus.trigger('stepped_on_environment_obstacle', self, Game.instance.area_map.tiles[self.x][self.y])
                return True             
            else:
                return Game.instance.area_map.get_blocking_object_at(self.x, self.y)

        return False # didn't move
        
    def move_towards(self, target_x, target_y):
        if self.turns_stuck > 0:
            self.turns_stuck -= 1
            message("{} can't move!".format(self.name))
            return False

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
            Game.instance.renderer.draw_string(self.x, self.y, self.char, self.color)

    def clear(self):
        # erase the character that represents this object
        Game.instance.renderer.draw_string(self.x, self.y, ' ', self.color)

    def cleanup(self):
        if self in Game.instance.area_map.entities:
            Game.instance.area_map.entities.remove(self)
        Game.instance.event_bus.unregister(self)

    def default_death_function(self):
        self.cleanup()
        self.clear()
        self.name = ''
        self.blocks = False
