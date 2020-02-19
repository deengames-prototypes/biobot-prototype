class Ruqya:
    @staticmethod
    def process(player_fighter, config):
        to_restore = int(config.percent/100 * player_fighter.max_hp)
        player_fighter.heal(to_restore)
