from game import Game

class Difficulty:
    instance = None

    def __init__(self):
        Difficulty.instance = self
        self.current_difficulty = 0
        self.load()
        self._watch_events()
    
    def _watch_events(self):
        Game.instance.event_bus.bind('on_entity_died', self._on_entity_died)
        Game.instance.event_bus.bind('on_entity_hurt', self._on_entity_hurt)
        Game.instance.event_bus.bind('on_descend', self._on_descend)
        Game.instance.event_bus.bind('on_trap_triggered', self._on_trap_triggered)
        Game.instance.event_bus.bind('stepped_on_environment_obstacle', self._on_environment_triggered)

    def save(self):
        with open('current_difficulty', 'w') as f:
            data = str(self.current_difficulty)
            f.writelines(data)
    
    def load(self):
        with open('current_difficulty', 'r') as f:
            difficulty = int(f.readline())

        self.current_difficulty = difficulty
        print("Loaded; difficulty is {}".format(self.current_difficulty))

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
    
    def _on_descend(self):
        self._modify_difficulty(10)

    def _on_trap_triggered(self, victim):
        if victim == Game.instance.player:
            self._modify_difficulty(-5)
        else:
            self._modify_difficulty(5)
    
    def _on_environment_triggered(self, victim, map_tile):
        if victim == Game.instance.player:
            self._modify_difficulty(-3)
        # Monsters just randomly stew in it. No need to spam-up difficulty.

    # internal methods
    def _modify_difficulty(self, amount):
        self.current_difficulty += amount
        self.save()