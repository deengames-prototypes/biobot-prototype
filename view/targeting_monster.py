def closest_monster(game, max_range):
    # find closest enemy, up to a maximum range, and in the player's FOV
    closest_enemy = None
    closest_dist = max_range + 1  # start with (slightly more than) maximum range

    for obj in game.area_map.entities:
        if game.fighter_system.has(obj) and game.fighter_system.get(obj).hostile and (obj.x, obj.y) in game.renderer.visible_tiles:
            # calculate distance between this object and the player
            dist = game.player.distance_to(obj)
            if dist < closest_dist:  # it's closer, so remember it
                closest_enemy = obj
                closest_dist = dist
    return closest_enemy
