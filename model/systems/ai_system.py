from model.systems.system import ComponentSystem


class AISystem(ComponentSystem):
    def take_turn(self, entity):
        if self.has(entity):
            ai = self.get(entity)
            ai.take_turn()
