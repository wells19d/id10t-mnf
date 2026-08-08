from copy import deepcopy

from areas.areaRegistry import areaRegistry
from game.itemRegistry import itemRegistry

WORLD_ITEM_PLACEMENT = "__world__"


def get_current_area_state(game_state):
    current_area_id = game_state["player"]["currentArea"]

    areas = game_state.setdefault(
        "areas",
        {},
    )

    return areas.setdefault(
        current_area_id,
        {
            "flags": {},
            "locations": {},
        },
    )


def build_initial_location_items(area_data):
    items = {}

    # Items that begin naturally in the area.
    for item_id in area_data.get(
        "items",
        [],
    ):
        items[item_id] = WORLD_ITEM_PLACEMENT

    # Items that begin inside/on scenery.
    for scenery_id, scenery_data in area_data.get(
        "scenery",
        {},
    ).items():
        for item_id in scenery_data.get(
            "items",
            [],
        ):
            items[item_id] = scenery_id

    return items


def build_initial_scenery_state(area_data):
    scenery_states = {}

    for scenery_id, scenery_data in area_data.get(
        "scenery",
        {},
    ).items():
        scenery_states[scenery_id] = deepcopy(
            scenery_data.get(
                "state",
                {},
            )
        )

    return scenery_states


def get_location_state(game_state, location_id):
    area_state = get_current_area_state(
        game_state,
    )

    locations = area_state.setdefault(
        "locations",
        {},
    )

    if location_id not in locations:
        area_data = areaRegistry.get(
            location_id,
            {},
        )

        locations[location_id] = {
            "visited": False,
            "items": build_initial_location_items(
                area_data,
            ),
            "scenery": build_initial_scenery_state(
                area_data,
            ),
        }

    return locations[location_id]


def get_current_location_state(game_state):
    current_location = game_state["player"]["currentLocation"]

    return get_location_state(
        game_state,
        current_location,
    )


def get_scenery_state(
    location_state,
    scenery_id,
):
    scenery_states = location_state.setdefault(
        "scenery",
        {},
    )

    return scenery_states.setdefault(
        scenery_id,
        {},
    )


def get_item_state(
    game_state,
    item_id,
):
    item_states = game_state.setdefault(
        "itemStates",
        {},
    )

    if item_id not in item_states:
        item = itemRegistry.get(
            item_id,
            {},
        )

        item_states[item_id] = deepcopy(
            item.get(
                "state",
                {},
            )
        )

    return item_states[item_id]


def state_matches(
    current_state,
    required_state,
):
    for key, required_value in required_state.items():
        if current_state.get(key) != required_value:
            return False

    return True


def apply_state_changes(
    current_state,
    changes,
):
    if not changes:
        return

    current_state.update(
        changes,
    )


def get_item_name(item):
    return item.get(
        "name",
        item["aliases"][0],
    )


def get_item_display_name(item):
    item_name = get_item_name(
        item,
    )

    return "<em><span class='item-highlight'>" f"{item_name}" "</span></em>"


def unequip_item(
    game_state,
    item_id,
):
    equipped = game_state["player"].get(
        "equipped",
        [],
    )

    if item_id in equipped:
        equipped.remove(
            item_id,
        )


def format_item_names(item_names):
    if len(item_names) == 1:
        return f"a {item_names[0]}"

    if len(item_names) == 2:
        return f"a {item_names[0]} and a {item_names[1]}"

    first_items = ", ".join(item_names[:-1])

    return f"a {first_items}, " f"and a {item_names[-1]}"


def find_scenery(
    target,
    current_area,
):
    if not target:
        return None, None

    for scenery_id, scenery_data in current_area.get(
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

        if item_name == item_id or item_name in aliases:
            matches.append(
                item_id,
            )

    return matches


def resolve_item(
    item_name,
    item_ids,
):
    matches = find_items(
        item_name,
        item_ids,
    )

    if not matches:
        return None, None

    if len(matches) > 1:
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
    current_area,
    game_state,
):
    location_state = get_current_location_state(
        game_state,
    )

    visible_items = []

    for item_id, placement in location_state["items"].items():

        # Initial world item or dropped loose item.
        if placement in [
            WORLD_ITEM_PLACEMENT,
            None,
        ]:
            visible_items.append(
                item_id,
            )
            continue

        scenery_data = current_area.get(
            "scenery",
            {},
        ).get(
            placement,
        )

        if not scenery_data:
            visible_items.append(
                item_id,
            )
            continue

        scenery_state = get_scenery_state(
            location_state,
            placement,
        )

        if not can_access_scenery_contents(
            scenery_data,
            scenery_state,
        ):
            continue

        visible_items.append(
            item_id,
        )

    return visible_items
