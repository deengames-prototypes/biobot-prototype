class MapTile:

    # TODO: these should be the renderer's concern, not the map's.
    DARK_GROUND_COLOUR = (32, 32, 32)
    DARK_WALL_COLOUR = (48, 48, 48)
    LIGHT_GROUND_COLOUR = (128, 128, 128)
    LIGHT_WALL_COLOUR = (192, 192, 192)
    GROUND_CHARACTER = '.'
    WALL_CHARACTER = '#'

    def __init__(self):
        self.is_explored = False
        self.is_walkable = True
        self.block_sight = False
        self.convert_to_ground()

    def convert_to_wall(self, character=WALL_CHARACTER, colour=LIGHT_WALL_COLOUR, dark_colour=DARK_WALL_COLOUR):
        self.is_walkable = False
        self.block_sight = True
        self._set_character_and_colour(character, colour, dark_colour)
        
    def convert_to_ground(self, character=GROUND_CHARACTER, colour=LIGHT_GROUND_COLOUR, dark_colour=DARK_GROUND_COLOUR):
        self.is_walkable = True
        self.block_sight = False
        self._set_character_and_colour(character, colour, dark_colour)
        
    def _set_character_and_colour(self, character, colour, dark_colour):
        self.character = character
        self.colour = colour
        self.dark_colour = dark_colour