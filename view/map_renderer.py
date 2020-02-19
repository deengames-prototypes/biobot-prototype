import palette
from constants import FOV_ALGO, FOV_LIGHT_WALLS, MSG_X
from game import Game
from model.maps import area_map
from model.config import config
from view.targeting_monster import closest_monster
from view.targeting_mouse import get_names_under_mouse


class MapRenderer:
    def __init__(self, player, ui_adapter):
        self._player = player
        self._ui_adapter = ui_adapter

        self.reset()
        
    def reset(self):
        self.recompute_fov = True
        self.visible_tiles = []
        self._all_tiles_rendered = False

    def render(self):
        if config.data.features.seeAllTiles and not self._all_tiles_rendered:
            for x in range(Game.instance.area_map.width):
                for y in range(Game.instance.area_map.height):
                    tile = Game.instance.area_map.tiles[x][y]
                    self._ui_adapter.con.draw_str(x, y, tile.character, tile.dark_colour)
            self._all_tiles_rendered = True

        if self.recompute_fov:
            self.recompute_fov = False
            # The current FOV is changing. Draw everything in it with the "explored"
            # style (because it was in the FOV, so it is explored).
            for (x, y) in self.visible_tiles:
                tile = Game.instance.area_map.tiles[x][y]
                self._ui_adapter.con.draw_str(x, y, tile.character, tile.dark_colour)

            # Due to lightWalls being set to true, we need to filter "walls" that are out of bounds.
            self.visible_tiles = area_map.filter_tiles(
                self._ui_adapter.calculate_fov(
                    self._player.x, self._player.y,
                    Game.instance.area_map.is_visible_tile,
                    FOV_ALGO,
                    config.data.player.lightRadius,
                    FOV_LIGHT_WALLS
                ),
                Game.instance.area_map.is_on_map
            )

            for (x, y) in self.visible_tiles:
                Game.instance.area_map.tiles[x][y].is_explored = True

        # Draw everything in the current FOV
        for (x, y) in self.visible_tiles:
            tile = Game.instance.area_map.tiles[x][y]
            self._ui_adapter.con.draw_str(x, y, tile.character, tile.colour)

        for e in Game.instance.area_map.entities:
            if e is self._player:
                continue
            e.draw()

        if Game.instance.draw_bowsight:
            Game.instance.target = closest_monster(Game, config.data.player.lightRadius) if Game.instance.auto_target else None
            x2, y2 = (Game.instance.target.x, Game.instance.target.y) if Game.instance.target is not None else Game.instance.mouse_coord

            x1, y1 = self._player.x, self._player.y
            line = Game.instance.ui.bresenham(x1, y1, x2, y2)
            monster_on_target_tile = [x for x in Game.instance.area_map.get_entities_on(x2, y2) if Game.instance.fighter_system.has(x)]
            for pos in line:
                if pos in self.visible_tiles:
                    if pos == (x2, y2) and monster_on_target_tile:
                        self._ui_adapter.con.draw_str(pos[0], pos[1], 'X', fg=palette.red)
                    else:
                        self._ui_adapter.con.draw_str(pos[0], pos[1], '*', palette.dark_green)

        self._player.draw()

        # prepare to render the GUI self._ui_adapter.panel
        self._ui_adapter.panel.clear(fg=palette.white, bg=palette.black)

        # print the game messages, one line at a time
        y = 1
        for (line, color) in Game.instance.game_messages:
            self._ui_adapter.panel.draw_str(MSG_X, y, line, fg=color)
            y += 1

        # show the player's stats
        self._ui_adapter.panel.draw_str(1, 1, "PLAYER")

        player_fighter = Game.instance.fighter_system.get(self._player)
        skill_component = Game.instance.skill_system.get(self._player)
        xp_component = Game.instance.xp_system.get(self._player)

        self._ui_adapter.panel.draw_str(11, 1, "LEVEL {}".format(xp_component.level))
        self._ui_adapter.panel.draw_str(10, 2, "HP: {}/{}".format(player_fighter.hp, player_fighter.max_hp))
        self._ui_adapter.panel.draw_str(10, 3, "SP: {}/{}".format(skill_component.skill_points,
                                                                  config.data.player.maxSkillPoints))

        self._ui_adapter.panel.draw_str(11, 4, "FLOOR {}".format(Game.instance.area_map.floor_num))

        # show the horse's stats
        if config.data.stallion.enabled:
            self._ui_adapter.panel.draw_str(1, 4, "STALLION")

            stallion_fighter = Game.instance.fighter_system.get(Game.instance.stallion)
            skill_component = Game.instance.skill_system.get(Game.instance.stallion)

            self._ui_adapter.panel.draw_str(10, 5, "HP: {}/{}".format(stallion_fighter.hp, stallion_fighter.max_hp))
            self._ui_adapter.panel.draw_str(10, 6, "SP: {}/{}".format(skill_component.skill_points,
                                                                      config.data.stallion.maxSkillPoints))

        # display names of objects under the mouse
        self._ui_adapter.panel.draw_str(1, 0, get_names_under_mouse(), fg=palette.light_gray)

        self._ui_adapter.flush()

    def refresh_all(self):
        for x in range(Game.instance.area_map.width):
            for y in range(Game.instance.area_map.height):
                tile = Game.instance.area_map.tiles[x][y]
                if tile.is_explored:
                    self._ui_adapter.con.draw_str(x, y, tile.character, tile.dark_colour)
                else:
                    self._ui_adapter.con.draw_str(x, y, ' ')
