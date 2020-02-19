from game import Game
from model.components.ai.monster import BasicMonster

from model.helper_functions.death_functions import monster_death
from model.components.fighter import Fighter
from model.components.xp import XPComponent


def create_monster(data, x, y, colour, name, cls):
    monster = cls(x, y, name[0], name, colour, blocks=True)

    Game.instance.fighter_system.set(
        monster, Fighter(
            owner=monster,
            hp=data.health,
            defense=data.defense,
            damage=data.attack,
            death_function=monster_death,
            hostile=True
        )
    )

    Game.instance.xp_system.set(
        monster, XPComponent(
            owner=monster,
            xp=data.xp
        )
    )

    Game.instance.ai_system.set(monster, BasicMonster(monster))

    return monster
