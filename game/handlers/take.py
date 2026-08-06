from game.handlers.common import (
    find_scenery,
    get_current_location_state,
    get_item_name,
    get_visible_item_ids,
    resolve_item,
)
from game.itemRegistry import itemRegistry


def handle_take(command, current_area, game_state):
    item_name = command["object"]
    source_name = command["target"]

    if not item_name:
        return "I don't know what I want to take."

    location_state = get_current_location_state(game_state)

    if source_name:
        scenery_id, scenery_data = find_scenery(
            source_name,
            current_area,
        )

        if not scenery_data:
            return f"I don't see a {source_name} here."

        scenery_state = location_state.get(
            "scenery",
            {},
        ).get(
            scenery_id,
            {},
        )

        if scenery_data.get("openable") and not scenery_state.get("isOpen", False):
            return scenery_data.get(
                "takeClosedResponse",
                f"The {scenery_id} is closed.",
            )

        available_items = [
            item_id
            for item_id in scenery_data.get("items", [])
            if item_id in location_state["itemsAvailable"]
        ]

    else:
        available_items = get_visible_item_ids(
            current_area,
            game_state,
        )

    item_id, clarification = resolve_item(
        item_name,
        available_items,
    )

    if clarification:
        return clarification

    if not item_id:
        scenery_id, scenery_data = find_scenery(
            item_name,
            current_area,
        )

        if scenery_data:
            return scenery_data.get(
                "takeFail",
                f"You can't take the {scenery_id}.",
            )

        return f"I don't see a {item_name} here."

    item = itemRegistry[item_id]
    display_name = get_item_name(item)

    area_item = current_area.get(
        "itemDescriptions",
        {},
    ).get(
        item_id,
        {},
    )

    if not item.get("takeable", False):
        return area_item.get(
            "takeFail",
            item.get(
                "takeFail",
                f"I can't take the {display_name}.",
            ),
        )

    location_state["itemsAvailable"].remove(item_id)

    if item_id not in location_state.setdefault(
        "itemsFound",
        [],
    ):
        location_state["itemsFound"].append(item_id)

    game_state["player"]["inventory"].append(item_id)

    return area_item.get(
        "takeResponse",
        item.get(
            "takeResponse",
            f"You take the {display_name}.",
        ),
    )
