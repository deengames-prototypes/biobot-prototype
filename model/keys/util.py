from constants import DELTA_UP, DELTA_DOWN, DELTA_LEFT, DELTA_RIGHT
from game import Game
from model.keys.decorators import in_game


def map_movement_callback(callback):
    @in_game(pass_turn=True)
    def new_up(event):
        callback(*DELTA_UP)

    @in_game(pass_turn=True)
    def new_down(event):
        callback(*DELTA_DOWN)

    @in_game(pass_turn=True)
    def new_left(event):
        callback(*DELTA_LEFT)

    @in_game(pass_turn=True)
    def new_right(event):
        callback(*DELTA_RIGHT)

    Game.instance.keybinder.register_keybinds({
        'UP': new_up,
        'DOWN': new_down,
        'LEFT': new_left,
        'RIGHT': new_right,
    })