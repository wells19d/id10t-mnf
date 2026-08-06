from game.handlers.common import (
    get_current_area_state,
    get_current_location_state,
    get_item_name,
    resolve_item,
)
from game.itemRegistry import itemRegistry


def handle_use(command, current_area, game_state):
    values = command["values"]
    target = command["target"]

    if values and target:
        interactions = current_area.get(
            "interactions",
            {},
        )

        interaction = interactions.get(target)

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

    target_action = item.get(
        "onUse",
        {},
    ).get(target)

    if not target_action:
        return f"You can't use the " f"{display_name} on {target} here."

    if isinstance(target_action, dict):
        flag_name = target_action.get("setsFlag")

        if flag_name:
            area_state = get_current_area_state(game_state)
            area_state["flags"][flag_name] = True

        if target_action.get("destroyItem"):
            inventory.remove(item_id)

        return target_action["response"]

    return target_action
