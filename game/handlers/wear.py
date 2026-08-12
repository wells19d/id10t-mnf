from game.handlers.common import (
    commandFailure,
    overflowCount,
    displayName,
    pendingPrompt,
    placeLooseItems,
    resolveItem,
)
from items.registry import itemRegistry


def handleWear(command, game_state):
    item_name = command["object"]

    if not item_name:
        return commandFailure(
            "I don't know what I want to wear.",
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
    display_name = displayName(item)

    if not item.get("wearable", False):
        return commandFailure(
            item.get(
                "wearFailResponse",
                f"You can't wear the {display_name}.",
            )
        )

    equipped = game_state["player"]["equipped"]
    item_slot = item.get("slot")

    equipped_item_id = None

    for equipped_item_id in equipped:
        equipped_item = itemRegistry.get(
            equipped_item_id,
        )

        if not equipped_item:
            continue

        if equipped_item.get("slot") == item_slot:
            break
    else:
        equipped_item_id = None

    if equipped_item_id:
        equipped_item = itemRegistry[equipped_item_id]

        if item_slot != "back":
            equipped_display_name = displayName(
                equipped_item,
            )

            return commandFailure(
                f"You are already wearing the {equipped_display_name}.",
            )

        final_inventory = [
            inventory_item_id
            for inventory_item_id in inventory
            if inventory_item_id != item_id
        ]
        final_inventory.append(
            equipped_item_id,
        )
        final_equipped = [
            current_equipped_item_id
            for current_equipped_item_id in equipped
            if current_equipped_item_id != equipped_item_id
        ]
        final_equipped.append(
            item_id,
        )

        if overflowCount(
            game_state["player"],
            final_inventory,
            final_equipped,
        ):
            game_state["pendingAction"] = {
                "type": "capacityChange",
                "action": "wear",
                "itemId": item_id,
                "equippedItemId": equipped_item_id,
                "locationId": game_state["player"]["currentLocation"],
            }

            return pendingPrompt(
                game_state,
            )

        game_state["player"]["inventory"] = final_inventory
        game_state["player"]["equipped"] = final_equipped

        return item.get(
            "wearResponse",
            f"You equip the {display_name}.",
        )

    inventory.remove(
        item_id,
    )
    equipped.append(
        item_id,
    )

    return item.get(
        "wearResponse",
        f"You put on the {display_name}.",
    )


def handleRemove(command, game_state):
    item_name = command["object"]

    if not item_name:
        return commandFailure(
            "I don't know what I want to remove.",
        )

    equipped = game_state["player"]["equipped"]

    item_id, clarification = resolveItem(
        item_name,
        equipped,
    )

    if clarification:
        return commandFailure(
            clarification,
        )

    if not item_id:
        return commandFailure(
            f"You aren't wearing {item_name}.",
        )

    item = itemRegistry[item_id]
    display_name = displayName(
        item,
    )

    inventory = game_state["player"]["inventory"]
    final_inventory = [
        *inventory,
        item_id,
    ]
    final_equipped = [
        equipped_item_id
        for equipped_item_id in equipped
        if equipped_item_id != item_id
    ]
    overflow_count = overflowCount(
        game_state["player"],
        final_inventory,
        final_equipped,
    )

    if overflow_count and item.get(
        "carryCapacity",
        0,
    ):
        game_state["pendingAction"] = {
            "type": "capacityChange",
            "action": "remove",
            "itemId": item_id,
            "locationId": game_state["player"]["currentLocation"],
        }

        return pendingPrompt(
            game_state,
        )

    if overflow_count:
        game_state["player"]["equipped"] = final_equipped
        placeLooseItems(
            game_state,
            [
                item_id,
            ],
        )

        return (
            f"You removed the {display_name}, but you don't have room to "
            "carry it, so you drop it on the ground."
        )

    game_state["player"]["inventory"] = final_inventory
    game_state["player"]["equipped"] = final_equipped

    return item.get(
        "removeResponse",
        f"You remove the {display_name}.",
    )
