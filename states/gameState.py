# states/gameState.py

from copy import deepcopy

from areas.locationRegistry import locationRegistry
from items.itemRegistry import itemRegistry

# Increment this when persistent location/item definitions or state semantics
# change incompatibly. Development saves are restarted instead of migrated.
SAVE_VERSION = 4

WORLD_ITEM_PLACEMENT = "__world__"

EQUIPMENT_SLOTS = frozenset(
    {
        "head",
        "chest",
        "hands",
        "legs",
        "feet",
    }
)

GAME_STATE_REQUIREMENT_KEYS = frozenset(
    {
        "player",
        "inventory",
        "equipped",
        "flags",
        "sceneryState",
        "itemStates",
    }
)

initialState = {
    "saveVersion": SAVE_VERSION,
    "player": {
        "introComplete": False,
        "currentLocation": "a1_clearing",
        "currentDirection": None,
        "currentShortDirection": None,
        "lastDirection": None,
        "lastShortDirection": None,
        "inventory": [],
        "equipped": [],
        "health": "Medium",
    },
    "itemStates": {},
    "flags": {},
    "locations": {},
}


def build_initial_item_locations():
    initial_item_locations = {}

    for location_id, location_definition in locationRegistry.items():
        for item_id in location_definition.get(
            "items",
            [],
        ):
            initial_item_locations[item_id] = location_id

        for scenery_definition in location_definition.get(
            "scenery",
            {},
        ).values():
            for item_id in scenery_definition.get(
                "items",
                [],
            ):
                initial_item_locations[item_id] = location_id

    return initial_item_locations


INITIAL_ITEM_LOCATIONS = build_initial_item_locations()


def merge_state(
    default_state,
    saved_state,
):
    merged_state = deepcopy(
        default_state,
    )

    for key, saved_value in saved_state.items():
        default_value = merged_state.get(
            key,
        )

        if isinstance(default_value, dict) and isinstance(saved_value, dict):
            merged_state[key] = merge_state(
                default_value,
                saved_value,
            )
        else:
            merged_state[key] = deepcopy(
                saved_value,
            )

    return merged_state


def create_game_state():
    return deepcopy(
        initialState,
    )


def is_valid_item_id_list(item_ids):
    if not isinstance(
        item_ids,
        list,
    ):
        return False

    if not all(
        isinstance(item_id, str) and item_id in itemRegistry
        for item_id in item_ids
    ):
        return False

    return len(item_ids) == len(set(item_ids))


def is_valid_player_state(player_state):
    if not isinstance(
        player_state,
        dict,
    ):
        return False

    if any(
        field not in player_state
        for field in initialState["player"]
    ):
        return False

    if not isinstance(
        player_state["introComplete"],
        bool,
    ):
        return False

    current_location = player_state["currentLocation"]

    if (
        not isinstance(current_location, str)
        or current_location not in locationRegistry
    ):
        return False

    for direction_field in [
        "currentDirection",
        "currentShortDirection",
        "lastDirection",
        "lastShortDirection",
    ]:
        direction = player_state[direction_field]

        if direction is not None and (
            not isinstance(direction, str) or not direction
        ):
            return False

    inventory = player_state["inventory"]
    equipped = player_state["equipped"]

    if not is_valid_item_id_list(inventory):
        return False

    if not is_valid_item_id_list(equipped):
        return False

    if any(
        item_id not in inventory
        for item_id in equipped
    ):
        return False

    equipped_slots = []

    for item_id in equipped:
        item = itemRegistry[item_id]
        slot = item.get(
            "slot",
        )

        if not item.get("wearable", False) or slot not in EQUIPMENT_SLOTS:
            return False

        equipped_slots.append(
            slot,
        )

    if len(equipped_slots) != len(set(equipped_slots)):
        return False

    health = player_state["health"]

    if not isinstance(health, str) or not health:
        return False

    return True


def is_valid_item_states(item_states):
    if not isinstance(
        item_states,
        dict,
    ):
        return False

    return all(
        isinstance(item_id, str)
        and item_id in itemRegistry
        and isinstance(item_state, dict)
        for item_id, item_state in item_states.items()
    )


def is_valid_location_state(
    location_id,
    location_state,
):
    if not isinstance(
        location_state,
        dict,
    ):
        return False

    for field in [
        "visited",
        "items",
        "scenery",
    ]:
        if field not in location_state:
            return False

    if not isinstance(
        location_state["visited"],
        bool,
    ):
        return False

    location_items = location_state["items"]
    scenery_states = location_state["scenery"]

    if not isinstance(location_items, dict) or not isinstance(
        scenery_states,
        dict,
    ):
        return False

    location_scenery = locationRegistry[location_id].get(
        "scenery",
        {},
    )

    for item_id, placement in location_items.items():
        if not isinstance(item_id, str) or item_id not in itemRegistry:
            return False

        if placement is None or placement == WORLD_ITEM_PLACEMENT:
            continue

        if not isinstance(placement, str) or placement not in location_scenery:
            return False

    return all(
        isinstance(scenery_id, str)
        and scenery_id in location_scenery
        and isinstance(scenery_state, dict)
        for scenery_id, scenery_state in scenery_states.items()
    )


def is_valid_locations_state(locations_state):
    if not isinstance(
        locations_state,
        dict,
    ):
        return False

    for location_id, location_state in locations_state.items():
        if (
            not isinstance(location_id, str)
            or location_id not in locationRegistry
            or not is_valid_location_state(
                location_id,
                location_state,
            )
        ):
            return False

    return True


def has_exclusive_item_ownership(
    player_state,
    locations_state,
):
    owned_item_ids = set(
        player_state["inventory"],
    )

    for location_state in locations_state.values():
        for item_id in location_state["items"]:
            if item_id in owned_item_ids:
                return False

            owned_item_ids.add(
                item_id,
            )

    for item_id in owned_item_ids:
        initial_location = INITIAL_ITEM_LOCATIONS.get(
            item_id,
        )

        if initial_location and initial_location not in locations_state:
            return False

    return True


def is_valid_saved_state(saved_state):
    if not isinstance(
        saved_state,
        dict,
    ):
        return False

    save_version = saved_state.get(
        "saveVersion",
    )

    if type(save_version) is not int or save_version != SAVE_VERSION:
        return False

    player_state = saved_state.get(
        "player",
    )

    if not is_valid_player_state(
        player_state,
    ):
        return False

    if not is_valid_item_states(
        saved_state.get(
            "itemStates",
        )
    ):
        return False

    if not isinstance(
        saved_state.get(
            "flags",
        ),
        dict,
    ):
        return False

    locations_state = saved_state.get(
        "locations",
    )

    if not is_valid_locations_state(
        locations_state,
    ):
        return False

    if not has_exclusive_item_ownership(
        player_state,
        locations_state,
    ):
        return False

    return True


def restore_game_state(saved_state):
    if not is_valid_saved_state(
        saved_state,
    ):
        return None

    restored_state = merge_state(
        initialState,
        saved_state,
    )

    return restored_state
