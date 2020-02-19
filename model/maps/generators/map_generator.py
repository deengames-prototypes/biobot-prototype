from game import Game
from model.entities.enemies.salamander import Salamander
from model.entities.game_object import GameObject
from model.helper_functions import item_callbacks
from model.config import config
from model.factories import item_factory
from model.factories import monster_factory
import palette


def generate_monsters(area_map, num_monsters):
    enemies = [
        ('bushslime', config.data.enemies.bushslime, palette.dark_green, GameObject),
        ('steelhawk', config.data.enemies.steelhawk, palette.blue, GameObject),
        ('tigerslash', config.data.enemies.tigerslash, palette.orange, GameObject),
        ('salamander', config.data.enemies.salamander, palette.red, Salamander)
    ]
    probabilities = [
        45,
        30,
        25,
        10
    ]

    for i in range(num_monsters):
        # choose random spot for this monster
        x, y = area_map.get_random_walkable_tile()
        name, data, colour, cls = Game.instance.random.choices(enemies, weights=probabilities)[0]

        monster = monster_factory.create_monster(data, x, y, colour, name, cls)
        area_map.entities.append(monster)


def generate_items(area_map, num_items):
    items = [
        ('!', 'healing potion', palette.pink, item_callbacks.cast_heal),
        ('$', 'skill potion', palette.pink, item_callbacks.restore_skill_points),
        ('#', 'scroll of lightning bolt', palette.yellow, item_callbacks.cast_lightning),
        ('#', 'scroll of fireball', palette.yellow, item_callbacks.cast_fireball),
        ('#', 'scroll of confusion', palette.yellow, item_callbacks.cast_confuse)
    ]
    probabilities = [
        35,
        35,
        10,
        10,
        10
    ]

    for i in range(num_items):
        # choose random spot for this item
        x, y = area_map.get_random_walkable_tile()
        char, name, color, use_func = Game.instance.random.choices(items, weights=probabilities)[0]

        item = item_factory.create_item(x, y, char, name, color, use_func)

        area_map.entities.append(item)
        item.send_to_back()  # items appear below other objects
