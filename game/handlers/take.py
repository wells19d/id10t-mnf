from game.handlers.common import (
    canAccessItemContents,
    canAccessSceneryContents,
    commandFailure,
    findScenery,
    overflowCount,
    currentLocation,
    displayName,
    getItemStateSnapshot,
    containerItems,
    sceneryItems,
    pendingPrompt,
    getSceneryState,
    visibleItemIds,
    resolveItem,
)
from items.registry import itemRegistry


def findMergeInventoryItem(item_id, inventory):
    item = itemRegistry[item_id]
    merge_config = item.get(
        "mergeOnTake",
    )

    if not merge_config:
        return None

    for carried_item_id in inventory:
        if carried_item_id == item_id:
            continue

        carried_item = itemRegistry[carried_item_id]
        carried_merge_config = carried_item.get(
            "mergeOnTake",
        )

        if not carried_merge_config:
            continue

        if (
            carried_merge_config.get("group") == merge_config.get("group")
            and carried_merge_config.get("stateKey")
            == merge_config.get("stateKey")
        ):
            return carried_item_id

    return None


def mergeTakenItem(
    item_id,
    retained_item_id,
    location_state,
    game_state,
):
    item = itemRegistry[item_id]
    merge_config = item["mergeOnTake"]
    state_key = merge_config["stateKey"]

    retained_state = getItemStateSnapshot(
        game_state,
        retained_item_id,
    )
    incoming_state = getItemStateSnapshot(
        game_state,
        item_id,
    )

    retained_state[state_key] += incoming_state[state_key]

    game_state["itemStates"][retained_item_id] = retained_state
    location_state["items"].pop(
        item_id,
        None,
    )
    game_state["itemStates"].pop(
        item_id,
        None,
    )

    display_name = displayName(
        item,
    )

    return item.get(
        "mergeResponse",
        f"You combine the {display_name} with the one you are carrying.",
    )


def handleTake(command, location_definition, game_state):
    item_name = command["object"]
    source_name = command["target"]

    if not item_name:
        return commandFailure(
            "I don't know what I want to take.",
        )

    location_state = currentLocation(
        game_state,
    )

    # TAKE <item> FROM <scenery>
    if source_name:
        scenery_id, scenery_data = findScenery(
            source_name,
            location_definition,
        )

        if scenery_data:
            scenery_state = getSceneryState(
                location_state,
                scenery_id,
            )

            # Closed containers must be opened first.
            if scenery_data.get("openable") and not scenery_state.get(
                "isOpen",
                False,
            ):
                return commandFailure(
                    scenery_data.get(
                        "takeClosedResponse",
                        f"The {scenery_id} is closed.",
                    )
                )

            # Other scenery conditions may also block
            # access to its contents.
            if not canAccessSceneryContents(
                scenery_data,
                scenery_state,
            ):
                return commandFailure(
                    scenery_data.get(
                        "takeBlockedResponse",
                        f"You can't reach anything in the {scenery_id} right now.",
                    )
                )

            available_items = sceneryItems(
                location_state,
                scenery_id,
            )
        else:
            accessible_items = (
                visibleItemIds(
                    location_definition,
                    game_state,
                )
                + game_state["player"]["inventory"]
                + game_state["player"]["equipped"]
            )
            container_item_id, clarification = resolveItem(
                source_name,
                accessible_items,
            )

            if clarification:
                return commandFailure(
                    clarification,
                )

            container_item = itemRegistry.get(
                container_item_id,
            )

            if not container_item or not container_item.get(
                "container",
                False,
            ):
                return commandFailure(
                    f"I don't see a {source_name} here.",
                )

            container_state = getItemStateSnapshot(
                game_state,
                container_item_id,
            )

            if not canAccessItemContents(
                container_item,
                container_state,
            ):
                return commandFailure(
                    container_item.get(
                        "takeBlockedResponse",
                        f"You can't reach anything in the {source_name} right now.",
                    )
                )

            available_items = containerItems(
                location_state,
                container_item_id,
            )

    # TAKE <item>
    else:
        available_items = visibleItemIds(
            location_definition,
            game_state,
        )

    item_id, clarification = resolveItem(
        item_name,
        available_items,
    )

    if clarification:
        return commandFailure(
            clarification,
        )

    if not item_id:
        scenery_id, scenery_data = findScenery(
            item_name,
            location_definition,
        )

        if scenery_data:
            return commandFailure(
                scenery_data.get(
                    "takeFail",
                    f"You can't take the {scenery_id}.",
                )
            )

        return commandFailure(
            f"I don't see a {item_name} here.",
        )

    item = itemRegistry[item_id]

    display_name = displayName(item)

    if not item.get(
        "takeable",
        False,
    ):
        return commandFailure(
            item.get(
                "takeFail",
                f"I can't take the {display_name}.",
            )
        )

    player_state = game_state["player"]
    inventory = player_state["inventory"]

    retained_item_id = findMergeInventoryItem(
        item_id,
        inventory,
    )

    if retained_item_id:
        return mergeTakenItem(
            item_id,
            retained_item_id,
            location_state,
            game_state,
        )

    contained_item_ids = []

    if item.get(
        "transferContentsOnTake",
        False,
    ):
        contained_item_ids = containerItems(
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

    overflow_count = overflowCount(
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

        return pendingPrompt(
            game_state,
        )

    if overflow_count:
        return commandFailure(
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
