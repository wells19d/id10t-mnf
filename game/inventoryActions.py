import random

from game.itemAccess import get_items_in_item_container
from game.itemPresentation import (
    append_narrator_response,
    get_formatted_item_list,
    get_item_display_name,
)
from game.worldState import get_current_location_state
from items.itemRegistry import itemRegistry
from states.gameState import (
    get_total_carry_capacity,
    is_valid_pending_action,
)


def get_carry_overflow_count(
    player_state,
    inventory=None,
    equipped=None,
):
    final_inventory = inventory if inventory is not None else player_state["inventory"]
    final_equipped = equipped if equipped is not None else player_state["equipped"]

    final_player_state = {
        **player_state,
        "inventory": final_inventory,
        "equipped": final_equipped,
    }

    return max(
        0,
        len(final_inventory)
        - get_total_carry_capacity(
            final_player_state,
        ),
    )


def select_overflow_items(
    inventory,
    overflow_count,
):
    if overflow_count <= 0:
        return []

    return random.sample(
        inventory,
        overflow_count,
    )


def place_items_loose(
    game_state,
    item_ids,
):
    if not item_ids:
        return

    location_state = get_current_location_state(
        game_state,
    )

    for item_id in item_ids:
        location_state["items"][item_id] = None


def get_pending_action_prompt(game_state):
    pending_action = game_state.get(
        "pendingAction",
    )

    if not pending_action:
        return None

    player_state = game_state["player"]
    action = pending_action["action"]
    item_id = pending_action["itemId"]
    item_name = get_item_display_name(
        itemRegistry[item_id],
    )

    if pending_action["type"] == "takeOverflow":
        location_state = get_current_location_state(
            game_state,
        )
        contained_item_ids = get_items_in_item_container(
            location_state,
            item_id,
        )
        final_inventory = [
            *player_state["inventory"],
            item_id,
            *contained_item_ids,
        ]
        overflow_count = get_carry_overflow_count(
            player_state,
            final_inventory,
        )

        return (
            f"Taking the {item_name} and everything still inside it will "
            f"require {overflow_count} carried "
            f"{'item' if overflow_count == 1 else 'items'} to be dropped. "
            "Continue? Yes or No."
        )

    if pending_action["type"] == "equippedDrop":
        return (
            f"The {item_name} is currently equipped. "
            "Drop it anyway? Yes or No."
        )

    if action == "wear":
        equipped_item_id = pending_action["equippedItemId"]
        equipped_item_name = get_item_display_name(
            itemRegistry[equipped_item_id],
        )
        final_inventory = [
            inventory_item_id
            for inventory_item_id in player_state["inventory"]
            if inventory_item_id != item_id
        ]
        final_equipped = [
            equipped_id
            for equipped_id in player_state["equipped"]
            if equipped_id != equipped_item_id
        ]
        final_equipped.append(
            item_id,
        )
        additional_drop_count = get_carry_overflow_count(
            player_state,
            final_inventory,
            final_equipped,
        )

        if additional_drop_count:
            drop_description = (
                f"the {equipped_item_name} and {additional_drop_count} "
                f"additional carried "
                f"{'item' if additional_drop_count == 1 else 'items'}"
            )
        else:
            drop_description = f"the {equipped_item_name}"

        return (
            f"The {item_name} has less carrying space. Equipping it will "
            f"cause {drop_description} to be dropped on the ground. "
            "Continue? Yes or No."
        )

    final_equipped = [
        equipped_id
        for equipped_id in player_state["equipped"]
        if equipped_id != item_id
    ]

    if action == "remove":
        final_inventory = [
            *player_state["inventory"],
            item_id,
        ]
        overflow_count = get_carry_overflow_count(
            player_state,
            final_inventory,
            final_equipped,
        )

        return (
            f"Removing the {item_name} will reduce your carrying space and "
            f"cause {overflow_count} carried "
            f"{'item' if overflow_count == 1 else 'items'} to fall to the "
            "ground. Continue? Yes or No."
        )

    overflow_count = get_carry_overflow_count(
        player_state,
        player_state["inventory"],
        final_equipped,
    )

    return (
        f"Dropping the {item_name} will reduce your carrying space and cause "
        f"{overflow_count} additional carried "
        f"{'item' if overflow_count == 1 else 'items'} to fall to the ground. "
        "Continue? Yes or No."
    )


