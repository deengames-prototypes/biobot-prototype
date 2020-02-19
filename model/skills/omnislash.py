from game import Game


class OmniSlash:
    @staticmethod
    def process(player, target, config):
        # do guaranteed hits
        for _ in range(config.guaranteedHits):
            if Game.instance.fighter_system.has(target):
                Game.instance.fighter_system.get(player).attack(target)
            else:
                return  # it's dead already!

        # do lucky hits
        while True:
            should_re_hit = Game.instance.random.randint(0, 100) <= config.probabilityOfAnotherHit
            if should_re_hit and Game.instance.fighter_system.has(target):
                Game.instance.fighter_system.get(player).attack(target)
            else:
                return

