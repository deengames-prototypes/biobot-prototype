from game import Game
from model.config import config


def can_use_skill(cost: int) -> bool:
    skill_component = Game.instance.skill_system.get(Game.instance.player)
    if skill_component.can_use_skill(cost):
        skill_component.use_skill(cost)
        return True
    else:
        return False


def can_use_horse_skill(cost: int) -> bool:
    if config.data.stallion.enabled:
        skill_component = Game.instance.skill_system.get(Game.instance.stallion)
        if skill_component.can_use_skill(cost):
            skill_component.use_skill(cost)
            return True

    return False
