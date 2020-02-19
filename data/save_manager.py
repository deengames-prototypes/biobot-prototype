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
        
        with open('current_difficulty', 'w') as f:
            data = str(Difficulty.instance.current_difficulty)
            f.writelines(data)
        print("Saved; difficulty is {}".format(Difficulty.instance.current_difficulty))

    def load(self):
        # open the previously saved shelve and load the game data
        with open('savegame', 'rb') as f:
            Game.instance.__dict__.update(pickle.load(f).__dict__)

        with open('current_difficulty', 'r') as f:
            difficulty = int(f.readline())

        Difficulty.instance.current_difficulty = difficulty
        print("Loaded; difficulty is {}".format(difficulty))