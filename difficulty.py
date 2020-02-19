class Difficulty:
    instance = None

    def __init__(self):
        Difficulty.instance = self
        self.current_difficulty = 1000