from constants import BASE_DIFFICULTY
from game import Game

class Difficulty:
    instance = None

    def __init__(self):
        Difficulty.instance = self
        self.current_difficulty = 0
        self.load()
        self._watch_events()

        # Hack for: don't decrease difficulty every env hit (because, water). Instead,
        # do it on the first time we step onto water; do nothing as we stay in; and once
        # we're ejected back onto land, if we step again on water, decrease again.
        self._was_player_on_water = False
    
    def _watch_events(self):
        Game.instance.event_bus.bind('on_entity_move', self._on_entity_move)
        Game.instance.event_bus.bind('on_entity_died', self._on_entity_died)
        Game.instance.event_bus.bind('on_descend', self._on_descend)
        Game.instance.event_bus.bind('on_trap_triggered', self._on_trap_triggered)
        Game.instance.event_bus.bind('stepped_on_environment_obstacle', self._on_environment_triggered)

    def save(self):
        with open('current_difficulty', 'w') as f:
            data = str(self.current_difficulty)
            f.writelines(data)
        with open('current_level', 'w') as f:
            data = str(Game.instance.player.level)
            f.writelines(data)
    
    def load(self):
        try:
            with open('current_difficulty', 'r') as f:
                difficulty = int(f.readline())
        except FileNotFoundError:
            difficulty = 1000
            level = 1
            self.current_difficulty = 1000
            self.save()

        self.current_difficulty = difficulty
    
    def diff_from_base(self):
        return self.current_difficulty - BASE_DIFFICULTY

    # event handlers
    def _on_entity_hurt(self, entity):
        if entity == Game.instance.player:
            # Getting hurt is always bad. Because health is low.
            # Snipe them from far, gank them with skills, etc.
            # Trading blows is OK, but no way sustainable.
            self._modify_difficulty(-1)
    
    def _on_entity_died(self, entity):
        if entity != Game.instance.player:
            self._modify_difficulty(1)
        else:
            self._modify_difficulty(-25)
    
    def _on_descend(self):
        self._modify_difficulty(10)

    def _on_trap_triggered(self, victim):
        if victim == Game.instance.player:
            self._modify_difficulty(-5)
        else:
            self._modify_difficulty(5)
    
    def _on_environment_triggered(self, victim, map_tile):
        # We know it was water.
        if victim == Game.instance.player and not self._was_player_on_water:
            self._modify_difficulty(-3)
            self._was_player_on_water = True
        # Monsters just randomly stew in it. No need to spam-up difficulty.
    
    def _on_entity_move(self, entity):
        if entity == Game.instance.player:
            if self._was_player_on_water and not Game.instance.area_map.tiles[entity.x][entity.y].is_environment_obstacle:
                self._was_player_on_water = False

    # internal methods
    def _modify_difficulty(self, amount):
        self.current_difficulty += amount
        self.save()