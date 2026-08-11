from game.handlers.common import (
    can_access_item_contents,
    can_access_scenery_contents,
    command_failure,
    find_scenery,
    get_carry_overflow_count,
    get_current_location_state,
    get_item_display_name,
    get_item_state_snapshot,
    get_items_in_item_container,
    get_items_in_scenery,
    get_pending_action_prompt,
    get_scenery_state,
    get_visible_item_ids,
    resolve_item,
)
from items.itemRegistry import itemRegistry


def handle_take(command, location_definition, game_state):
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
            location_definition,
        )

        if scenery_data:
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
        else:
            accessible_items = (
                get_visible_item_ids(
                    location_definition,
                    game_state,
                )
                + game_state["player"]["inventory"]
                + game_state["player"]["equipped"]
            )
            container_item_id, clarification = resolve_item(
                source_name,
                accessible_items,
            )

            if clarification:
                return command_failure(
                    clarification,
                )

            container_item = itemRegistry.get(
                container_item_id,
            )

            if not container_item or not container_item.get(
                "container",
                False,
            ):
                return command_failure(
                    f"I don't see a {source_name} here.",
                )

            container_state = get_item_state_snapshot(
                game_state,
                container_item_id,
            )

            if not can_access_item_contents(
                container_item,
                container_state,
            ):
                return command_failure(
                    container_item.get(
                        "takeBlockedResponse",
                        f"You can't reach anything in the {source_name} right now.",
                    )
                )

            available_items = get_items_in_item_container(
                location_state,
                container_item_id,
            )

    # TAKE <item>
    else:
        available_items = get_visible_item_ids(
            location_definition,
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
            location_definition,
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

    player_state = game_state["player"]
    inventory = player_state["inventory"]
    contained_item_ids = []

    if item.get(
        "transferContentsOnTake",
        False,
    ):
        contained_item_ids = get_items_in_item_container(
            location_state,
            item_id,
        )

    acquired_item_ids = [
        item_id,
        *contained_item_ids,
    ]
    final_inventory = [
        *inventory,
        *acquired_item_ids,
    ]

    overflow_count = get_carry_overflow_count(
        player_state,
        final_inventory,
    )

    if overflow_count and contained_item_ids and overflow_count <= len(inventory):
        game_state["pendingAction"] = {
            "type": "takeOverflow",
            "action": "take",
            "itemId": item_id,
            "locationId": player_state["currentLocation"],
        }

        return get_pending_action_prompt(
            game_state,
        )

    if overflow_count:
        return command_failure(
            "You can't carry anything else.",
        )

    # Remove the complete acquisition bundle from its
    # current world placements.
    for acquired_item_id in acquired_item_ids:
        location_state["items"].pop(
            acquired_item_id,
            None,
        )

    # A taken container is emptied into normal inventory.
    inventory.extend(
        acquired_item_ids,
    )

    return item.get(
        "takeResponse",
        f"You took the {display_name}.",
    )
