import palette
from game import Game
from model.components.fighter import Fighter
from model.entities.game_object import GameObject
from model.config import config


class Fire(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, '*', 'Fire', palette.red, blocks=False)

        Game.instance.event_bus.bind('on_entity_move', self.on_entity_move, self)
        Game.instance.event_bus.bind('on_turn_pass', self.on_turn_passed, self)

        self.turns_left_alight = config.data.enemies.fire.selfExtinguishTurns

    def on_entity_move(self, entity):
        if (entity.x, entity.y) == (self.x, self.y):
            fighter = Game.instance.fighter_system.get(entity)
            if fighter is not None:
                damage = Fighter.calculate_damage(config.data.enemies.fire, 1, fighter)
                fighter.take_damage(damage)
            else:
                entity.default_death_function()
            self.default_death_function()

    def on_turn_passed(self):
        self.turns_left_alight -= 1
        if self.turns_left_alight <= 0:
            self.default_death_function()
        if config.data.enemies.fire.spreadProbability >= Game.instance.random.randint(1, 100):
            tile = Game.instance.area_map.mutate_position_if_walkable(self.x, self.y)
            if tile is not None:
                entities_on_tile = Game.instance.area_map.get_entities_on(*tile)
                fire_on_tile = [e for e in entities_on_tile if isinstance(e, Fire)]

                if not fire_on_tile:
                    created_fire = Fire(*tile)
                    Game.instance.area_map.entities.append(created_fire)

                    if entities_on_tile:
                        created_fire.on_entity_move(entities_on_tile[0])