def execute_pending_action(game_state):
    pending_action = game_state["pendingAction"]
    player_state = game_state["player"]

    if not is_valid_pending_action(
        pending_action,
        game_state,
    ):
        game_state["pendingAction"] = None

        return "That pending action can no longer be completed."

    action = pending_action["action"]
    item_id = pending_action["itemId"]
    item = itemRegistry[item_id]
    item_name = get_item_display_name(
        item,
    )

    if pending_action["type"] == "takeOverflow":
        location_state = get_current_location_state(
            game_state,
        )
        contained_item_ids = get_items_in_item_container(
            location_state,
            item_id,
        )
        acquired_item_ids = [
            item_id,
            *contained_item_ids,
        ]
        final_inventory = [
            *player_state["inventory"],
            *acquired_item_ids,
        ]
        overflow_count = get_carry_overflow_count(
            player_state,
            final_inventory,
        )
        dropped_item_ids = select_overflow_items(
            player_state["inventory"],
            overflow_count,
        )

        player_state["inventory"] = [
            inventory_item_id
            for inventory_item_id in final_inventory
            if inventory_item_id not in dropped_item_ids
        ]

        for acquired_item_id in acquired_item_ids:
            location_state["items"].pop(
                acquired_item_id,
                None,
            )

        place_items_loose(
            game_state,
            dropped_item_ids,
        )
        game_state["pendingAction"] = None

        response = item.get(
            "takeResponse",
            f"You took the {item_name} and everything still inside it.",
        )

        return append_narrator_response(
            response,
            "To make room, you drop "
            f"{get_formatted_item_list(dropped_item_ids)} on the ground.",
        )

    if pending_action["type"] == "equippedDrop":
        player_state["equipped"] = [
            equipped_id
            for equipped_id in player_state["equipped"]
            if equipped_id != item_id
        ]
        place_items_loose(
            game_state,
            [item_id],
        )
        game_state["pendingAction"] = None

        return item.get(
            "dropResponse",
            f"You drop the {item_name}.",
        )

    if action == "wear":
        equipped_item_id = pending_action["equippedItemId"]
        final_inventory = [
            inventory_item_id
            for inventory_item_id in player_state["inventory"]
            if inventory_item_id != item_id
        ]
        final_equipped = [
            equipped_id
            for equipped_id in player_state["equipped"]
            if equipped_id != equipped_item_id
        ]
        final_equipped.append(
            item_id,
        )
        overflow_count = get_carry_overflow_count(
            player_state,
            final_inventory,
            final_equipped,
        )
        overflow_item_ids = select_overflow_items(
            final_inventory,
            overflow_count,
        )
        dropped_item_ids = [
            equipped_item_id,
            *overflow_item_ids,
        ]

        player_state["inventory"] = [
            inventory_item_id
            for inventory_item_id in final_inventory
            if inventory_item_id not in overflow_item_ids
        ]
        player_state["equipped"] = final_equipped
        place_items_loose(
            game_state,
            dropped_item_ids,
        )
        game_state["pendingAction"] = None

        response = item.get(
            "wearResponse",
            f"You equip the {item_name}.",
        )

        return append_narrator_response(
            response,
            "The reduced carrying space causes "
            f"{get_formatted_item_list(dropped_item_ids)} to fall to the ground.",
        )

    final_equipped = [
        equipped_id
        for equipped_id in player_state["equipped"]
        if equipped_id != item_id
    ]

    if action == "remove":
        final_inventory = [
            *player_state["inventory"],
            item_id,
        ]
        overflow_count = get_carry_overflow_count(
            player_state,
            final_inventory,
            final_equipped,
        )
        dropped_item_ids = select_overflow_items(
            final_inventory,
            overflow_count,
        )

        player_state["inventory"] = [
            inventory_item_id
            for inventory_item_id in final_inventory
            if inventory_item_id not in dropped_item_ids
        ]
        player_state["equipped"] = final_equipped
        place_items_loose(
            game_state,
            dropped_item_ids,
        )
        game_state["pendingAction"] = None

        response = item.get(
            "removeResponse",
            f"You remove the {item_name}.",
        )

        return append_narrator_response(
            response,
            "The reduced carrying space causes "
            f"{get_formatted_item_list(dropped_item_ids)} to fall to the ground.",
        )

    final_inventory = list(
        player_state["inventory"],
    )
    overflow_count = get_carry_overflow_count(
        player_state,
        final_inventory,
        final_equipped,
    )
    overflow_item_ids = select_overflow_items(
        final_inventory,
        overflow_count,
    )
    dropped_item_ids = [
        item_id,
        *overflow_item_ids,
    ]

    player_state["inventory"] = [
        inventory_item_id
        for inventory_item_id in final_inventory
        if inventory_item_id not in overflow_item_ids
    ]
    player_state["equipped"] = final_equipped
    place_items_loose(
        game_state,
        dropped_item_ids,
    )
    game_state["pendingAction"] = None

    response = item.get(
        "dropResponse",
        f"You drop the {item_name}.",
    )

    if not overflow_item_ids:
        return response

    return append_narrator_response(
        response,
        "The reduced carrying space also causes "
        f"{get_formatted_item_list(overflow_item_ids)} to fall to the ground.",
    )
