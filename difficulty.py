from game import Game

class Difficulty:
    instance = None

    def __init__(self):
        Difficulty.instance = self
        self.current_difficulty = 1000

        self.watch_events()
    
    def watch_events(self):
        Game.instance.event_bus.bind('on_entity_died', self._on_entity_died)
        Game.instance.event_bus.bind('on_entity_hurt', self._on_entity_hurt)

    def save(self):
        with open('current_difficulty', 'w') as f:
            data = str(self.current_difficulty)
            f.writelines(data)

    # event handlers
    def _on_entity_hurt(self, entity):
        pass
    
    def _on_entity_died(self, entity):
        if entity != Game.instance.player:
            self._modify_difficulty(1)
    
    # internal methods
    def _modify_difficulty(self, amount):
        message = "increased"
        if amount < 0: message = "decreased"
        
        print("Difficulty {}: {} => {}".format(message, self.current_difficulty, self.current_difficulty + amount))
        self.current_difficulty += amount
        self.save()