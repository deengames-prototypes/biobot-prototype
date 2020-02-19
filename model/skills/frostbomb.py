from game import Game
from model.components.ai.monster import FrozenMonster


class FrostBomb:
    @staticmethod
    def process(area_map, player, ai_system, config):
        half_range = config.radius // 2
        for x in range(player.x - half_range, player.x + half_range + 1):
            for y in range(player.y - half_range, player.y + half_range + 1):
                entities = (
                    e
                    for e in area_map.get_entities_on(x, y)
                    if (Game.instance.fighter_system.get(e) is not None
                        and Game.instance.fighter_system.get(e).hostile)
                )
                for entity in entities:
                    ai_system.get(entity).temporarily_switch_to(FrozenMonster(entity, config.turnsToThaw))
