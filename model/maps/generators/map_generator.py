from difficulty import Difficulty
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

DIFFICULTY_PER_MONSTER_DISTRIBUTION_PERCENT_INCREASE = 15

def generate_monsters(area_map, num_monsters):
    enemies = [
        ('bushslime', config.data.enemies.bushslime, palette.yellow, GameObject),
        ('hawk', config.data.enemies.hawk, palette.light_orange, GameObject),
        ('tigerslash', config.data.enemies.tigerslash, palette.orange, GameObject),
        ('salamander', config.data.enemies.salamander, palette.red, Salamander)
    ]
    
    # Given two sets of probabilities (base and worst-case) as two points on a line, pick a point between
    # these two extremities based on our proportional difficulty. eg. if base is at 1000 and max is at 2000
    # and we're at 1600, pick a point that's 40% of 1000 + 60% of 2000.
    #
    # But, we don't have a max difficulty. So for every, say, 50, move 1% closer to the max probabilities.
    # If we did that, 1000+5000 = max. The max difficulty really should be around 2000, so the diff is 1000,
    # which means we should move by +1% for every 10.
    base_probabilities = [
        45,
        30,
        25,
        10
    ]

    max_probabilities = [
        5,
        15,
        35,
        45
    ]

    # Up to 750: just use base
    probabilities = base_probabilities
    diff_percent = (Difficulty.instance.diff_from_base() / DIFFICULTY_PER_MONSTER_DISTRIBUTION_PERCENT_INCREASE) / 100.0
    base_percent = 1 - diff_percent
    max_percent = diff_percent

    for i in range(len(probabilities)):
        probabilities[i] = max(0, (base_probabilities[i] * base_percent) + (max_probabilities[i] * max_percent))


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