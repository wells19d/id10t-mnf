from game.handlers.common import (
    command_failure,
    get_carry_overflow_count,
    get_item_display_name,
    get_pending_action_prompt,
    place_items_loose,
    resolve_item,
)
from items.itemRegistry import itemRegistry


def handle_wear(command, game_state):
    item_name = command["object"]

    if not item_name:
        return command_failure(
            "I don't know what I want to wear.",
        )

    inventory = game_state["player"]["inventory"]

    item_id, clarification = resolve_item(
        item_name,
        inventory,
    )

    if clarification:
        return command_failure(
            clarification,
        )

    if not item_id:
        return command_failure(
            f"You aren't carrying {item_name}.",
        )

    item = itemRegistry[item_id]
    display_name = get_item_display_name(item)

    if not item.get("wearable", False):
        return command_failure(
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
            equipped_display_name = get_item_display_name(
                equipped_item,
            )

            return command_failure(
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

        if get_carry_overflow_count(
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

            return get_pending_action_prompt(
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


def handle_remove(command, game_state):
    item_name = command["object"]

    if not item_name:
        return command_failure(
            "I don't know what I want to remove.",
        )

    equipped = game_state["player"]["equipped"]

    item_id, clarification = resolve_item(
        item_name,
        equipped,
    )

    if clarification:
        return command_failure(
            clarification,
        )

    if not item_id:
        return command_failure(
            f"You aren't wearing {item_name}.",
        )

    item = itemRegistry[item_id]
    display_name = get_item_display_name(
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
    overflow_count = get_carry_overflow_count(
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

        return get_pending_action_prompt(
            game_state,
        )

    if overflow_count:
        game_state["player"]["equipped"] = final_equipped
        place_items_loose(
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
