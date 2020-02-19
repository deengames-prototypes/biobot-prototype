from game import Game


class Whirlwind:
    # modified copypasta from cast_fireball
    # TODO: DRY?
    @staticmethod
    def process(player, radius, area_map):
        for obj in area_map.entities:
            if obj.distance(player.x, player.y) <= radius and Game.instance.fighter_system.has(obj) and Game.instance.fighter_system.get(obj).hostile:
                Game.instance.fighter_system.get(player).attack(obj)
