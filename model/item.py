import colors
from game import Game
from model.helper_functions.message import message
from model.components.base import Component


class Item(Component):
    """
    an item that can be picked up and used.
    """
    def __init__(self, owner, use_function=None):
        super().__init__(owner)
        self.use_function = use_function

    def pick_up(self):
        """
        add to the player's inventory and remove from the map
        """
        if len(Game.instance.inventory) >= 26:
            message('Your inventory is full, cannot pick up ' +
                    self.owner.name + '.', colors.red)
        elif "arrows" in self.owner.name:
            # eg. 13 arrows
            num_arrows = int(self.owner.name[0:self.owner.name.index(' ')])
            Game.instance.player.arrows += num_arrows
            message("Picked up {} arrows. Total={}".format(num_arrows, Game.instance.player.arrows))
            Game.instance.area_map.entities.remove(self.owner)
        else:
            Game.instance.inventory.append(self.owner)
            Game.instance.area_map.entities.remove(self.owner)
            message('You picked up a ' + self.owner.name + '!', colors.green)

    def drop(self):
        """
        add to the map and remove from the player's inventory. also, place it at the player's coordinates
        """
        Game.instance.area_map.entities.append(self.owner)
        Game.instance.inventory.remove(self.owner)
        self.owner.x = Game.instance.player.x
        self.owner.y = Game.instance.player.y
        message('You dropped a ' + self.owner.name + '.', colors.yellow)

    def use(self):
        # just call the "use_function" if it is defined
        if self.use_function is None:
            message('The ' + self.owner.name + ' cannot be used.')
        else:
            if self.use_function() != 'cancelled':
                Game.instance.inventory.remove(self.owner)  # destroy after use, unless it was
                # cancelled for some reason


