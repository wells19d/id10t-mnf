from game.handlers.common import (
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

    # Required world or event flags.
    required_flags = requirements.get(
        "flags",
        {},
    )

    if required_flags:
        if not state_matches(
            game_state["flags"],
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
    location_definition,
    player_state,
    game_state=None,
):
    full_direction = directionAliases.get(
        direction,
    )

    if not full_direction:
        return None

    exit_data = location_definition["exits"].get(
        full_direction,
    )

    if not exit_data:
        return f"I can't go {full_direction} from here."

    # Standard exit:
    #
    # "north": "a1_clearing"
    if isinstance(
        exit_data,
        str,
    ):
        next_location = exit_data

    # Conditional exit:
    #
    # "north": {
    #     "location": "admin_grounds",
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

    player_state["currentLocation"] = next_location
    player_state["lastDirection"] = full_direction
    player_state["lastShortDirection"] = full_direction[0]

    return next_location
