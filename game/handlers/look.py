from game.handlers.common import (
    find_scenery,
    get_current_location_state,
    get_item_state,
    get_location_description,
    get_scenery_state,
    get_visible_item_ids,
    resolve_item,
    state_matches,
)
from items.itemRegistry import itemRegistry


def get_state_description(
    data,
    current_state,
):
    for state_description in data.get(
        "stateDescriptions",
        [],
    ):
        required_state = state_description.get(
            "requiresState",
            {},
        )

        if state_matches(
            current_state,
            required_state,
        ):
            return state_description.get(
                "description",
            )

    return None


def handle_look(command, current_area, game_state):
    target = command["target"] or command["object"]

    # LOOK
    # Return the basic description of the current area.
    if not target:
        return get_location_description(
            current_area,
            game_state,
        )

    # LOOK AT <scenery>
    scenery_id, scenery_data = find_scenery(
        target,
        current_area,
    )

    if scenery_data:
        location_state = get_current_location_state(
            game_state,
        )

        scenery_state = get_scenery_state(
            location_state,
            scenery_id,
        )

        state_description = get_state_description(
            scenery_data,
            scenery_state,
        )

        if state_description:
            return state_description

        description = scenery_data.get(
            "description",
        )

        if description:
            return description

        return f"There is nothing remarkable " f"about the {target}."

    # LOOK AT <item>
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

        item_state = get_item_state(
            game_state,
            item_id,
        )

        state_description = get_state_description(
            item,
            item_state,
        )

        if state_description:
            return state_description

        description = item.get(
            "description",
        )

        if description:
            return description

        return f"There is nothing remarkable " f"about the {target}."

    return f"I don't see a {target} here."
