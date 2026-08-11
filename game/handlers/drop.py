from game.handlers.common import (
    command_failure,
    get_carry_overflow_count,
    get_current_location_state,
    get_item_display_name,
    get_pending_action_prompt,
    resolve_item,
)
from items.itemRegistry import itemRegistry


def resolve_drop_item(item_name, player_state):
    item_id, clarification = resolve_item(
        item_name,
        player_state["inventory"],
        include_match_names=True,
    )

    if item_id or clarification:
        return item_id, clarification, False

    item_id, clarification = resolve_item(
        item_name,
        player_state["equipped"],
        include_match_names=True,
    )

    return item_id, clarification, bool(item_id)


def handle_drop(command, game_state):
    item_name = command["object"]

    if not item_name:
        return command_failure(
            "I don't know what I want to drop.",
        )

    player_state = game_state["player"]
    inventory = player_state["inventory"]
    equipped = player_state["equipped"]

    item_id, clarification, is_equipped = resolve_drop_item(
        item_name,
        player_state,
    )

    if clarification:
        return command_failure(
            clarification,
        )

    if not item_id:
        return command_failure(
            f"You aren't carrying or wearing {item_name}.",
        )

    item = itemRegistry[item_id]

    display_name = get_item_display_name(
        item,
    )

    if is_equipped:
        final_equipped = [
            equipped_item_id
            for equipped_item_id in equipped
            if equipped_item_id != item_id
        ]

        if item.get("carryCapacity", 0) and get_carry_overflow_count(
            game_state["player"],
            inventory,
            final_equipped,
        ):
            game_state["pendingAction"] = {
                "type": "capacityChange",
                "action": "drop",
                "itemId": item_id,
                "locationId": game_state["player"]["currentLocation"],
            }

            return get_pending_action_prompt(
                game_state,
            )

        game_state["pendingAction"] = {
            "type": "equippedDrop",
            "action": "drop",
            "itemId": item_id,
            "locationId": player_state["currentLocation"],
        }

        return get_pending_action_prompt(
            game_state,
        )
    else:
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
