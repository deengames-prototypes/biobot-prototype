from difficulty import Difficulty
import palette
from constants import POISON_TRAP_RADIUS, POISON_TRAP_TURNS, SWAMP_TRAP_STUCK_TURNS
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
    entity.turns_stuck = SWAMP_TRAP_STUCK_TURNS
    message('{} falls into a patch of swamp!'.format(entity.name))
