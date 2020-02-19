from game import Game
from model.entities.game_object import GameObject
from model.item import Item


def create_item(x, y, character, name, color, use_function=None):

    item_obj = GameObject(x, y, character, name, color)
    Game.instance.item_system.set(
        item_obj, Item(
            owner=item_obj,
            use_function=use_function
        )
    )

    return item_obj
