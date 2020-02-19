import palette
from constants import DELTA_UP, DELTA_DOWN, DELTA_LEFT, DELTA_RIGHT
from game import Game
from model.helper_functions.menu import inventory_menu
from model.helper_functions.message import message
from model.helper_functions.skills import can_use_skill
from model.keys.decorators import in_game, skill, horse_skill
from model.keys.util import map_movement_callback
from model.skills.frostbomb import FrostBomb
from model.skills.lance_charge import LanceCharge
from model.skills.omnislash import OmniSlash
from model.skills.ruqya import Ruqya
from model.skills.whirlwind import Whirlwind
from model.config import config
from model.weapons import Bow


def exit_to_main_menu_callback(event):
    Game.instance.save_manager.save()
    Game.instance.ui.app.suspend()
    Game.instance.ui.unblit_map_and_panel()


def enter_callback(event):
    if event.alt:
        Game.instance.ui.toggle_fullscreen()


# Movement
@in_game(pass_turn=True)
def up_callback(event):
    Game.instance.player.move_or_attack(*DELTA_UP)


@in_game(pass_turn=True)
def down_callback(event):
    Game.instance.player.move_or_attack(*DELTA_DOWN)


@in_game(pass_turn=True)
def left_callback(event):
    Game.instance.player.move_or_attack(*DELTA_LEFT)


@in_game(pass_turn=True)
def right_callback(event):
    Game.instance.player.move_or_attack(*DELTA_RIGHT)


# Item pick up
@in_game(pass_turn=False)
def pickup_callback(event):
    for obj in Game.instance.area_map.entities:  # look for an item in the player's tile
        obj_item = Game.instance.item_system.get(obj)
        if (obj.x, obj.y) == (Game.instance.player.x, Game.instance.player.y) and obj_item:
            obj_item.pick_up()
            break


# Inventory use
@in_game(pass_turn=False)
def inventory_use(event):
    chosen_item = inventory_menu('Press the key next to an item to use it, or any other to cancel.\n')
    if chosen_item is not None:
        chosen_item.use()


# Inventory drop
@in_game(pass_turn=False)
def inventory_drop(event):
    chosen_item = inventory_menu('Press the key next to an item to drop it, or any other to cancel.\n')
    if chosen_item is not None:
        chosen_item.drop()


# Bow
@in_game(pass_turn=False)
def bow_callback(event):
    arrows_are_available = (not config.data.features.limitedArrows
                            or (config.data.features.limitedArrows and Game.instance.player.arrows > 0))

    if isinstance(Game.instance.fighter_system.get(Game.instance.player).weapon, Bow) and arrows_are_available:
        Game.instance.draw_bowsight = True
        Game.instance.auto_target = True

        Game.instance.keybinder.suspend_all_keybinds()

        @in_game(pass_turn=False)
        def new_escape_callback(event):
            Game.instance.draw_bowsight = False
            Game.instance.current_turn = Game.instance.player
            Game.instance.keybinder.register_all_keybinds_and_events()

        @in_game(pass_turn=True)
        def new_f_callback(event):
            if not Game.instance.auto_target:
                Game.instance.target = Game.instance.area_map.get_blocking_object_at(*Game.instance.mouse_coord) or None

            if Game.instance.target and Game.instance.fighter_system.has(Game.instance.target):
                is_critical = False
                conf = config.data.weapons
                damage_multiplier = conf.arrowDamageMultiplier

                if config.data.features.bowCrits and Game.instance.random.randint(0, 100) <= conf.bowCriticalProbability:
                    damage_multiplier *= 1 + conf.bowCriticalDamageMultiplier
                    if config.data.features.bowCritsStack:
                        target_fighter = Game.instance.fighter_system.get(Game.instance.target)
                        damage_multiplier += conf.bowCriticalDamageMultiplier * target_fighter.bow_crits
                        target_fighter.bow_crits += 1
                    is_critical = True

                Game.instance.fighter_system.get(Game.instance.player).attack(Game.instance.target, damage_multiplier, is_critical)
                Game.instance.player.arrows -= 1
                Game.instance.auto_target = True

        Game.instance.keybinder.register_keybind('ESCAPE', new_escape_callback)
        Game.instance.keybinder.register_keybind('f', new_f_callback)


# Mount
@in_game(pass_turn=True)
def mount_callback(event):
    if config.data.stallion.enabled and Game.instance.player.distance_to(Game.instance.stallion) <= 1:
        if Game.instance.player.mounted:
            Game.instance.player.unmount(Game.instance.stallion)
        else:
            Game.instance.player.mount(Game.instance.stallion)


# Rest
@in_game(pass_turn=True)
def rest_callback(event):
    if config.data.skills.resting.enabled:
        Game.instance.player.rest()


