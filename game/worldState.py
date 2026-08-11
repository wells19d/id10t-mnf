from copy import deepcopy

from areas.locationRegistry import locationRegistry
from items.itemRegistry import itemRegistry
from states.gameState import (
    GAME_STATE_REQUIREMENT_KEYS,
    WORLD_ITEM_PLACEMENT,
)


def build_initial_location_items(location_definition):
    items = {}

    # Items that begin naturally in the location.
    for item_id in location_definition.get(
        "items",
        [],
    ):
        items[item_id] = WORLD_ITEM_PLACEMENT

    # Items that begin inside/on scenery.
    for scenery_id, scenery_data in location_definition.get(
        "scenery",
        {},
    ).items():
        for item_id in scenery_data.get(
            "items",
            [],
        ):
            items[item_id] = scenery_id

    # Real items may begin inside a world item container.
    for container_item_id, contained_item_ids in location_definition.get(
        "itemContents",
        {},
    ).items():
        for item_id in contained_item_ids:
            items[item_id] = container_item_id

    return items


def build_initial_scenery_state(location_definition):
    scenery_states = {}

    for scenery_id, scenery_data in location_definition.get(
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
    locations = game_state.setdefault(
        "locations",
        {},
    )

    if location_id not in locations:
        location_definition = locationRegistry.get(
            location_id,
            {},
        )

        locations[location_id] = {
            "visited": False,
            "items": build_initial_location_items(
                location_definition,
            ),
            "scenery": build_initial_scenery_state(
                location_definition,
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


def get_item_state_snapshot(
    game_state,
    item_id,
):
    existing_state = game_state.get(
        "itemStates",
        {},
    ).get(
        item_id,
    )

    if existing_state is not None:
        return deepcopy(
            existing_state,
        )

    return deepcopy(
        itemRegistry.get(
            item_id,
            {},
        ).get(
            "state",
            {},
        )
    )


def state_matches(
    current_state,
    required_state,
):
    for key, required_value in required_state.items():
        if current_state.get(key) != required_value:
            return False

    return True


def game_state_requirements_met(
    requirements,
    game_state,
):
    if not requirements:
        return True

    if any(key not in GAME_STATE_REQUIREMENT_KEYS for key in requirements):
        return False

    player_state = game_state["player"]

    if not state_matches(
        player_state,
        requirements.get(
            "player",
            {},
        ),
    ):
        return False

    inventory = player_state.get(
        "inventory",
        [],
    )

    for item_id in requirements.get(
        "inventory",
        [],
    ):
        if item_id not in itemRegistry or item_id not in inventory:
            return False

    equipped = player_state.get(
        "equipped",
        [],
    )

    for item_id in requirements.get(
        "equipped",
        [],
    ):
        if item_id not in itemRegistry or item_id not in equipped:
            return False

    if not state_matches(
        game_state["flags"],
        requirements.get(
            "flags",
            {},
        ),
    ):
        return False

    current_location = player_state["currentLocation"]
    current_location_definition = locationRegistry.get(
        current_location,
        {},
    )
    location_state = get_current_location_state(
        game_state,
    )

    for scenery_id, required_state in requirements.get(
        "sceneryState",
        {},
    ).items():
        if scenery_id not in current_location_definition.get(
            "scenery",
            {},
        ):
            return False

        scenery_state = get_scenery_state(
            location_state,
            scenery_id,
        )

        if not state_matches(
            scenery_state,
            required_state,
        ):
            return False

    for item_id, required_state in requirements.get(
        "itemStates",
        {},
    ).items():
        if item_id not in itemRegistry:
            return False

        item_state = get_item_state(
            game_state,
            item_id,
        )

        if not state_matches(
            item_state,
            required_state,
        ):
            return False

    return True


def get_location_description(
    location_data,
    game_state,
):
    for state_description in location_data.get(
        "stateDescriptions",
        [],
    ):
        if game_state_requirements_met(
            state_description.get(
                "requires",
                {},
            ),
            game_state,
        ):
            description = state_description.get(
                "description",
            )

            if description is not None:
                return description

    return location_data.get(
        "description",
        "There is nothing remarkable here.",
    )


def apply_state_changes(
    current_state,
    changes,
):
    if not changes:
        return

    current_state.update(
        changes,
    )
