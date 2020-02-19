from game import Game


def get_names_under_mouse():
    # create a list with the names of all objects at the mouse's coordinates and in FOV
    names = [obj.name for obj in get_objects_under_mouse()]

    names = ', '.join(names)  # join the names, separated by commas
    return names.capitalize()


def get_objects_under_mouse():
    (x, y) = Game.instance.mouse_coord

    # create a list with the names of all objects at the mouse's coordinates and in FOV
    stuff = [obj for obj in Game.instance.area_map.entities
             if obj.x == x and obj.y == y and (obj.x, obj.y) in Game.instance.renderer.visible_tiles]

    return stuff
