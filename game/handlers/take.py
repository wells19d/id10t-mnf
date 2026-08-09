from game.handlers.common import (
    can_access_scenery_contents,
    command_failure,
    find_scenery,
    get_current_location_state,
    get_item_display_name,
    get_items_in_scenery,
    get_scenery_state,
    get_visible_item_ids,
    resolve_item,
)
from game.itemRegistry import itemRegistry


def handle_take(command, current_area, game_state):
    item_name = command["object"]
    source_name = command["target"]

    if not item_name:
        return command_failure(
            "I don't know what I want to take.",
        )

    location_state = get_current_location_state(
        game_state,
    )

    # TAKE <item> FROM <scenery>
    if source_name:
        scenery_id, scenery_data = find_scenery(
            source_name,
            current_area,
        )

        if not scenery_data:
            return command_failure(
                f"I don't see a {source_name} here.",
            )

        scenery_state = get_scenery_state(
            location_state,
            scenery_id,
        )

        # Closed containers must be opened first.
        if scenery_data.get("openable") and not scenery_state.get(
            "isOpen",
            False,
        ):
            return command_failure(
                scenery_data.get(
                    "takeClosedResponse",
                    f"The {scenery_id} is closed.",
                )
            )

        # Other scenery conditions may also block
        # access to its contents.
        if not can_access_scenery_contents(
            scenery_data,
            scenery_state,
        ):
            return command_failure(
                scenery_data.get(
                    "takeBlockedResponse",
                    f"You can't reach anything in the {scenery_id} right now.",
                )
            )

        available_items = get_items_in_scenery(
            location_state,
            scenery_id,
        )

    # TAKE <item>
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
        return command_failure(
            clarification,
        )

    if not item_id:
        scenery_id, scenery_data = find_scenery(
            item_name,
            current_area,
        )

        if scenery_data:
            return command_failure(
                scenery_data.get(
                    "takeFail",
                    f"You can't take the {scenery_id}.",
                )
            )

        return command_failure(
            f"I don't see a {item_name} here.",
        )

    item = itemRegistry[item_id]

    display_name = get_item_display_name(item)

    if not item.get(
        "takeable",
        False,
    ):
        return command_failure(
            item.get(
                "takeFail",
                f"I can't take the {display_name}.",
            )
        )

    # Remove the item from its current world placement.
    location_state["items"].pop(
        item_id,
        None,
    )

    # Add it to inventory.
    game_state["player"]["inventory"].append(
        item_id,
    )

    return item.get(
        "takeResponse",
        f"You took the {display_name}.",
    )
