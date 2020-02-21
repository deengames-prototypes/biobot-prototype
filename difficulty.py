from game import Game

class Difficulty:
    instance = None

    def __init__(self):
        Difficulty.instance = self
        self.load()
        self._watch_events()
    
    def _watch_events(self):
        Game.instance.event_bus.bind('on_entity_died', self._on_entity_died)
        Game.instance.event_bus.bind('on_entity_hurt', self._on_entity_hurt)
        Game.instance.event_bus.bind('on_descend', self._on_descend)

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

    # internal methods
    def _modify_difficulty(self, amount):
        message = "increased"
        if amount < 0: message = "decreased"
        
        print("Difficulty {}: {} => {}".format(message, self.current_difficulty, self.current_difficulty + amount))
        self.current_difficulty += amount
        self.save()