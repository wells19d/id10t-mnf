from game.handlers.common import (
    command_failure,
    get_item_display_name,
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

    if item_id in equipped:
        return command_failure(
            item.get(
                "alreadyWearingResponse",
                f"You are already wearing the {display_name}.",
            )
        )

    for equipped_item_id in equipped:
        equipped_item = itemRegistry.get(
            equipped_item_id,
        )

        if not equipped_item:
            continue

        if equipped_item.get("slot") == item_slot:
            equipped_display_name = get_item_display_name(
                equipped_item,
            )

            return command_failure(
                f"You are already wearing the {equipped_display_name}.",
            )

    equipped.append(item_id)

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

    equipped.remove(
        item_id,
    )

    return item.get(
        "removeResponse",
        f"You remove the {display_name}.",
    )
