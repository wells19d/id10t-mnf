from game.handlers.common import (
    command_failure,
    get_item_display_name,
    resolve_item,
)
from game.itemRegistry import itemRegistry


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

    for equipped_item_id in list(equipped):
        equipped_item = itemRegistry[equipped_item_id]

        if equipped_item.get("slot") == item_slot:
            equipped.remove(equipped_item_id)

    if item_id not in equipped:
        equipped.append(item_id)

    return item.get(
        "wearResponse",
        f"You put on the {display_name}.",
    )
