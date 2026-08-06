from game.handlers.common import (
    find_scenery,
    get_current_area_state,
    get_current_location_state,
    get_item_name,
    resolve_item,
)
from game.itemRegistry import itemRegistry


def handle_use(command, current_area, game_state):
    values = command["values"]
    target = command["target"]

    # Handle special scenery interactions, such as entering
    # a combination into a safe.
    if values and target:
        scenery_id, scenery_data = find_scenery(
            target,
            current_area,
        )

        if not scenery_data:
            return f"I don't see a {target} here."

        interactions = current_area.get(
            "interactions",
            {},
        )

        interaction = interactions.get(scenery_id)

        if interaction and interaction.get("type") == "combination":
            correct_combination = interaction.get(
                "combination",
                [],
            )

            if values == correct_combination:
                location_state = get_current_location_state(game_state)
                location_state["safeOpened"] = True

                return interaction["onSuccess"]

            return interaction["onFail"]

    item_name = command["object"]

    if not item_name:
        return "I don't know what I want to use."

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

    if not target:
        return f"I don't know what I want to use " f"the {display_name} on."

    # Resolve the player's target through the current location's
    # scenery IDs and aliases.
    scenery_id, scenery_data = find_scenery(
        target,
        current_area,
    )

    if not scenery_data:
        return f"I don't see a {target} here."

    target_action = item.get(
        "onUse",
        {},
    ).get(scenery_id)

    if not target_action:
        return f"You can't use the " f"{display_name} on {scenery_id} here."

    if isinstance(target_action, dict):
        flag_name = target_action.get("setsFlag")

        if flag_name:
            area_state = get_current_area_state(game_state)
            area_state["flags"][flag_name] = True

        if target_action.get("destroyItem"):
            inventory.remove(item_id)

        return target_action["response"]

    return target_action
