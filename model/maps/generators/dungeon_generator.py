from game import Game
from model.rect import Rect
from model.maps.generators import map_generator


class DungeonGenerator:
    """
    Generates a multi-room dungeon map in entirety, by mutating map tiles.
    Includes population of monsters, map items, etc.
    """

    NUM_ROOMS = (15, 30)
    ROOM_MAX_SIZE = 10
    ROOM_MIN_SIZE = 6
    NUM_ITEMS = (10, 20)
    NUM_MONSTERS = (30, 40)

    def __init__(self, area_map):
        self._rooms = []
        self._area_map = area_map

    def generate(self):
        self._generate_rooms()

        map_generator.generate_monsters(self._area_map,
            Game.instance.random.randint(*DungeonGenerator.NUM_ROOMS))
        map_generator.generate_items(self._area_map,
            Game.instance.random.randint(*DungeonGenerator.NUM_ITEMS))

    def _generate_rooms(self):
        # TODO: dry this block with forest generator
        for x in range(0, self._area_map.width):
            for y in range(0, self._area_map.height):
                self._area_map.tiles[x][y].convert_to_wall()

        rooms_to_generate = Game.instance.random.randint(*DungeonGenerator.NUM_ROOMS)

        # If you generate a room overlapping another room, that's a fail.
        # After ten failures, we give up and return the dungeon as-is.
        num_failures = 10

        while rooms_to_generate and num_failures:
            # random width and height
            w = Game.instance.random.randint(DungeonGenerator.ROOM_MIN_SIZE, DungeonGenerator.ROOM_MAX_SIZE)
            h = Game.instance.random.randint(DungeonGenerator.ROOM_MIN_SIZE, DungeonGenerator.ROOM_MAX_SIZE)
            # random position without going out of the boundaries of the map
            x = Game.instance.random.randint(0, self._area_map.width - w - 1)
            y = Game.instance.random.randint(0, self._area_map.height - h - 1)

            # "Rect" class makes rectangles easier to work with
            new_room = Rect(x, y, w, h)

            # run through the other rooms and see if they intersect with this one
            failed = False
            for other_room in self._rooms:
                if new_room.intersect(other_room):
                    failed = True
                    num_failures -= 1
                    break

            if not failed:
                # this means there are no intersections, so this room is valid

                # "paint" it to the map's tiles
                self._create_room(new_room)
                rooms_to_generate -= 1

                # center coordinates of new room, will be useful later
                (new_x, new_y) = new_room.center()

                if len(self._rooms) == 0:
                    # this is the first room, where the player starts at
                    Game.instance.player.x = new_x
                    Game.instance.player.y = new_y

                else:
                    # all rooms after the first:
                    # connect it to the previous room with a tunnel

                    # center coordinates of previous room
                    (prev_x, prev_y) = self._rooms[len(self._rooms) - 1].center()

                    # draw a coin (random number that is either 0 or 1)
                    if Game.instance.random.randint(0, 1):
                        # first move horizontally, then vertically
                        self._create_h_tunnel(prev_x, new_x, prev_y)
                        self._create_v_tunnel(prev_y, new_y, new_x)
                    else:
                        # first move vertically, then horizontally
                        self._create_v_tunnel(prev_y, new_y, prev_x)
                        self._create_h_tunnel(prev_x, new_x, new_y)

                # finally, append the new room to the list
                self._rooms.append(new_room)

    def _create_room(self, room):
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self._area_map.tiles[x][y].convert_to_ground()

    def _create_h_tunnel(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self._area_map.tiles[x][y].convert_to_ground()

    def _create_v_tunnel(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self._area_map.tiles[x][y].convert_to_ground()
