class ComponentSystem:
    """
    Base class for component systems.
    """
    def __init__(self):
        self.component_dict = {}

    def set(self, owner, component):
        self.component_dict[owner] = component

    def remove(self, owner):
        if owner in self.component_dict:
            del self.component_dict[owner] 

    def get(self, owner):
        return self.component_dict.get(owner, None)

    def has(self, owner):
        return self.get(owner) is not None
