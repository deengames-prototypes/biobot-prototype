from model.event.event_bus import EventBus
from model.systems.system import ComponentSystem
import random

class Game:
    instance = None
    _dont_pickle = {'ui', 'save_manager', 'keybinder', 'renderer'}

    def __init__(self):
        Game.instance = self

        self.inventory = []
        self.draw_bowsight = None
        self.mouse_coord = (0, 0)
        self.auto_target = None
        self.target = None
        self.game_messages = []
        self.game_state = None

        self.area_map = None
        self.renderer = None
        self.ui = None
        self.current_turn = None

        self.save_manager = None
        self.keybinder = None

        self.fighter_system = ComponentSystem()
        self.ai_system = ComponentSystem()
        self.xp_system = ComponentSystem()
        self.skill_system = ComponentSystem()
        self.item_system = ComponentSystem()

        self.player = None
        self.stallion = None

        self.random = random.Random()
        self.floors = []
        self.event_busses = []
        self.current_floor = 1

        self.event_bus = EventBus()
