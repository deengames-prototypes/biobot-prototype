from functools import wraps

import colors
from game import Game
from model.helper_functions.message import message
from model.helper_functions.skills import can_use_horse_skill, can_use_skill


def in_game(callback=None, *, pass_turn=False):
    """
    Decorator for ensuring in-game access only
    Also marks the current turn as passed.
    """
    def decorator(callback):
        @wraps(callback)
        def _inner_function(event):
            if Game.instance.game_state == 'playing' and Game.instance.current_turn is Game.instance.player:
                if pass_turn:
                    Game.instance.current_turn = None
                callback(event)

        return _inner_function

    if callback is None:
        return decorator
    else:
        return decorator(callback)


def skill(callback=None, *, cost=0):
    def decorator(callback):
        @wraps(callback)
        def _inner_function(event):
            if can_use_skill(cost):
                callback(event)
            else:
                message(f"Not enough skill points to use skill!", colors.dark_red)

        return _inner_function

    if callback is None:
        return decorator
    else:
        return decorator(callback)


def horse_skill(callback=None, *, cost=0):
    def decorator(callback):
        @wraps(callback)
        def _inner_function(event):
            if can_use_horse_skill(cost):
                if Game.instance.stallion.is_mounted:
                    callback(event)
                else:
                    message("You can only use this skill on a horse!", colors.dark_red)
            else:
                message("Not enough skill points to use skill!", colors.dark_red)

        return _inner_function

    if callback is None:
        return decorator
    else:
        return decorator(callback)
