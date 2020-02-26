import palette
from constants import FOV_ALGO, FOV_LIGHT_WALLS, MSG_X, SCREEN_WIDTH, SCREEN_HEIGHT
from difficulty import Difficulty
from game import Game
from model.maps import area_map
from model.config import config
from view.targeting_monster import closest_monster
from view.targeting_mouse import get_names_under_mouse

class MapRenderer:
    def __init__(self, player, ui_adapter):
        self._player = player
        self._ui_adapter = ui_adapter
        self._previous_camera = (-1, -1) # redraw on first draw
        self.reset()
        
    def reset(self):
        self.recompute_fov = True
        self.visible_tiles = []

    def render(self):
        camera_x, camera_y = self._get_camera_coordinates()
        previous_x, previous_y = self._previous_camera

        if camera_x != previous_x or camera_y != previous_y:
            self._previous_camera = camera_x, camera_y
            # Draw things outside our FOV that are on-screen but maybe moved because the camera moved
            # TODO: do this more selectively (on first render or on camera-move)
            for x in range(camera_x, camera_x + SCREEN_WIDTH - 1):
                for y in range(camera_y, camera_y + SCREEN_HEIGHT - 5 - 1):
                    tile = Game.instance.area_map.tiles[x][y]
                    self.draw_string(x, y, tile.character, tile.dark_colour)

        if self.recompute_fov:
            self.recompute_fov = False
            # The current FOV is changing. Draw everything in it with the "explored"
            # style (because it was in the FOV, so it is explored).
            for (x, y) in self.visible_tiles:
                tile = Game.instance.area_map.tiles[x][y]
                self.draw_string(x, y, tile.character, tile.dark_colour)

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
            self.draw_string(x, y, tile.character, tile.colour)

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
                        self.draw_string(pos[0], pos[1], 'X', palette.red)
                    else:
                        self.draw_string(pos[0], pos[1], '*', palette.dark_green)

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
        LABEL_X = 3

        self._ui_adapter.panel.draw_str(LABEL_X, 1, "LEVEL {}".format(xp_component.level))
        self._ui_adapter.panel.draw_str(LABEL_X, 2, "HP: {}/{}".format(player_fighter.hp, player_fighter.max_hp))
        self._ui_adapter.panel.draw_str(LABEL_X, 3, "SP: {}/{}".format(skill_component.skill_points,
                                                                  config.data.player.maxSkillPoints))

        self._ui_adapter.panel.draw_str(LABEL_X, 4, "FLOOR {}".format(Game.instance.area_map.floor_num))
        self._ui_adapter.panel.draw_str(LABEL_X, 5, "Difficulty: {}".format(Difficulty.instance.current_difficulty))

        # display names of objects under the mouse
        self._ui_adapter.panel.draw_str(1, 0, get_names_under_mouse(), fg=palette.light_gray)

        self._ui_adapter.flush()

    def refresh_all(self):
        for x in range(Game.instance.area_map.width):
            for y in range(Game.instance.area_map.height):
                tile = Game.instance.area_map.tiles[x][y]
                if tile.is_explored:
                    self.draw_string(x, y, tile.character, tile.dark_colour)
                else:
                    self.draw_string(x, y, ' ', palette.black)

    # Quick fix for map > camera size: translate world-to-screen and only draw things on-screen
    def draw_string(self, x, y, string, colour):
        camera_x, camera_y = self._get_camera_coordinates()

        screen_x = x - camera_x
        screen_y = y - camera_y

        if 0 <= screen_x < SCREEN_WIDTH and 0 <= screen_y < SCREEN_HEIGHT:
            self._ui_adapter.con.draw_str(screen_x, screen_y, string, colour)
    
    def _get_camera_coordinates(self):
        map_width = Game.instance.area_map.width
        map_height = Game.instance.area_map.height

        camera_left = self._player.x - (SCREEN_WIDTH // 2)
        if camera_left > map_width - SCREEN_WIDTH: camera_left = map_width - SCREEN_WIDTH
        if camera_left < 0: camera_left = 0
        
        camera_top = self._player.y - (SCREEN_HEIGHT // 2)
        if camera_top > map_height - SCREEN_HEIGHT: camera_top = map_height - SCREEN_HEIGHT
        if camera_top < 0: camera_top = 0
        
        return (camera_left, camera_top)