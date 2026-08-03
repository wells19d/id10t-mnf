directionAliases = {
    "n": "north",
    "north": "north",
    "s": "south",
    "south": "south",
    "e": "east",
    "east": "east",
    "w": "west",
    "west": "west",
}


def move_player(direction, current_area, player_state):
    full_direction = directionAliases.get(direction)

    if not full_direction:
        return None

    next_location = current_area["exits"].get(full_direction)

    if not next_location:
        return f"I can't go {full_direction} from here."

    player_state["currentLocation"] = next_location
    player_state["lastDirection"] = full_direction
    player_state["lastShortDirection"] = full_direction[0]

    return next_location
