from game.handlers.common import (
    addQuantityText,
    findScenery,
    currentLocation,
    getItemStateSnapshot,
    locationText,
    getSceneryState,
    visibleItemIds,
    resolveItem,
)
from game.itemDisplay import getStateDescription
from items.registry import itemRegistry


def handleLook(command, location_definition, game_state):
    target = command["target"] or command["object"]

    # LOOK
    # Return the basic description of the current area.
    if not target:
        return locationText(
            location_definition,
            game_state,
        )

    # LOOK AT <scenery>
    scenery_id, scenery_data = findScenery(
        target,
        location_definition,
    )

    if scenery_data:
        location_state = currentLocation(
            game_state,
        )

        scenery_state = getSceneryState(
            location_state,
            scenery_id,
        )

        state_description = getStateDescription(
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
        visibleItemIds(
            location_definition,
            game_state,
        )
        + game_state["player"]["inventory"]
        + game_state["player"]["equipped"]
    )

    item_id, clarification = resolveItem(
        target,
        visible_items,
    )

    if clarification:
        return clarification

    if item_id:
        item = itemRegistry[item_id]

        item_state = getItemStateSnapshot(
            game_state,
            item_id,
        )

        inspect_state_response = getStateDescription(
            item,
            item_state,
            "inspectState",
        )

        if inspect_state_response:
            return addQuantityText(
                inspect_state_response,
                item,
                item_state,
            )

        if item_id in game_state["player"]["inventory"]:
            inspect_response = item.get(
                "inspect",
            ) or item.get(
                "description",
            )

            if inspect_response:
                return addQuantityText(
                    inspect_response,
                    item,
                    item_state,
                )

            return f"There is nothing remarkable " f"about the {target}."

        state_description = getStateDescription(
            item,
            item_state,
        )

        if state_description:
            return addQuantityText(
                state_description,
                item,
                item_state,
            )

        description = item.get(
            "description",
        )

        if description:
            return addQuantityText(
                description,
                item,
                item_state,
            )

        return f"There is nothing remarkable " f"about the {target}."

    return f"I don't see a {target} here."
