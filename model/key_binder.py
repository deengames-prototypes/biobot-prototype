from model.keys.callbacks import quit_event, mousemotion_event
from model.keys.update_manager import UpdateManager
from model.keys.key_callbacks import *
from model.keys.key_callbacks import whirlwind_callback, omnislash_callback, frost_bomb_callback, lance_charge_callback, \
    ruqya_callback


KEY_BINDINGS = {
    'ESCAPE': exit_to_main_menu_callback,
    'ENTER': enter_callback,

    'UP': up_callback,
    'DOWN': down_callback,
    'LEFT': left_callback,
    'RIGHT': right_callback,

    'g': pickup_callback,

    'i': inventory_use,
    'd': inventory_drop,

    'f': bow_callback,
    'm': mount_callback,

    'r': rest_callback,
    'R': continuous_rest_callback
}

EVENT_BINDINGS = {
    'QUIT': quit_event,

    'MOUSEMOTION': mousemotion_event,
    'MOUSEDOWN': None,
    'MOUSEUP': None,

    'KEYDOWN': None,
    'KEYUP': None,
}


def placeholder_callback(ev):
    pass


class KeyBinder:
    def __init__(self, game):
        self.game = game

    @staticmethod
    def _format_attr_key(key_name):
        return f'key_{key_name}'

    @staticmethod
    def _format_attr_event(event_name):
        return f'ev_{event_name}'

    def register_all_keybinds_and_events(self):
        self.register_all_keybinds()
        self.register_all_events()

    # Keybinds
    def register_all_keybinds(self):
        self.register_keybinds(KEY_BINDINGS)

    def suspend_all_keybinds(self):
        for key in KEY_BINDINGS.keys():
            self.suspend_keybind(key)

    def register_keybinds(self, key_callback_dict):
        """Helpful for avoiding a multiple register_keybind calls"""
        for key, callback in key_callback_dict.items():
            self.register_keybind(key, callback)

    def register_keybind(self, key, callback=None):
        callback = callback or KEY_BINDINGS.get(key) or placeholder_callback
        
        setattr(Game.instance.ui.app, self._format_attr_key(key), callback)

    def suspend_keybind(self, key):
        try:
            delattr(Game.instance.ui.app, self._format_attr_key(key))
        except AttributeError:
            pass

    # Events
    def register_all_events(self):
        for key, callback in EVENT_BINDINGS.items():
            self.register_event(key, callback)

        self.register_update()

    def register_event(self, event_name, callback=None):
        callback = callback or EVENT_BINDINGS.get(event_name) or placeholder_callback
        setattr(Game.instance.ui.app, self._format_attr_event(event_name), callback)

    # Update
    def register_update(self, new_callback=None):
        update_manager = UpdateManager(Game.instance)

        def update(delta_time):
            update_manager.base_update()
            new_callback(delta_time, update_manager)

        callback = update if new_callback is not None else update_manager.update
        setattr(Game.instance.ui.app, 'update', callback)


SKILL_KEYBINDINGS = {
    "whirlwind": {'l': whirlwind_callback},
    "omnislash": {'o': omnislash_callback},
    "frostbomb": {'h': frost_bomb_callback},
    "lanceCharge": {'j': lance_charge_callback},
    "ruqya": {'u': ruqya_callback}
}


def add_skill(skill_name):
    skill_keybind = SKILL_KEYBINDINGS.get(skill_name)
    Game.instance.keybinder.register_keybinds(skill_keybind)
