import textwrap

import colors
from constants import MSG_WIDTH, MSG_HEIGHT
from game import Game


def message(new_msg, color=colors.white):
    # split the message if necessary, among multiple lines
    new_msg_lines = textwrap.wrap(new_msg, MSG_WIDTH)

    for line in new_msg_lines:
        # if the buffer is full, remove the first line to make room for the new one
        if len(Game.instance.game_messages) == MSG_HEIGHT:
            del Game.instance.game_messages[0]

        # add the new line as a tuple, with the text and the color
        Game.instance.game_messages.append((line, color))
