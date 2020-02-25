from constants import DELTA_UP, DELTA_DOWN, DELTA_LEFT, DELTA_RIGHT
from game import Game
from model.maps.map_tile import MapTile
from model.rect import Rect

import math

class AreaMap:
    def __init__(self, width, height, floor_num=0):
        self.tiles = []
        self.entities = []
        self.width = width
        self.height = height
        self.next_floor_stairs = (None, None)
        #self.previous_floor_stairs = (None, None)
        self.floor_num = floor_num

        # Create a 2D structure of tiles
        for x in range(0, self.width):
            self.tiles.append([])
            for y in range(0, self.height):
                self.tiles[x].append(MapTile())

    def is_on_map(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def get_entities_on(self, x, y):
        return [
            e
            for e in self.entities
            if (e.x, e.y) == (x, y)
        ]

    def is_walkable(self, x, y):
        return (self.is_on_map(x, y)
                and self.tiles[x][y].is_walkable
                and len([
                            e
                            for e in self.get_entities_on(x, y)
                            if e.blocks
                        ]) == 0)

    def is_visible_tile(self, x, y):
        return self.is_on_map(x, y) and not self.tiles[x][y].block_sight

    def get_random_tile(self):
        return Game.instance.random.randint(0, self.width), Game.instance.random.randint(0, self.height)

    def get_random_walkable_tile(self):
        while True:
            x, y = self.get_random_tile()
            if self.is_walkable(x, y):
                return x, y

    def get_random_nonwalkable_tile(self):
        while True:
            x, y = self.get_random_tile()
            if not self.is_walkable(x, y):
                return x, y

    def place_on_random_ground(self, entity):
        x, y = self.get_random_walkable_tile()

        entity.x = x
        entity.y = y
        self.entities.append(entity)

        return self.entities.index(entity)

    def get_walkable_tile_within(self, rect):
        all_tiles_around_range = [
            (tile_x, tile_y)
            for tile_x in range(rect.x1, rect.x2)
            for tile_y in range(rect.y1, rect.y2)
            if self.is_walkable(tile_x, tile_y)
        ]

        if all_tiles_around_range:
            tile = Game.instance.random.choice(all_tiles_around_range)
            return tile
        else:
            return None

    def get_walkable_tile_around(self, x, y, range_num):
        """
        returns a walkable tile in given range "around" x, y.
        tries to return closest tile there is.
        """
        already_processed = set()

        for delta in range(range_num):
            for width_range in range(-delta, delta):
                for height_range in range(-delta, delta):
                    if (width_range, height_range) not in already_processed:
                        already_processed.add((width_range, height_range))
                        rect = Rect(x, y, width_range, height_range)
                        tile = self.get_walkable_tile_within(rect)
                        if tile is not None:
                            return tile

        return None

    def get_nonwalkable_tiles_around(self, center_x, center_y, range_num):
        to_return = []
        for r2 in range(-range_num, range_num):
            for r1 in range(-range_num, range_num):
                x = center_x + r1
                y = center_y + r2
                if x >= 0 and y >= 0 and x < self.width and y < self.height and math.sqrt(((center_x - x) ** 2) + ((center_y - y) ** 2)) <= range_num:
                    to_return.append([x, y])

        return to_return

    def place_around(self, entity, x, y):
        tile = self.get_walkable_tile_around(x, y, min(self.width, self.height))

        entity.x = tile[0]
        entity.y = tile[1]
        self.entities.append(entity)

        return self.entities.index(entity)

    def get_blocking_object_at(self, x, y):
        for obj in self.entities:
            if obj.blocks and (obj.x, obj.y) == (x, y):
                return obj

        return None

    def mutate_position_if_walkable(self, x, y):
        adjacent_tiles = [
            (x + x_offset, y + y_offset)
            for x_offset, y_offset in (DELTA_UP, DELTA_DOWN, DELTA_LEFT, DELTA_RIGHT)
        ]
        Game.instance.random.shuffle(adjacent_tiles)

        for tile_x, tile_y in adjacent_tiles:
            if self.is_walkable(tile_x, tile_y):
                return tile_x, tile_y

        return None


def filter_tiles(tiles, filter_callback):
    return [
        (x, y)
        for x, y in tiles
        if filter_callback(x, y)
    ]
