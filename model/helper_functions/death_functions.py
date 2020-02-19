import colors
from model.helper_functions.message import message
from game import Game


def monster_death(monster):
    # transform it into a nasty corpse! it doesn't block, can't be
    # attacked and doesn't move
    message(monster.name.capitalize() + ' is dead!', colors.orange)
    _mark_entity_as_dead(monster)

    Game.instance.xp_system.get(Game.instance.player).gain_xp(Game.instance.xp_system.get(monster).xp)
    Game.instance.fighter_system.remove(monster)
    Game.instance.ai_system.remove(monster)

    monster.original_ai = None


def player_death(player):
    # the game ended!
    message('You died!', colors.red)
    Game.instance.game_state = 'dead'
    Game.instance.keybinder.register_all_keybinds_and_events()

    # for added effect, transform the player into a corpse!
    player.char = '%'
    player.color = colors.dark_red


def horse_death(horse):
    message('Stallion is dead!', colors.red)
    _mark_entity_as_dead(horse)

    Game.instance.fighter_system.remove(horse)
    Game.instance.ai_system.remove(horse)

    if Game.instance.player.mounted:
        Game.instance.player.unmount(Game.instance.stallion)


def _mark_entity_as_dead(entity):
    entity.char = '%'
    entity.color = colors.dark_red
    entity.blocks = False
    entity.name = "{} remains".format(entity.name)
    entity.send_to_back()
