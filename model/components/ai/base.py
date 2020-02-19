from game import Game
from model.components.base import Component


class AbstractAI(Component):
    """
    Base class for all AI components.
    """
    def __init__(self, owner, num_turns=None):
        super().__init__(owner)
        self.num_turns = num_turns
        self.take_turn = self._take_turn
        self.other = None

    def _take_turn(self):
        pass

    def cleanup(self):
        """optional method for temporary AIs"""

    def temporarily_switch_to(self, other):
        # This assertion is in place because permanent AIs have `num_turns` set to None.
        # On that note, it wouldn't make sense to set a permanent AI through this method,
        # which is why it only accepts temporary ones.
        assert isinstance(other.num_turns, int), "The passed AI's num_turns attribute can only be an int."

        if type(other) == type(self):  # If they're the same AI type, extend this one
            if self.num_turns is not None:
                self.num_turns += other.num_turns
                return
            # Else, continue on setting it anyway

        Game.instance.ai_system.set(self.owner, other)
        self.other = other

        other.take_turn = self.temporary_take_turn

    def temporary_take_turn(self):
        if self.other.num_turns > 0:
            self.other._take_turn()
        else:
            self.other.cleanup()
            Game.instance.ai_system.set(self.owner, self)
            self.take_turn()
