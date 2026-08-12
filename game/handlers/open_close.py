from game.handlers.common import (
    applyChanges,
    addQuantityText,
    commandFailure,
    findScenery,
    currentLocation,
    getItemStateSnapshot,
    getSceneryState,
    visibleItemIds,
    resolveItem,
    stateMatches,
)
from items.registry import itemRegistry


def requirementsMet(
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

    if not stateMatches(
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
        if not stateMatches(
            game_state["flags"],
            required_flags,
        ):
            return False

    return True


def resolveAccessibleItemTarget(
    target,
    location_definition,
    game_state,
):
    accessible_item_ids = (
        visibleItemIds(
            location_definition,
            game_state,
        )
        + game_state["player"]["inventory"]
        + game_state["player"]["equipped"]
    )

    return resolveItem(
        target,
        accessible_item_ids,
    )


def handleOpenItem(
    target,
    location_definition,
    game_state,
):
    item_id, clarification = resolveAccessibleItemTarget(
        target,
        location_definition,
        game_state,
    )

    if clarification:
        return commandFailure(
            clarification,
        )

    item = itemRegistry.get(
        item_id,
    )

    if not item:
        return commandFailure(
            f"I don't see a {target} here.",
        )

    if not item.get(
        "openable",
        False,
    ):
        return commandFailure(
            item.get(
                "openFailResponse",
                f"You can't open the {target}.",
            )
        )

    item_state = getItemStateSnapshot(
        game_state,
        item_id,
    )

    if item_state.get(
        "isLocked",
        False,
    ):
        return commandFailure(
            item.get(
                "lockedResponse",
                f"The {target} is locked.",
            )
        )

    if item_state.get(
        "isOpen",
        False,
    ):
        return commandFailure(
            item.get(
                "alreadyOpenResponse",
                f"The {target} is already open.",
            )
        )

    if not requirementsMet(
        item.get(
            "openRequires",
            {},
        ),
        game_state,
        item_state,
    ):
        return commandFailure(
            item.get(
                "openBlockedResponse",
                f"You can't open the {target} right now.",
            )
        )

    item_state["isOpen"] = True
    applyChanges(
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

    return addQuantityText(
        response,
        item,
        item_state,
    )


def handleCloseItem(
    target,
    location_definition,
    game_state,
):
    item_id, clarification = resolveAccessibleItemTarget(
        target,
        location_definition,
        game_state,
    )

    if clarification:
        return commandFailure(
            clarification,
        )

    item = itemRegistry.get(
        item_id,
    )

    if not item:
        return commandFailure(
            f"I don't see a {target} here.",
        )

    if not item.get(
        "closeable",
        False,
    ):
        return commandFailure(
            item.get(
                "closeFailResponse",
                f"You can't close the {target}.",
            )
        )

    item_state = getItemStateSnapshot(
        game_state,
        item_id,
    )

    if not item_state.get(
        "isOpen",
        False,
    ):
        return commandFailure(
            item.get(
                "alreadyClosedResponse",
                f"The {target} is already closed.",
            )
        )

    if not requirementsMet(
        item.get(
            "closeRequires",
            {},
        ),
        game_state,
        item_state,
    ):
        return commandFailure(
            item.get(
                "closeBlockedResponse",
                f"You can't close the {target} right now.",
            )
        )

    item_state["isOpen"] = False
    applyChanges(
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


def _handleOpenScenery(
    scenery_id,
    scenery_data,
    game_state,
):
    if not scenery_data.get(
        "openable",
        False,
    ):
        return commandFailure(
            scenery_data.get(
                "openFailResponse",
                f"You can't open the {scenery_id}.",
            )
        )

    location_state = currentLocation(
        game_state,
    )

    scenery_state = getSceneryState(
        location_state,
        scenery_id,
    )

    # Broken objects cannot be opened normally.
    if scenery_state.get(
        "isBroken",
        False,
    ):
        return commandFailure(
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
        return commandFailure(
            scenery_data.get(
                "lockedResponse",
                f"The {scenery_id} is locked.",
            )
        )

    if scenery_state.get(
        "isOpen",
        False,
    ):
        return commandFailure(
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

    if not requirementsMet(
        requirements,
        game_state,
        scenery_state,
    ):
        return commandFailure(
            scenery_data.get(
                "openBlockedResponse",
                f"You can't open the {scenery_id} right now.",
            )
        )

    scenery_state["isOpen"] = True

    # Optional extra state changes caused by opening.
    applyChanges(
        scenery_state,
        scenery_data.get(
            "openEffects",
        ),
    )

    return scenery_data.get(
        "openResponse",
        f"You open the {scenery_id}.",
    )


def _handleCloseScenery(
    scenery_id,
    scenery_data,
    game_state,
):
    if not scenery_data.get(
        "closeable",
        False,
    ):
        return commandFailure(
            scenery_data.get(
                "closeFailResponse",
                f"You can't close the {scenery_id}.",
            )
        )

    location_state = currentLocation(
        game_state,
    )

    scenery_state = getSceneryState(
        location_state,
        scenery_id,
    )

    # Broken objects cannot be closed again.
    if scenery_state.get(
        "isBroken",
        False,
    ):
        return commandFailure(
            scenery_data.get(
                "brokenCloseResponse",
                f"The {scenery_id} is broken and can't be closed.",
            )
        )

    if not scenery_state.get(
        "isOpen",
        False,
    ):
        return commandFailure(
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

    if not requirementsMet(
        requirements,
        game_state,
        scenery_state,
    ):
        return commandFailure(
            scenery_data.get(
                "closeBlockedResponse",
                f"You can't close the {scenery_id} right now.",
            )
        )

    scenery_state["isOpen"] = False

    # Optional extra state changes caused by closing.
    applyChanges(
        scenery_state,
        scenery_data.get(
            "closeEffects",
        ),
    )

    return scenery_data.get(
        "closeResponse",
        f"You close the {scenery_id}.",
    )


def handleOpen(command, location_definition, game_state):
    target = command["object"] or command["target"]

    if not target:
        return commandFailure(
            "I don't know what I want to open.",
        )

    scenery_id, scenery_data = findScenery(
        target,
        location_definition,
    )

    if not scenery_data:
        return handleOpenItem(
            target,
            location_definition,
            game_state,
        )

    return _handleOpenScenery(
        scenery_id,
        scenery_data,
        game_state,
    )


def handleClose(command, location_definition, game_state):
    target = command["object"] or command["target"]

    if not target:
        return commandFailure(
            "I don't know what I want to close.",
        )

    scenery_id, scenery_data = findScenery(
        target,
        location_definition,
    )

    if not scenery_data:
        return handleCloseItem(
            target,
            location_definition,
            game_state,
        )

    return _handleCloseScenery(
        scenery_id,
        scenery_data,
        game_state,
    )
