def closest_monster(game, max_range):
    # find closest enemy, up to a maximum range, and in the player's FOV
    closest_enemy = None
    closest_dist = max_range + 1  # start with (slightly more than) maximum range

    for obj in game.instance.area_map.entities:
        if game.instance.fighter_system.has(obj) and game.instance.fighter_system.get(obj).hostile and (obj.x, obj.y) in game.instance.renderer.visible_tiles:
            # calculate distance between this object and the player
            dist = game.instance.player.distance_to(obj)
            if dist < closest_dist:  # it's closer, so remember it
                closest_enemy = obj
                closest_dist = dist
    return closest_enemy
