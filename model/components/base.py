class Component:
    """
    Basic class describing a component.

    Since all components inherit from this, it shouldn't be passed to GameObject's get_component method;
    lest it returns a random component.

    Class Attributes:
        component_type (str): Defines the component slot; used for defining mutually exclusive components

    Attributes:
        owner (GameObject): The object who this component belongs to
    """
    def __init__(self, owner):
        self.owner = owner
