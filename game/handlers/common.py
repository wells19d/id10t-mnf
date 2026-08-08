from areas.areaRegistry import areaRegistry
from game.itemRegistry import itemRegistry


def get_current_area_state(game_state):
    current_area_id = game_state["player"]["currentArea"]

    areas = game_state.setdefault("areas", {})

    return areas.setdefault(
        current_area_id,
        {
            "flags": {},
            "locations": {},
        },
    )


def build_initial_location_items(area_data):
    items = {}

    # Loose items in the area.
    for item_id in area_data.get("items", []):
        items[item_id] = None

    # Items that begin inside/on scenery.
    for scenery_id, scenery_data in area_data.get(
        "scenery",
        {},
    ).items():
        for item_id in scenery_data.get("items", []):
            items[item_id] = scenery_id

    return items


def get_location_state(game_state, location_id):
    area_state = get_current_area_state(game_state)

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
            "items": build_initial_location_items(area_data),
            "scenery": {},
        }

    return locations[location_id]


def get_current_location_state(game_state):
    current_location = game_state["player"]["currentLocation"]

    return get_location_state(
        game_state,
        current_location,
    )


def get_item_name(item):
    return item.get(
        "name",
        item["aliases"][0],
    )


def format_item_names(item_names):
    if len(item_names) == 1:
        return f"a {item_names[0]}"

    if len(item_names) == 2:
        return f"a {item_names[0]} and a {item_names[1]}"

    first_items = ", ".join(item_names[:-1])

    return f"a {first_items}, and a {item_names[-1]}"


def find_scenery(target, current_area):
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


def find_items(item_name, item_ids):
    if not item_name:
        return []

    item_name = item_name.strip().lower()

    matches = []

    for item_id in item_ids:
        item = itemRegistry.get(item_id)

        if not item:
            continue

        aliases = item.get(
            "aliases",
            [],
        )

        if item_name == item_id or item_name in aliases:
            matches.append(item_id)

    return matches


def resolve_item(item_name, item_ids):
    matches = find_items(
        item_name,
        item_ids,
    )

    if not matches:
        return None, None

    if len(matches) > 1:
        return None, f"Which {item_name} do you mean?"

    return matches[0], None


def get_scenery_state(location_state, scenery_id):
    scenery_states = location_state.setdefault(
        "scenery",
        {},
    )

    return scenery_states.setdefault(
        scenery_id,
        {},
    )


def get_items_in_scenery(location_state, scenery_id):
    return [
        item_id
        for item_id, container_id in location_state["items"].items()
        if container_id == scenery_id
    ]


def get_visible_item_ids(current_area, game_state):
    location_state = get_current_location_state(
        game_state,
    )

    visible_items = []

    for item_id, container_id in location_state["items"].items():

        # Loose item.
        if container_id is None:
            visible_items.append(item_id)
            continue

        scenery_data = current_area.get(
            "scenery",
            {},
        ).get(container_id)

        if not scenery_data:
            visible_items.append(item_id)
            continue

        scenery_state = get_scenery_state(
            location_state,
            container_id,
        )

        # Items inside a closed container are hidden.
        if scenery_data.get("openable") and not scenery_state.get("isOpen", False):
            continue

        visible_items.append(item_id)

    return visible_items
