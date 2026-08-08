from game.handlers.common import (
    get_current_area_state,
    get_current_location_state,
    get_scenery_state,
    state_matches,
)

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


def exit_requirements_met(
    exit_data,
    game_state,
):
    requirements = exit_data.get(
        "requires",
        {},
    )

    # No requirements means the exit is available.
    if not requirements:
        return True

    player_state = game_state["player"]

    # Required inventory items.
    for item_id in requirements.get(
        "inventory",
        [],
    ):
        if item_id not in player_state["inventory"]:
            return False

    # Required equipped items.
    for item_id in requirements.get(
        "equipped",
        [],
    ):
        if item_id not in player_state["equipped"]:
            return False

    # Required area flags.
    required_flags = requirements.get(
        "flags",
        {},
    )

    if required_flags:
        area_state = get_current_area_state(
            game_state,
        )

        if not state_matches(
            area_state["flags"],
            required_flags,
        ):
            return False

    # Required scenery states in the current location.
    required_scenery = requirements.get(
        "sceneryState",
        {},
    )

    if required_scenery:
        location_state = get_current_location_state(
            game_state,
        )

        for scenery_id, required_state in required_scenery.items():
            scenery_state = get_scenery_state(
                location_state,
                scenery_id,
            )

            if not state_matches(
                scenery_state,
                required_state,
            ):
                return False

    return True


def move_player(
    direction,
    current_area,
    player_state,
    game_state=None,
):
    full_direction = directionAliases.get(
        direction,
    )

    if not full_direction:
        return None

    exit_data = current_area["exits"].get(
        full_direction,
    )

    if not exit_data:
        return f"I can't go {full_direction} from here."

    next_area = None

    # Standard exit:
    #
    # "north": "clearing"
    if isinstance(
        exit_data,
        str,
    ):
        next_location = exit_data

    # Conditional / cross-area exit:
    #
    # "north": {
    #     "location": "admin_grounds",
    #     "area": "area2",
    #     "requires": {...},
    #     "blockedResponse": "...",
    # }
    elif isinstance(
        exit_data,
        dict,
    ):
        next_location = exit_data.get(
            "location",
        )

        next_area = exit_data.get(
            "area",
        )

        if not next_location:
            return f"I can't go {full_direction} from here."

        if game_state is not None:
            if not exit_requirements_met(
                exit_data,
                game_state,
            ):
                return exit_data.get(
                    "blockedResponse",
                    f"You can't go {full_direction} from here.",
                )

    else:
        return f"I can't go {full_direction} from here."

    # Change major game area when the exit specifies one.
    if next_area:
        player_state["currentArea"] = next_area

    player_state["currentLocation"] = next_location
    player_state["lastDirection"] = full_direction
    player_state["lastShortDirection"] = full_direction[0]

    return next_location
