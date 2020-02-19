from game import Game


class LanceCharge:
    @staticmethod
    def process(target, config):
        Game.instance.fighter_system.get(target).take_damage(config.damage)
