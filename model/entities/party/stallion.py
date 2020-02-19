import palette
from game import Game
from model.components.skill import SkillComponent
from model.config import config
from model.components.ai.stallion import StallionAi
from model.components.fighter import Fighter
from model.entities.game_object import GameObject
from model.helper_functions.death_functions import horse_death


class Stallion(GameObject):
    def __init__(self, player):
        super().__init__(0, 0, '=', 'stallion', color=palette.brown, blocks=True)

        data = config.data.stallion

        Game.instance.ai_system.set(self, StallionAi(self))
        Game.instance.fighter_system.set(
            self, Fighter(
                owner=self,
                hp=data.startingHealth,
                defense=data.startingDefense,
                damage=data.startingDamage,
                death_function=horse_death
            )
        )

        Game.instance.skill_system.set(
            self, SkillComponent(
                owner=self,
                max_skill_points=config.data.stallion.maxSkillPoints

            )
        )

        self.player = player
        self.is_mounted = False
