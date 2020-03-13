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
DIFFICULTY_PER_TRAP_INCREASE = 80 # a bit faster than we add rows/columns to the map

def generate_monsters(area_map, num_monsters):
    enemies = [
        ('walkrock', config.data.enemies.walkrock, palette.yellow, GameObject),
        ('treeshell', config.data.enemies.treeshell, palette.light_orange, GameObject),
        ('bloodbat', config.data.enemies.bloodbat, palette.orange, GameObject),
        ('salamander', config.data.enemies.salamander, palette.red, Salamander),
        ('ogrestone', config.data.enemies.ogrestone, palette.mauve, GameObject),
        ('venobite', config.data.enemies.venobite, palette.pink, GameObject),
        ('ent', config.data.enemies.ent, palette.purple, GameObject),
        ('flamespider', config.data.enemies.flamespider, palette.red, Salamander),
        ('chompvine', config.data.enemies.chompvine, palette.fuscia, GameObject)
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
        10,
        0,
        0,
        0,
        0,
        0
    ]

    max_probabilities = [
        0,
        0,
        0,
        0,
        10,
        10,
        20,
        30,
        30
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
        
        # Don't add monsters that are impossible to hurt. Spawn the next strongest thing.
        # Assumes you're smart enough to stab/scroll them.
        while data.defense >= 2 * Game.instance.fighter_system.get(Game.instance.player).damage:
            index = get_enemies_index(data, enemies)
            data = enemies[index - 1][1]
        
        monster = monster_factory.create_monster(data, x, y, colour, name, cls)
        area_map.entities.append(monster)

def get_enemies_index(who, enemies):
    for i in range(len(enemies)):
        if enemies[i][1] == who:
            return i
    
    return -1

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
    base_total = num_a + num_b
    percent_a = num_a * 1.0 / base_total
    percent_b = num_b * 1.0 / base_total

    extra_traps = Difficulty.instance.diff_from_base() // DIFFICULTY_PER_TRAP_INCREASE
    new_total = base_total + extra_traps
    poison_traps = int(percent_a * new_total)
    swamp_traps = int(percent_b * new_total)

    trap_data = [
        ['poison trap', poison_traps, palette.dark_green, trap_callbacks.poison_trap],
        ['swamp trap', swamp_traps, palette.mauve, trap_callbacks.swamp_trap],
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