from game.handlers.common import (
    apply_state_changes,
    command_failure,
    find_scenery,
    get_current_area_state,
    get_current_location_state,
    get_scenery_state,
    state_matches,
)


def requirements_met(
    requirements,
    game_state,
    scenery_state,
):
    if not requirements:
        return True

    player_state = game_state["player"]

    # Required state of this scenery.
    required_scenery_state = requirements.get(
        "sceneryState",
        {},
    )

    if not state_matches(
        scenery_state,
        required_scenery_state,
    ):
        return False

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

    return True


def handle_open(command, current_area, game_state):
    target = command["object"] or command["target"]

    if not target:
        return command_failure(
            "I don't know what I want to open.",
        )

    scenery_id, scenery_data = find_scenery(
        target,
        current_area,
    )

    if not scenery_data:
        return command_failure(
            f"I don't see a {target} here.",
        )

    if not scenery_data.get(
        "openable",
        False,
    ):
        return command_failure(
            scenery_data.get(
                "openFailResponse",
                f"You can't open the {scenery_id}.",
            )
        )

    location_state = get_current_location_state(
        game_state,
    )

    scenery_state = get_scenery_state(
        location_state,
        scenery_id,
    )

    # Broken objects cannot be opened normally.
    if scenery_state.get(
        "isBroken",
        False,
    ):
        return command_failure(
            scenery_data.get(
                "brokenOpenResponse",
                f"The {scenery_id} is already broken open.",
            )
        )

    # Standard locked state.
    if scenery_state.get(
        "isLocked",
        False,
    ):
        return command_failure(
            scenery_data.get(
                "lockedResponse",
                f"The {scenery_id} is locked.",
            )
        )

    if scenery_state.get(
        "isOpen",
        False,
    ):
        return command_failure(
            scenery_data.get(
                "alreadyOpenResponse",
                f"The {scenery_id} is already open.",
            )
        )

    # Optional additional requirements.
    requirements = scenery_data.get(
        "openRequires",
        {},
    )

    if not requirements_met(
        requirements,
        game_state,
        scenery_state,
    ):
        return command_failure(
            scenery_data.get(
                "openBlockedResponse",
                f"You can't open the {scenery_id} right now.",
            )
        )

    scenery_state["isOpen"] = True

    # Optional extra state changes caused by opening.
    apply_state_changes(
        scenery_state,
        scenery_data.get(
            "openEffects",
        ),
    )

    return scenery_data.get(
        "openResponse",
        f"You open the {scenery_id}.",
    )


def handle_close(command, current_area, game_state):
    target = command["object"] or command["target"]

    if not target:
        return command_failure(
            "I don't know what I want to close.",
        )

    scenery_id, scenery_data = find_scenery(
        target,
        current_area,
    )

    if not scenery_data:
        return command_failure(
            f"I don't see a {target} here.",
        )

    if not scenery_data.get(
        "closeable",
        False,
    ):
        return command_failure(
            scenery_data.get(
                "closeFailResponse",
                f"You can't close the {scenery_id}.",
            )
        )

    location_state = get_current_location_state(
        game_state,
    )

    scenery_state = get_scenery_state(
        location_state,
        scenery_id,
    )

    # Broken objects cannot be closed again.
    if scenery_state.get(
        "isBroken",
        False,
    ):
        return command_failure(
            scenery_data.get(
                "brokenCloseResponse",
                f"The {scenery_id} is broken and can't be closed.",
            )
        )

    if not scenery_state.get(
        "isOpen",
        False,
    ):
        return command_failure(
            scenery_data.get(
                "alreadyClosedResponse",
                f"The {scenery_id} is already closed.",
            )
        )

    # Optional additional requirements.
    requirements = scenery_data.get(
        "closeRequires",
        {},
    )

    if not requirements_met(
        requirements,
        game_state,
        scenery_state,
    ):
        return command_failure(
            scenery_data.get(
                "closeBlockedResponse",
                f"You can't close the {scenery_id} right now.",
            )
        )

    scenery_state["isOpen"] = False

    # Optional extra state changes caused by closing.
    apply_state_changes(
        scenery_state,
        scenery_data.get(
            "closeEffects",
        ),
    )

    return scenery_data.get(
        "closeResponse",
        f"You close the {scenery_id}.",
    )
