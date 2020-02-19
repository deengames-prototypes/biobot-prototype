import colors
from model.config import config
from model.components.ai.monster import StunnedMonster
from model.helper_functions.message import message
from model.weapons.base import Weapon


class Sword(Weapon):
    """
    A sword. It sometimes incapacitates (stuns) the opponent due to damage
    inflicted. As a class, it doesn't calculate or deal damage; merely adds
    effects on top of the combat algorithms. (This is true of all weapons.)
    """
    def attack(self, target, game, **kwargs):
        if config.data.features.swordStuns and game.ai_system.has(target):
            if game.random.randint(0, 100) <= config.data.weapons.swordStunProbability:
                target_ai = game.ai_system.get(target)
                if config.data.features.stunsStack:
                    if isinstance(target_ai, StunnedMonster):
                        # Stack the stun
                        target_ai.num_turns += config.data.weapons.numTurnsStunned
                    else:
                        target_ai.temporarily_switch_to(StunnedMonster(target))
                else:
                    # Copy-pasta from two lines above
                    target_ai.temporarily_switch_to(StunnedMonster(target))
                message('{} looks incapacitated!'.format(target.name), colors.light_green)