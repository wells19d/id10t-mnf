from game.itemRegistry import itemRegistry


def get_current_area_state(game_state):
    current_area = game_state["player"]["currentArea"]

    return game_state["areas"][current_area]


def get_current_location_state(game_state):
    area_state = get_current_area_state(game_state)
    current_location = game_state["player"]["currentLocation"]

    return area_state["locations"][current_location]


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
        aliases = scenery_data.get("aliases", [])

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

        aliases = item.get("aliases", [])

        if item_name == item_id or item_name in aliases:
            matches.append(item_id)

    return matches


def resolve_item(item_name, item_ids):
    matches = find_items(item_name, item_ids)

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


def get_scenery_item_ids(current_area):
    scenery_item_ids = []

    for scenery_data in current_area.get(
        "scenery",
        {},
    ).values():
        scenery_item_ids.extend(scenery_data.get("items", []))

    return scenery_item_ids


def get_visible_item_ids(current_area, game_state):
    location_state = get_current_location_state(game_state)
    available_items = location_state["itemsAvailable"]
    visible_items = []

    scenery_item_ids = get_scenery_item_ids(current_area)

    for item_id in available_items:
        if item_id not in scenery_item_ids:
            visible_items.append(item_id)

    for scenery_id, scenery_data in current_area.get(
        "scenery",
        {},
    ).items():
        scenery_items = scenery_data.get("items", [])

        if not scenery_items:
            continue

        scenery_state = get_scenery_state(
            location_state,
            scenery_id,
        )

        if scenery_data.get("openable") and not scenery_state.get("isOpen", False):
            continue

        for item_id in scenery_items:
            if item_id in available_items and item_id not in visible_items:
                visible_items.append(item_id)

    return visible_items
