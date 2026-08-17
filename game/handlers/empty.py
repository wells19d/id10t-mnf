from game.handlers.common import (
    applyChanges,
    commandFailure,
    displayName,
    getItemStateSnapshot,
    resolveItem,
    stateMatches,
)
from items.registry import itemRegistry


def handleEmpty(command, game_state):
    item_name = command["object"]

    if not item_name:
        return commandFailure(
            "I don't know what I want to empty.",
        )

    if command["target"]:
        return commandFailure(
            "Use the item on a target if you want to affect it.",
        )

    inventory = game_state["player"]["inventory"]

    item_id, clarification = resolveItem(
        item_name,
        inventory,
    )

    if clarification:
        return commandFailure(
            clarification,
        )

    if not item_id:
        return commandFailure(
            f"You aren't carrying {item_name}.",
        )

    item = itemRegistry[item_id]
    display_name = displayName(
        item,
    )
    empty_actions = item.get(
        "emptyActions",
        [],
    )

    if not empty_actions:
        return commandFailure(
            f"You can't empty the {display_name}.",
        )

    item_state = getItemStateSnapshot(
        game_state,
        item_id,
    )

    for empty_action in empty_actions:
        if not stateMatches(
            item_state,
            empty_action["requiresState"],
        ):
            continue

        applyChanges(
            item_state,
            empty_action["effects"],
        )
        game_state["itemStates"][item_id] = item_state

        return empty_action["response"]

    return commandFailure(
        item.get(
            "emptyFailResponse",
            f"The {display_name} is already empty.",
        )
    )
