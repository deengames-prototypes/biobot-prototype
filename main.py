#!/usr/bin/env python3
from random import Random
from datetime import datetime

from tcod import image_load

from model.config import file_watcher, config
file_watcher.watch('config.json', lambda raw_json: config.load(raw_json))

import palette
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, MAP_WIDTH, MAP_HEIGHT, PANEL_Y, PANEL_HEIGHT, LIMIT_FPS
from difficulty import Difficulty
from game import Game
from data.save_manager import SaveManager
from model.helper_functions.menu import create_menu, message_box
from model.helper_functions.message import message
from model.entities.party.player import Player
from model.entities.party.stallion import Stallion
from model.event.event_bus import EventBus
from model.key_binder import KeyBinder
from model.maps.area_map import AreaMap
from model.maps.generators import ForestGenerator
from model.systems.ai_system import AISystem
from model.systems.system import ComponentSystem
from view.adapter.tdl_adapter import TdlAdapter
from view.map_renderer import MapRenderer

def new_game():

    Game.instance.fighter_system = ComponentSystem()
    Game.instance.xp_system = ComponentSystem()
    Game.instance.skill_system = ComponentSystem()
    Game.instance.ai_system = AISystem()

    Game.instance.player = Player()
    Game.instance.player.set_skills()
    if config.data.stallion.enabled:
        Game.instance.stallion = Stallion(Game.instance.player)

    Game.instance.floors = []

    with open('current_difficulty', 'rb') as f:
        difficulty = int(f.readline())

    Game.instance.current_difficulty = difficulty

    Game.instance.generate_floor()

    Game.instance.area_map.place_on_random_ground(Game.instance.player)
    if config.data.stallion.enabled:
        Game.instance.area_map.place_around(Game.instance.stallion, Game.instance.player.x, Game.instance.player.y)

    Game.instance.game_state = 'playing'
    Game.instance.inventory = []

    # create the list of game messages and their colors, starts empty
    Game.instance.game_messages = []

    # a warm welcoming message!
    message('Bio-bot 7163R descends to the planet.', palette.red)

def play_game():
    Game.instance.ui.clear()
    Game.instance.ui.blit_map_and_panel()

    Game.instance.mouse_coord = (0, 0)
    Game.instance.renderer = MapRenderer(Game.instance.player, Game.instance.ui)
    Game.instance.renderer.recompute_fov = True
    Game.instance.renderer.refresh_all()

    Game.instance.current_turn = Game.instance.player
    Game.instance.ui.run()


def init_game():
    Game() # initializes Game.instance
    Difficulty()

    Game.instance.save_manager = SaveManager(Game)

    Game.instance.ui = TdlAdapter(
        "Roguelike",
        screen=(SCREEN_WIDTH, SCREEN_HEIGHT),
        map=(200, 50),
        panel=(SCREEN_WIDTH, PANEL_HEIGHT),
        fps_limit=LIMIT_FPS)
    
    Game.instance.keybinder = KeyBinder(Game)        
    Game.instance.keybinder.register_all_keybinds_and_events()
    
    seed = config.get("seed") or int(datetime.now().timestamp())
    Game.instance.random = Random(seed)
    print("Seeding as universe #{}".format(seed))

def main_menu():
    init_game()
    img = image_load('menu_background.png')

    while not Game.instance.ui.event_closed():
        # show the background image, at twice the regular console resolution
        img.blit_2x(Game.instance.ui.root, 0, 0)

        # show the game's title, and some credits!
        title = 'BIOBOT (PROTOTYPE)'
        center = (SCREEN_WIDTH - len(title)) // 2
        Game.instance.ui.draw_root(center, SCREEN_HEIGHT // 2 - 4, title, palette.yellow)

        title = 'Difficulty: {}'.format(Difficulty.instance.current_difficulty)
        center = (SCREEN_WIDTH - len(title)) // 2
        Game.instance.ui.draw_root(center, SCREEN_HEIGHT - 2, title, palette.white)

        # show options and wait for the player's choice
        choice = create_menu('', ['Play a new game', 'Continue last game', 'Quit'], 24)

        if choice == 0:  # new game
            new_game()
            play_game()
        if choice == 1:  # load last game
            try:
                Game.instance.save_manager.load()
            except Exception as e:
                message_box('\n No saved game to load.\n', 24)
                continue
            play_game()
        elif choice == 2:  # quit
            break

    print("Terminating ...")

    file_watcher.stop()


if __name__ == '__main__':
    main_menu()

