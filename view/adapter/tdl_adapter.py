#!/usr/bin/env python3
import tdl

from constants import PANEL_Y, PANEL_HEIGHT, SCREEN_WIDTH
from game import Game
from model.config import config
from view.adapter.console_adapter import ConsoleAdapter
from view.adapter.extensible_app import ExtensibleApp


class TdlAdapter:
    def __init__(self, window_title, screen, map, panel, fps_limit=20):
        tdl.set_font('arial10x10.png', greyscale=True, altLayout=True)
        self.root = tdl.init(*screen, title=window_title,
                             fullscreen=config.data.fullscreen)
        tdl.setFPS(fps_limit)
        self.blit_dict = {}  # dict of {console: (args, kwargs)}

        self.con = self.managed_console(*map)
        self.panel = self.managed_console(*panel)

        self.app = ExtensibleApp()

    def blit_map_and_panel(self):
        self.blit_at(self.panel, 0, PANEL_Y, SCREEN_WIDTH, PANEL_HEIGHT, 0, 0)
        self.blit_at(self.con, 0, 0, self.con.width, self.con.height, 0, 0)

    def unblit_map_and_panel(self):
        self.unblit(self.panel)
        self.unblit(self.con)

    def run(self):
        self.app.run()

    def clear(self):
        """
        Clears the screen.
        """
        self.root.clear()

    def flush(self):
        """
        Render everything from buffers to screen
        """
        for console, (args, kwargs) in self.blit_dict.items():
            self.root.blit(console, *args, **kwargs)
        tdl.flush()

    @staticmethod
    def calculate_fov(origin_x, origin_y, is_tile_walkable_callback, algorithm, view_radius, should_light_walls):
        return tdl.map.quickFOV(
            origin_x, origin_y,
            is_tile_walkable_callback,
            fov=algorithm,
            radius=view_radius,
            lightWalls=should_light_walls
        )

    def wait_for(self, event, *, flush=True, condition=lambda i: True):
        while True:
            if flush:
                if Game.instance.renderer is not None:
                    Game.instance.renderer.render()
                else:
                    self.flush()

            user_input = tdl.event.wait()
            if user_input.type == event and condition(user_input):
                return user_input

    def wait_for_mouse(self, flush=True):
        return self.wait_for('MOUSEDOWN', flush=flush)

    def wait_for_key(self, flush=True):
        """
        wait for response

        The condition is used to normalize keydown events to only one event per keypress(TEXT)
            instead of two(CHAR and TEXT)
        """
        return self.wait_for('KEYDOWN', flush=flush, condition=lambda i: i.key == 'TEXT')

    @staticmethod
    def get_input():
        """
        Ask for input. If none, returns None.
        """
        for event in tdl.event.get():
            return event

    @staticmethod
    def toggle_fullscreen():
        tdl.set_fullscreen(not tdl.get_fullscreen())

    @staticmethod
    def event_closed():
        return tdl.event.is_window_closed()

    @staticmethod
    def managed_console(width, height):
        return ConsoleAdapter(width, height)

    def draw_root(self, x, y, string, color):
        self.root.draw_str(x, y, string, fg=color, bg=None)

    def blit_at(self, console, *args, **kwargs):
        self.blit_dict[console.console] = args, kwargs

    def unblit(self, console):
        if self.blit_dict.get(console.console, None):
            del self.blit_dict[console.console]

    @staticmethod
    def bresenham(x1, y1, x2, y2):
        return tdl.map.bresenham(x1, y1, x2, y2)
