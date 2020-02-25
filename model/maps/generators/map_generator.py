from game import Game
from model.entities.enemies.salamander import Salamander
from model.entities.game_object import GameObject
from model.trap import Trap
from model.helper_functions import item_callbacks
from model.helper_functions import trap_callbacks
from model.config import config
from model.factories import item_factory
from model.factories import monster_factory
import palette


def generate_monsters(area_map, num_monsters):
    enemies = [
        ('bushslime', config.data.enemies.bushslime, palette.mauve, GameObject),
        ('hawk', config.data.enemies.hawk, palette.pink, GameObject),
        ('tigerslash', config.data.enemies.tigerslash, palette.light_orange, GameObject),
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
        ('-', 'scroll of lightning bolt', palette.yellow, item_callbacks.cast_lightning),
        ('-', 'scroll of fireball', palette.red, item_callbacks.cast_fireball),
        ('-', 'scroll of confusion', palette.blue, item_callbacks.cast_confuse)
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

def generate_traps(area_map, num_a, num_b):
    trap_data = [
        ['poison trap', num_a, palette.dark_green, trap_callbacks.poison_trap],
        ['swamp trap', num_b, palette.mauve, trap_callbacks.swamp_trap],
    ]

    for data in trap_data:
        trap_name = data[0]
        num = data[1]
        colour = data[2]
        trap_callback = data[3]

        for i in range(num):
            x, y = area_map.get_random_walkable_tile()
            trap = Trap(x, y, '^', trap_name, colour, trap_callback)
            area_map.entities.append(trap)
            trap.send_to_back()  # items appear below other objects