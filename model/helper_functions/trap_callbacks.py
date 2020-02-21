from difficulty import Difficulty
import palette
from constants import POISON_TRAP_RADIUS, POISON_TRAP_TURNS
from game import Game
from model.config import config
from model.helper_functions.message import message

def poison_trap(target):
    # Poison everything alive in our radius
    (x, y) = (target.x, target.y)
    victims = [e for e in Game.instance.area_map.entities if e.distance(x, y) <= POISON_TRAP_RADIUS and Game.instance.fighter_system.get(e)]
    for victim in victims:
        message('{} is poisoned!'.format(victim.name))
        Game.instance.fighter_system.get(victim).poison_left += POISON_TRAP_TURNS
    
def swamp_trap(entity):
    # You're stuck for a few turns
    pass


# def fireball_trap():
#     # ask the player for a target tile to throw a fireball at
#     message('Left-click a target tile for the fireball, or right-click to ' +
#             'cancel.', palette.light_cyan)

#     (x, y) = target_tile()
#     if x is None:
#         message('Cancelled')
#         return 'cancelled'
#     message('The fireball explodes, burning everything within ' +
#             str(FIREBALL_RADIUS) + ' tiles!', palette.orange)

#     for obj in Game.instance.area_map.entities:  # damage every fighter in range, including the player
#         obj_fighter = Game.instance.fighter_system.get(obj)
#         if obj.distance(x, y) <= FIREBALL_RADIUS and obj_fighter:
#             message('The ' + obj.name + ' gets burned for ' +
#                     str(FIREBALL_DAMAGE) + ' hit points.', palette.orange)

#             obj_fighter.take_damage(FIREBALL_DAMAGE)
