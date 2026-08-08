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
        return scenery_data.get(
            "lookResponse",
            scenery_data["description"],
        )

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

        return item.get(
            "lookResponse",
            item["description"],
        )

    return f"There is nothing remarkable about the {target}."
