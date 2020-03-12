from game import Game
from difficulty import Difficulty
import copy
import pickle

class SaveManager:
    def __init__(self, game):
        self.game = game

    def save(self):
        # open a new empty shelve (possibly overwriting an old one) to write the game data
        to_pickle = copy.copy(Game.instance)

        for attr_to_remove in self.game._dont_pickle:
            if hasattr(to_pickle, attr_to_remove):
                delattr(to_pickle, attr_to_remove)

        with open('savegame', 'wb') as f:
            pickle.dump(to_pickle, f, pickle.HIGHEST_PROTOCOL)
        
        Difficulty.instance.save()

    def load(self):
        # open the previously saved shelve and load the game data
        with open('savegame', 'rb') as f:
            Game.instance.__dict__.update(pickle.load(f).__dict__)

        # learn skills and set up keybindings
        Game.instance.player.set_skills()
        Difficulty.instance.load()
