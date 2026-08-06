from game.handlers.common import (
    find_scenery,
    get_current_location_state,
    get_scenery_state,
)


def handle_open(command, current_area, game_state):
    target = command["object"] or command["target"]

    if not target:
        return "I don't know what I want to open."

    scenery_id, scenery_data = find_scenery(
        target,
        current_area,
    )

    if not scenery_data:
        return f"I don't see a {target} here."

    if not scenery_data.get("openable", False):
        return scenery_data.get(
            "openFailResponse",
            f"You can't open the {scenery_id}.",
        )

    location_state = get_current_location_state(game_state)
    scenery_state = get_scenery_state(
        location_state,
        scenery_id,
    )

    if scenery_state.get("isOpen", False):
        return scenery_data.get(
            "alreadyOpenResponse",
            f"The {scenery_id} is already open.",
        )

    scenery_state["isOpen"] = True

    return scenery_data.get(
        "openResponse",
        f"You open the {scenery_id}.",
    )


def handle_close(command, current_area, game_state):
    target = command["object"] or command["target"]

    if not target:
        return "I don't know what I want to close."

    scenery_id, scenery_data = find_scenery(
        target,
        current_area,
    )

    if not scenery_data:
        return f"I don't see a {target} here."

    if not scenery_data.get("closeable", False):
        return scenery_data.get(
            "closeFailResponse",
            f"You can't close the {scenery_id}.",
        )

    location_state = get_current_location_state(game_state)
    scenery_state = get_scenery_state(
        location_state,
        scenery_id,
    )

    if not scenery_state.get("isOpen", False):
        return scenery_data.get(
            "alreadyClosedResponse",
            f"The {scenery_id} is already closed.",
        )

    scenery_state["isOpen"] = False

    return scenery_data.get(
        "closeResponse",
        f"You close the {scenery_id}.",
    )
