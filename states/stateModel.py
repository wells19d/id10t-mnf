from copy import deepcopy

from areas.locationRegistry import locationRegistry
from items.itemRegistry import itemRegistry


SAVE_VERSION = 1


WORLD_ITEM_PLACEMENT = "__world__"


EQUIPMENT_SLOT_ORDER = (
    "head",
    "chest",
    "outerwear",
    "hands",
    "legs",
    "feet",
    "back",
    "accessory",
)


EQUIPMENT_SLOTS = frozenset(
    EQUIPMENT_SLOT_ORDER,
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


BASE_CARRY_LIMIT = 10


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
        "equipped": [
            "a1_light_blue_dress_shirt",
            "a1_loose_fit_blue_jeans",
            "a1_grey_casual_shoes",
        ],
        "health": "Medium",
        "healthStatus": "You are slightly wounded. You have a small cut on your head, but the bleeding has stopped.",
    },
    "itemStates": {},
    "flags": {},
    "locations": {},
    "pendingAction": None,
}


def build_initial_item_locations():
    initial_item_locations = {}

    for location_id, location_definition in locationRegistry.items():
        for item_id in location_definition.get(
            "items",
            [],
        ):
            initial_item_locations[item_id] = location_id

        for contained_item_ids in location_definition.get(
            "itemContents",
            {},
        ).values():
            for item_id in contained_item_ids:
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


def get_total_carry_capacity(player_state):
    total_capacity = BASE_CARRY_LIMIT

    for item_id in player_state.get(
        "equipped",
        [],
    ):
        item = itemRegistry.get(
            item_id,
            {},
        )

        total_capacity += item.get(
            "carryCapacity",
            0,
        )

    return total_capacity
