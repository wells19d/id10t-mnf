from game.itemPresentation import get_item_display_name
from game.worldState import (
    get_current_location_state,
    get_item_state_snapshot,
    get_scenery_state,
    state_matches,
)
from items.itemRegistry import itemRegistry
from states.gameState import WORLD_ITEM_PLACEMENT


def find_scenery(
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


def find_items(
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
        item_display_name = item.get(
            "name",
            "",
        ).strip().lower()

        if (
            item_name == item_id
            or item_name == item_display_name
            or item_name in aliases
        ):
            matches.append(
                item_id,
            )

    return matches


def resolve_item(
    item_name,
    item_ids,
    include_match_names=False,
):
    matches = find_items(
        item_name,
        item_ids,
    )

    if not matches:
        return None, None

    if len(matches) > 1:
        if include_match_names:
            match_names = [
                get_item_display_name(
                    itemRegistry[item_id],
                )
                for item_id in matches
            ]

            if len(match_names) == 2:
                choices = " or ".join(
                    match_names,
                )
            else:
                choices = (
                    ", ".join(match_names[:-1])
                    + f", or {match_names[-1]}"
                )

            return None, (
                f"Which {item_name} do you mean: "
                f"{choices}?"
            )

        return None, f"Which {item_name} do you mean?"

    return matches[0], None


def get_items_in_scenery(
    location_state,
    scenery_id,
):
    return [
        item_id
        for item_id, placement in location_state["items"].items()
        if placement == scenery_id
    ]


def get_items_in_item_container(
    location_state,
    container_item_id,
):
    return [
        item_id
        for item_id, placement in location_state["items"].items()
        if placement == container_item_id
    ]


def can_access_item_contents(
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

    return state_matches(
        item_state,
        item.get(
            "contentsRequiresState",
            {},
        ),
    )


def is_world_item_accessible(
    item_id,
    location_definition,
    game_state,
    checked_item_ids=None,
):
    location_state = get_current_location_state(
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
        scenery_state = get_scenery_state(
            location_state,
            placement,
        )

        return can_access_scenery_contents(
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

    if not is_world_item_accessible(
        placement,
        location_definition,
        game_state,
        checked_item_ids,
    ):
        return False

    container_state = get_item_state_snapshot(
        game_state,
        placement,
    )

    return can_access_item_contents(
        container_item,
        container_state,
    )


def can_access_scenery_contents(
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

    if not state_matches(
        scenery_state,
        required_state,
    ):
        return False

    return True


def get_visible_item_ids(
    location_definition,
    game_state,
):
    location_state = get_current_location_state(
        game_state,
    )

    visible_items = []

    for item_id in location_state["items"]:
        if is_world_item_accessible(
            item_id,
            location_definition,
            game_state,
        ):
            visible_items.append(
                item_id,
            )

    return visible_items
