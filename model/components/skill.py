from model.components.base import Component

class SkillComponent(Component):
    def __init__(self, owner, max_skill_points: int):
        super().__init__(owner)
        self.skill_points = max_skill_points
        self.max_skill_points = max_skill_points

    def can_use_skill(self, skill_cost: int):
        return self.skill_points - skill_cost >= 0

    def use_skill(self, skill_cost: int):
        self.skill_points -= skill_cost
        if self.skill_points < 0:
            self.skill_points = 0

    def restore_skill_points(self, to_restore: int):
        self.skill_points += to_restore
        if self.skill_points > self.max_skill_points:
            self.skill_points = self.max_skill_points
