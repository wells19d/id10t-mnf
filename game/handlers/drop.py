from game.handlers.common import (
    commandFailure,
    overflowCount,
    currentLocation,
    displayName,
    pendingPrompt,
    resolveItem,
)
from items.registry import itemRegistry


def resolveDropItem(item_name, player_state):
    item_id, clarification = resolveItem(
        item_name,
        player_state["inventory"],
        include_match_names=True,
    )

    if item_id or clarification:
        return item_id, clarification, False

    item_id, clarification = resolveItem(
        item_name,
        player_state["equipped"],
        include_match_names=True,
    )

    return item_id, clarification, bool(item_id)


def handleDrop(command, game_state):
    item_name = command["object"]

    if not item_name:
        return commandFailure(
            "I don't know what I want to drop.",
        )

    player_state = game_state["player"]
    inventory = player_state["inventory"]
    equipped = player_state["equipped"]

    item_id, clarification, is_equipped = resolveDropItem(
        item_name,
        player_state,
    )

    if clarification:
        return commandFailure(
            clarification,
        )

    if not item_id:
        return commandFailure(
            f"You aren't carrying or wearing {item_name}.",
        )

    item = itemRegistry[item_id]

    display_name = displayName(
        item,
    )

    if is_equipped:
        final_equipped = [
            equipped_item_id
            for equipped_item_id in equipped
            if equipped_item_id != item_id
        ]

        if item.get("carryCapacity", 0) and overflowCount(
            game_state["player"],
            inventory,
            final_equipped,
        ):
            game_state["pendingAction"] = {
                "type": "capacityChange",
                "action": "drop",
                "itemId": item_id,
                "locationId": game_state["player"]["currentLocation"],
            }

            return pendingPrompt(
                game_state,
            )

        game_state["pendingAction"] = {
            "type": "equippedDrop",
            "action": "drop",
            "itemId": item_id,
            "locationId": player_state["currentLocation"],
        }

        return pendingPrompt(
            game_state,
        )
    else:
        inventory.remove(
            item_id,
        )

    location_state = currentLocation(
        game_state,
    )

    # None means the item is loose in the current area.
    location_state["items"][item_id] = None

    return item.get(
        "dropResponse",
        f"You drop the {display_name}.",
    )