# Continuous rest
@in_game(pass_turn=False)
def continuous_rest_callback(event):
    if config.data.skills.resting.enabled:
        turns_to_rest = Game.instance.player.calculate_turns_to_rest()
        message(f'You rest for {turns_to_rest} turns.')

        def can_rest():
            return not [
                    e
                    for e in Game.instance.area_map.entities
                    if (Game.instance.fighter_system.has(e)
                        and Game.instance.fighter_system.get(e).hostile
                        and (e.x, e.y) in Game.instance.renderer.visible_tiles)
                ]

        def new_update_callback(delta_time, update_manager):
            nonlocal turns_to_rest
            if turns_to_rest > 0:
                if can_rest():
                    update_manager.take_enemy_turns()
                    update_manager.restore_skill_points()
                    turns_to_rest -= 1
                    Game.instance.player.rest()
                    Game.instance.current_turn = None
                else:
                    message("Your resting is interrupted; there are enemies nearby!", palette.red)
                    turns_to_rest = 0
                    new_update_callback(delta_time, update_manager)
            else:
                Game.instance.keybinder.register_all_keybinds_and_events()

        Game.instance.keybinder.suspend_all_keybinds()
        Game.instance.keybinder.register_update(new_update_callback)


@skill(cost=config.data.skills.whirlwind.cost)
@in_game(pass_turn=True)
def whirlwind_callback(event):
    if config.data.skills.whirlwind.enabled:
        Whirlwind.process(Game.instance.player, config.data.skills.whirlwind.radius, Game.instance.area_map)


@in_game(pass_turn=False)
def omnislash_callback(event):
    """Enter omnislash mode!"""
    if config.data.skills.omnislash.enabled:
        message('Attack an enemy to activate omnislash, or press escape to cancel.', palette.light_cyan)

        Game.instance.keybinder.suspend_all_keybinds()

        def new_escape_callback(event):
            message('Cancelled')
            Game.instance.keybinder.register_all_keybinds()

        def new_move_callback(dx, dy):
            target = Game.instance.area_map.get_blocking_object_at(Game.instance.player.x + dx, Game.instance.player.y + dy)
            if target is not None and Game.instance.fighter_system.has(target):
                message(f'{target.name.capitalize()} has been ruthlessly attacked by {Game.instance.player.name}!',
                        palette.purple)
                Game.instance.skill_system.get(Game.instance.player).use_skill(config.data.skills.omnislash.cost)
                OmniSlash.process(Game.instance.player, target, config.data.skills.omnislash)
                Game.instance.keybinder.register_all_keybinds()
            else:
                Game.instance.player.move_or_attack(dx, dy)

        map_movement_callback(new_move_callback)
        Game.instance.keybinder.register_keybind('ESCAPE', new_escape_callback)


@skill(cost=config.data.skills.frostbomb.cost)
@in_game(pass_turn=True)
def frost_bomb_callback(event):
    if config.data.skills.frostbomb.enabled:
        FrostBomb.process(Game.instance.area_map, Game.instance.player, Game.instance.ai_system, config.data.skills.frostbomb)
        message("A cold wind gushes forward as enemies around you freeze!", palette.cyan)


@horse_skill(cost=0)
@in_game(pass_turn=False)
def lance_charge_callback(event):
    if config.data.stallion.enabled and config.data.skills.lanceCharge.enabled:
        message('Move to charge with your lance, or press escape to cancel.', palette.light_cyan)

        Game.instance.keybinder.suspend_all_keybinds()

        def new_escape_callback(event):
            message('Cancelled')
            Game.instance.keybinder.register_all_keybinds()

        def new_move_callback(dx, dy):
            charge_distance = config.data.skills.lanceCharge.chargeDistance
            message("With a mighty charge, you bolster your lance towards your enemies!")

            for _ in range(charge_distance):
                target = Game.instance.area_map.get_blocking_object_at(Game.instance.player.x + dx, Game.instance.player.y + dy)
                if target is not None and Game.instance.fighter_system.has(target):
                    LanceCharge.process(target, config.data.skills.lanceCharge)

                Game.instance.player.move_or_attack(dx, dy)

            Game.instance.skill_system.get(Game.instance.stallion).use_skill(config.data.skills.lanceCharge.cost)
            Game.instance.keybinder.register_all_keybinds()

        map_movement_callback(new_move_callback)
        Game.instance.keybinder.register_keybind('ESCAPE', new_escape_callback)


@in_game(pass_turn=False)
def ruqya_callback(event):
    if config.data.skills.ruqya.enabled:
        player_fighter = Game.instance.fighter_system.get(Game.instance.player)
        if player_fighter.hp == player_fighter.max_hp:
            message("You are already at full health.", palette.red)
            return

        if can_use_skill(config.data.skills.ruqya.cost):
            Ruqya.process(player_fighter, config.data.skills.ruqya)
            Game.instance.current_turn = None
