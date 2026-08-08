from game.handlers.common import (
    find_scenery,
    get_visible_item_ids,
    resolve_item,
)
from game.itemRegistry import itemRegistry


def handle_look(command, current_area, game_state):
    target = command["target"] or command["object"]

    if not target:
        return current_area.get(
            "lookResponse",
            current_area["description"],
        )

    scenery_id, scenery_data = find_scenery(
        target,
        current_area,
    )

    if scenery_data:
        look_response = scenery_data.get("lookResponse")
        description = scenery_data.get("description")

        if look_response:
            return look_response

        if description:
            return description

        return f"There is nothing remarkable about the {target}."

    visible_items = (
        get_visible_item_ids(
            current_area,
            game_state,
        )
        + game_state["player"]["inventory"]
    )

    item_id, clarification = resolve_item(
        target,
        visible_items,
    )

    if clarification:
        return clarification

    if item_id:
        item = itemRegistry[item_id]

        look_response = item.get("lookResponse")
        description = item.get("description")

        if look_response:
            return look_response

        if description:
            return description

        return f"There is nothing remarkable about the {target}."

    return f"I don't see a {target} here."
