from game.handlers.common import (
    get_current_location_state,
    resolve_item,
    unequip_item,
    get_item_display_name,
)
from game.itemRegistry import itemRegistry


def handle_drop(command, game_state):
    item_name = command["object"]

    if not item_name:
        return "I don't know what I want to drop."

    inventory = game_state["player"]["inventory"]

    item_id, clarification = resolve_item(
        item_name,
        inventory,
    )

    if clarification:
        return clarification

    if not item_id:
        return f"You aren't carrying {item_name}."

    item = itemRegistry[item_id]

    display_name = get_item_display_name(
        item,
    )

    # Dropped items can no longer remain equipped.
    unequip_item(
        game_state,
        item_id,
    )

    inventory.remove(
        item_id,
    )

    location_state = get_current_location_state(
        game_state,
    )

    # None means the item is loose in the current area.
    location_state["items"][item_id] = None

    return item.get(
        "dropResponse",
        f"You drop the {display_name}.",
    )
