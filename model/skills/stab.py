from game import Game

class Stab:
    @staticmethod
    def process(player, target, config):
        if Game.instance.fighter_system.has(target):
            Game.instance.fighter_system.get(player).attack(target, config.damageMultiplier)

