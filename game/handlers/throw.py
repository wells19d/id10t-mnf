from game.handlers.common import (
    find_scenery,
    get_current_location_state,
    get_item_display_name,
    resolve_item,
    unequip_item,
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

    display_name = get_item_display_name(
        item,
    )

    throw_actions = item.get(
        "onThrow",
        {},
    )

    target_scenery_id = None
    throw_action = None
    attach_to_target = False

    # THROW <item> AT <target>
    if target:
        scenery_id, scenery_data = find_scenery(
            target,
            current_area,
        )

        if not scenery_data:
            return f"I don't see a {target} here."

        target_scenery_id = scenery_id

        # Scenery defines special targeted throws.
        throw_action = scenery_data.get(
            "throwInteractions",
            {},
        ).get(
            item_id,
        )

        if throw_action:
            attach_to_target = True

    # Otherwise use the item's normal throw behavior.
    if not throw_action:
        throw_action = throw_actions.get(
            "default",
        )

    if not throw_action:
        return f"You can't throw the {display_name}."

    # Thrown items can no longer remain equipped.
    unequip_item(
        game_state,
        item_id,
    )

    inventory.remove(
        item_id,
    )

    if not throw_action.get(
        "destroyItem",
        False,
    ):
        location_state = get_current_location_state(
            game_state,
        )

        if attach_to_target:
            location_state["items"][item_id] = target_scenery_id
        else:
            location_state["items"][item_id] = None

    return throw_action["response"]
