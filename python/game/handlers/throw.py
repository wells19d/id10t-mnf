from game.handlers.common import (
    commandFailure,
    findScenery,
    currentLocation,
    displayName,
    resolveItem,
)
from items.registry import itemRegistry


def handleThrow(command, location_definition, game_state):
    item_name = command["object"]
    target = command["target"]

    if not item_name:
        return commandFailure(
            "I don't know what I want to throw.",
        )

    inventory = game_state["player"]["inventory"]

    item_id, clarification = resolveItem(
        item_name,
        inventory,
        allow_interchangeable=True,
    )

    if clarification:
        return commandFailure(
            clarification,
        )

    if not item_id:
        return commandFailure(
            f"You aren't carrying {item_name}.",
        )

    item = itemRegistry[item_id]

    display_name = displayName(
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
        scenery_id, scenery_data = findScenery(
            target,
            location_definition,
        )

        if not scenery_data:
            return commandFailure(
                f"I don't see a {target} here.",
            )

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
        return commandFailure(
            f"You can't throw the {display_name}.",
        )

    inventory.remove(
        item_id,
    )

    if not throw_action.get(
        "destroyItem",
        False,
    ):
        location_state = currentLocation(
            game_state,
        )

        if attach_to_target:
            location_state["items"][item_id] = target_scenery_id
        else:
            location_state["items"][item_id] = None

    return throw_action["response"]
