import palette
from constants import HEAL_AMOUNT, LIGHTNING_RANGE, LIGHTNING_DAMAGE, CONFUSE_RANGE, FIREBALL_RADIUS, FIREBALL_DAMAGE
from view.targeting_distance import target_tile, target_monster
from view.targeting_monster import closest_monster
from game import Game
from model.config import config
from model.helper_functions.message import message
from model.components.ai.monster import ConfusedMonster


def cast_heal():
    # heal the player
    player_fighter = Game.instance.fighter_system.get(Game.instance.player)
    if player_fighter.hp == player_fighter.max_hp:
        message('You are already at full health.', palette.red)
        return 'cancelled'

    message('Your wounds start to feel better!', palette.pink)
    player_fighter.heal(HEAL_AMOUNT)


def cast_lightning():
    # find closest enemy (inside a maximum range) and damage it
    monster = closest_monster(Game, LIGHTNING_RANGE)
    if monster is None:  # no enemy found within maximum range
        message('No enemy is close enough to strike.', palette.red)
        return 'cancelled'

    # zap it!
    message('A lighting bolt strikes the ' + monster.name + ' with a loud ' +
            'thunder! The damage is ' + str(LIGHTNING_DAMAGE) + ' hit points.',
            palette.blue)

    Game.instance.fighter_system.get(monster).take_damage(LIGHTNING_DAMAGE)


def cast_confuse():
    # ask the player for a target to confuse
    message('Left-click an enemy to confuse it, or right-click to cancel.',
            palette.light_cyan)
    monster = target_monster(CONFUSE_RANGE)
    if monster is None:
        message('Cancelled')
        return 'cancelled'

    # replace the monster's AI with a "confused" one; after some turns it will
    # restore the old AI
    Game.instance.ai_system.get(monster).temporarily_switch_to(ConfusedMonster(monster))
    message('The eyes of the ' + monster.name + ' look vacant, as he starts to ' +
            'stumble around!', palette.lime_green)


def cast_fireball():
    # ask the player for a target tile to throw a fireball at
    message('Left-click a target tile for the fireball, or right-click to ' +
            'cancel.', palette.light_cyan)

    (x, y) = target_tile()
    if x is None:
        message('Cancelled')
        return 'cancelled'
    message('The fireball explodes, burning everything within ' +
            str(FIREBALL_RADIUS) + ' tiles!', palette.orange)

    for obj in Game.instance.area_map.entities:  # damage every fighter in range, including the player
        obj_fighter = Game.instance.fighter_system.get(obj)
        if obj.distance(x, y) <= FIREBALL_RADIUS and obj_fighter:
            message('The ' + obj.name + ' gets burned for ' +
                    str(FIREBALL_DAMAGE) + ' hit points.', palette.orange)

            obj_fighter.take_damage(FIREBALL_DAMAGE)


def restore_skill_points():
    skill_component = Game.instance.skill_system.get(Game.instance.player)

    if skill_component.skill_points == config.data.player.maxSkillPoints:
        message("You already feel great and ready for action.", palette.red)
        return 'cancelled'

    message('You feel a lot more refreshed!', palette.pink)
    skill_component.restore_skill_points(config.data.item.skillPointPotion.restores)
