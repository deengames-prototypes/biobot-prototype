from model.components.ai.base import AbstractAI
from model.config import config


class StallionAi(AbstractAI):
    def _take_turn(self):
        if self.owner.is_mounted:
            self.owner.x, self.owner.y = self.owner.player.x, self.owner.player.y
        elif self.owner.distance_to(self.owner.player) >= config.data.player.stallionFollowDistance:
            self.owner.move_towards(self.owner.player.x, self.owner.player.y)
