from game.handlers.common import (
    find_scenery,
    get_current_location_state,
    get_item_name,
    resolve_item,
)
from game.itemRegistry import itemRegistry


def handle_throw(command, current_area, game_state):
    item_name = command["object"]
    target = command["target"]

    if not item_name:
        return "I don't know what I want to throw."

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
    display_name = get_item_name(item)
    throw_actions = item.get("onThrow")

    if not throw_actions:
        return f"You can't throw the {display_name}."

    if target:
        scenery_id, scenery_data = find_scenery(
            target,
            current_area,
        )

        if not scenery_data:
            return f"I don't see a {target} here."

        target = scenery_id

    throw_action = throw_actions.get(
        target,
        throw_actions.get("default"),
    )

    if not throw_action:
        return f"You can't throw the {display_name} here."

    inventory.remove(item_id)

    if not throw_action.get("destroyItem", False):
        location_state = get_current_location_state(game_state)

        if item_id not in location_state["itemsAvailable"]:
            location_state["itemsAvailable"].append(item_id)

    return throw_action["response"]
