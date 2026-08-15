from game.itemDisplay import displayName
from game.worldState import (
    currentLocation,
    getItemStateSnapshot,
    getSceneryState,
    stateMatches,
)
from items.registry import itemRegistry
from states.game import WORLD_ITEM_PLACEMENT


def findScenery(
    target,
    location_definition,
):
    if not target:
        return None, None

    for scenery_id, scenery_data in location_definition.get(
        "scenery",
        {},
    ).items():
        aliases = scenery_data.get(
            "aliases",
            [],
        )

        if target == scenery_id or target in aliases:
            return scenery_id, scenery_data

    return None, None


def findItems(
    item_name,
    item_ids,
):
    if not item_name:
        return []

    item_name = item_name.strip().lower()

    matches = []

    for item_id in item_ids:
        item = itemRegistry.get(
            item_id,
        )

        if not item:
            continue

        aliases = item.get(
            "aliases",
            [],
        )
        item_display_name = (
            item.get(
                "name",
                "",
            )
            .strip()
            .lower()
        )

        if (
            item_name == item_id
            or item_name == item_display_name
            or item_name in aliases
        ):
            matches.append(
                item_id,
            )

    return matches


def resolveItem(
    item_name,
    item_ids,
    include_match_names=False,
    allow_interchangeable=False,
):
    matches = findItems(
        item_name,
        item_ids,
    )

    if not matches:
        return None, None

    if len(matches) > 1:
        if allow_interchangeable:
            interchangeable_group = None

            for item_id in matches:
                group = itemRegistry[item_id].get(
                    "interchangeableGroup",
                )

                if not isinstance(group, str) or not group.strip():
                    break

                if interchangeable_group is None:
                    interchangeable_group = group
                elif group != interchangeable_group:
                    break
            else:
                return matches[0], None

        if include_match_names:
            match_names = [
                displayName(
                    itemRegistry[item_id],
                )
                for item_id in matches
            ]

            if len(match_names) == 2:
                choices = " or ".join(
                    match_names,
                )
            else:
                choices = ", ".join(match_names[:-1]) + f", or {match_names[-1]}"

            return None, (f"Which {item_name} do you mean: " f"{choices}?")

        return None, f"Which {item_name} do you mean?"

    return matches[0], None


def sceneryItems(
    location_state,
    scenery_id,
):
    return [
        item_id
        for item_id, placement in location_state["items"].items()
        if placement == scenery_id
    ]


def containerItems(
    location_state,
    container_item_id,
):
    return [
        item_id
        for item_id, placement in location_state["items"].items()
        if placement == container_item_id
    ]


def canAccessItemContents(
    item,
    item_state,
):
    if not item.get(
        "container",
        False,
    ):
        return False

    if item.get("openable") and not item_state.get(
        "isOpen",
        False,
    ):
        return False

    if item.get("contentsRequireSearch") and not item_state.get(
        "isSearched",
        False,
    ):
        return False

    return stateMatches(
        item_state,
        item.get(
            "contentsRequiresState",
            {},
        ),
    )


def canReachItem(
    item_id,
    location_definition,
    game_state,
    checked_item_ids=None,
):
    location_state = currentLocation(
        game_state,
    )
    placement = location_state["items"].get(
        item_id,
    )

    if placement in {
        WORLD_ITEM_PLACEMENT,
        None,
    }:
        return item_id in location_state["items"]

    scenery_data = location_definition.get(
        "scenery",
        {},
    ).get(
        placement,
    )

    if scenery_data:
        scenery_state = getSceneryState(
            location_state,
            placement,
        )

        return canAccessSceneryContents(
            scenery_data,
            scenery_state,
        )

    container_item = itemRegistry.get(
        placement,
    )

    if not container_item:
        return False

    checked_item_ids = set(
        checked_item_ids or [],
    )

    if item_id in checked_item_ids:
        return False

    checked_item_ids.add(
        item_id,
    )

    if not canReachItem(
        placement,
        location_definition,
        game_state,
        checked_item_ids,
    ):
        return False

    container_state = getItemStateSnapshot(
        game_state,
        placement,
    )

    return canAccessItemContents(
        container_item,
        container_state,
    )


def canAccessSceneryContents(
    scenery_data,
    scenery_state,
):
    # Closed containers hide their contents.
    if scenery_data.get("openable") and not scenery_state.get(
        "isOpen",
        False,
    ):
        return False

    # Optional state requirements for accessing contents.
    required_state = scenery_data.get(
        "contentsRequiresState",
        {},
    )

    if not stateMatches(
        scenery_state,
        required_state,
    ):
        return False

    return True


def visibleItemIds(
    location_definition,
    game_state,
):
    location_state = currentLocation(
        game_state,
    )

    visible_items = []

    for item_id in location_state["items"]:
        if canReachItem(
            item_id,
            location_definition,
            game_state,
        ):
            visible_items.append(
                item_id,
            )

    return visible_items
