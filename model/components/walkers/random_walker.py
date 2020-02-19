class RandomWalker:
    """Walks randomly. Does this by mutating the parent entity's x/y coordinates."""
    def __init__(self, area_map, parent):
        self.area_map = area_map
        self.parent = parent

    def walk(self):
        tile = self.area_map.mutate_position_if_walkable(self.parent.x, self.parent.y)
        if tile is not None:
            self.parent.x, self.parent.y = tile
