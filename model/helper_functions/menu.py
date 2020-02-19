import textwrap

import colors
from constants import INVENTORY_WIDTH, SCREEN_WIDTH, SCREEN_HEIGHT
from game import Game


def create_menu(header, options, width):
    if len(options) > 26:
        raise ValueError('Cannot have a menu with more than 26 options.')

    # calculate total height for the header (after textwrap) and one line per option
    header_wrapped = textwrap.wrap(header, width)
    header_height = len(header_wrapped)
    if header == '':
        header_height = 0
    height = len(options) + header_height

    # create an off-screen console that represents the menu's window
    window = Game.instance.ui.managed_console(width, height)

    # print the header, with wrapped text
    window.draw_rect(0, 0, width, height, None, fg=colors.white)
    for i, line in enumerate(header_wrapped):
        window.draw_str(0, 0 + i, header_wrapped[i])

    # print all the options
    y = header_height
    letter_index = ord('a')
    for option_text in options:
        text = '(' + chr(letter_index) + ') ' + option_text
        window.draw_str(0, y, text)
        y += 1
        letter_index += 1

    x = SCREEN_WIDTH // 2 - width // 2
    y = SCREEN_HEIGHT // 2 - height // 2

    Game.instance.ui.blit_at(window, x, y, width, height, 0, 0, bg_alpha=0.7)
    key = Game.instance.ui.wait_for_key()
    Game.instance.ui.unblit(window)

    key_char = key.text
    if key_char == '':
        key_char = ' '  # placeholder

    # convert the ASCII code to an index; if it corresponds to an option, return it
    index = ord(key_char) - ord('a')
    if 0 <= index < len(options):
        return index
    return None


def message_box(text, width=50):
    create_menu(text, [], width)


def inventory_menu(header):
    # show a menu with each item of the inventory as an option
    if len(Game.instance.inventory) == 0:
        options = ['Inventory is empty.']
    else:
        options = [item.name for item in Game.instance.inventory]

    index = create_menu(header, options, INVENTORY_WIDTH)

    # if an item was chosen, return it
    if index is None or len(Game.instance.inventory) == 0:
        return None
    return Game.instance.item_system.get(Game.instance.inventory[index])
