from game.handlers.common import (
    apply_state_changes,
    append_item_quantity_description,
    command_failure,
    find_scenery,
    get_current_location_state,
    get_item_state_snapshot,
    get_scenery_state,
    get_visible_item_ids,
    resolve_item,
    state_matches,
)
from items.itemRegistry import itemRegistry


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

    return True


def resolve_accessible_item_target(
    target,
    location_definition,
    game_state,
):
    accessible_item_ids = (
        get_visible_item_ids(
            location_definition,
            game_state,
        )
        + game_state["player"]["inventory"]
        + game_state["player"]["equipped"]
    )

    return resolve_item(
        target,
        accessible_item_ids,
    )


def handle_open_item(
    target,
    location_definition,
    game_state,
):
    item_id, clarification = resolve_accessible_item_target(
        target,
        location_definition,
        game_state,
    )

    if clarification:
        return command_failure(
            clarification,
        )

    item = itemRegistry.get(
        item_id,
    )

    if not item:
        return command_failure(
            f"I don't see a {target} here.",
        )

    if not item.get(
        "openable",
        False,
    ):
        return command_failure(
            item.get(
                "openFailResponse",
                f"You can't open the {target}.",
            )
        )

    item_state = get_item_state_snapshot(
        game_state,
        item_id,
    )

    if item_state.get(
        "isLocked",
        False,
    ):
        return command_failure(
            item.get(
                "lockedResponse",
                f"The {target} is locked.",
            )
        )

    if item_state.get(
        "isOpen",
        False,
    ):
        return command_failure(
            item.get(
                "alreadyOpenResponse",
                f"The {target} is already open.",
            )
        )

    if not requirements_met(
        item.get(
            "openRequires",
            {},
        ),
        game_state,
        item_state,
    ):
        return command_failure(
            item.get(
                "openBlockedResponse",
                f"You can't open the {target} right now.",
            )
        )

    item_state["isOpen"] = True
    apply_state_changes(
        item_state,
        item.get(
            "openEffects",
        ),
    )
    game_state["itemStates"][item_id] = item_state

    response = item.get(
        "openResponse",
        f"You open the {target}.",
    )

    return append_item_quantity_description(
        response,
        item,
        item_state,
    )


def handle_close_item(
    target,
    location_definition,
    game_state,
):
    item_id, clarification = resolve_accessible_item_target(
        target,
        location_definition,
        game_state,
    )

    if clarification:
        return command_failure(
            clarification,
        )

    item = itemRegistry.get(
        item_id,
    )

    if not item:
        return command_failure(
            f"I don't see a {target} here.",
        )

    if not item.get(
        "closeable",
        False,
    ):
        return command_failure(
            item.get(
                "closeFailResponse",
                f"You can't close the {target}.",
            )
        )

    item_state = get_item_state_snapshot(
        game_state,
        item_id,
    )

    if not item_state.get(
        "isOpen",
        False,
    ):
        return command_failure(
            item.get(
                "alreadyClosedResponse",
                f"The {target} is already closed.",
            )
        )

    if not requirements_met(
        item.get(
            "closeRequires",
            {},
        ),
        game_state,
        item_state,
    ):
        return command_failure(
            item.get(
                "closeBlockedResponse",
                f"You can't close the {target} right now.",
            )
        )

    item_state["isOpen"] = False
    apply_state_changes(
        item_state,
        item.get(
            "closeEffects",
        ),
    )
    game_state["itemStates"][item_id] = item_state

    return item.get(
        "closeResponse",
        f"You close the {target}.",
    )


def _handle_open_scenery(
    scenery_id,
    scenery_data,
    game_state,
):
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


def _handle_close_scenery(
    scenery_id,
    scenery_data,
    game_state,
):
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


def handle_open(command, location_definition, game_state):
    target = command["object"] or command["target"]

    if not target:
        return command_failure(
            "I don't know what I want to open.",
        )

    scenery_id, scenery_data = find_scenery(
        target,
        location_definition,
    )

    if not scenery_data:
        return handle_open_item(
            target,
            location_definition,
            game_state,
        )

    return _handle_open_scenery(
        scenery_id,
        scenery_data,
        game_state,
    )


def handle_close(command, location_definition, game_state):
    target = command["object"] or command["target"]

    if not target:
        return command_failure(
            "I don't know what I want to close.",
        )

    scenery_id, scenery_data = find_scenery(
        target,
        location_definition,
    )

    if not scenery_data:
        return handle_close_item(
            target,
            location_definition,
            game_state,
        )

    return _handle_close_scenery(
        scenery_id,
        scenery_data,
        game_state,
    )
