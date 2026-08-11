from copy import deepcopy
import random

from areas.locationRegistry import locationRegistry
from items.itemRegistry import itemRegistry
from states.gameState import (
    GAME_STATE_REQUIREMENT_KEYS,
    WORLD_ITEM_PLACEMENT,
    get_total_carry_capacity,
    is_valid_pending_action,
)

VALID_RESPONSE_SPEAKERS = frozenset(
    {
        "narrator",
        "voice",
        "system",
    }
)


class CommandFailure:
    def __init__(self, response):
        self.response = response


def command_failure(response):
    return CommandFailure(
        response,
    )


def is_valid_response_message(
    message,
    allow_empty_text=False,
):
    if not isinstance(message, dict):
        return False

    speaker = message.get(
        "speaker",
    )
    text = message.get(
        "text",
    )

    if not isinstance(speaker, str) or speaker not in VALID_RESPONSE_SPEAKERS:
        return False

    if not isinstance(text, str):
        return False

    return allow_empty_text or bool(text.strip())


def is_valid_response(
    response,
    allow_empty_list=False,
    allow_empty_text=False,
):
    if isinstance(response, str):
        return allow_empty_text or bool(response.strip())

    if isinstance(response, dict):
        return is_valid_response_message(
            response,
            allow_empty_text,
        )

    if isinstance(response, list):
        if not response and not allow_empty_list:
            return False

        return all(
            is_valid_response_message(
                message,
                allow_empty_text,
            )
            for message in response
        )

    return False


def normalize_response_messages(
    response,
    default_speaker="narrator",
    allow_empty_list=False,
    allow_empty_text=False,
):
    if not is_valid_response(
        response,
        allow_empty_list,
        allow_empty_text,
    ):
        raise ValueError("Invalid response shape.")

    if isinstance(response, str):
        return [
            {
                "speaker": default_speaker,
                "text": response,
            }
        ]

    if isinstance(response, dict):
        return [
            response,
        ]

    return list(
        response,
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


def get_item_name(item):
    return item.get(
        "name",
        item["aliases"][0],
    )


def get_item_display_name(item):
    item_name = get_item_name(
        item,
    )

    highlight_class = (
        "equipment-highlight" if item.get("wearable", False) else "item-highlight"
    )

    return f"<em><span class='{highlight_class}'>" f"{item_name}" "</span></em>"


def get_carry_overflow_count(
    player_state,
    inventory=None,
    equipped=None,
):
    final_inventory = inventory if inventory is not None else player_state["inventory"]
    final_equipped = equipped if equipped is not None else player_state["equipped"]

    final_player_state = {
        **player_state,
        "inventory": final_inventory,
        "equipped": final_equipped,
    }

    return max(
        0,
        len(final_inventory)
        - get_total_carry_capacity(
            final_player_state,
        ),
    )


def select_overflow_items(
    inventory,
    overflow_count,
):
    if overflow_count <= 0:
        return []

    return random.sample(
        inventory,
        overflow_count,
    )


def place_items_loose(
    game_state,
    item_ids,
):
    if not item_ids:
        return

    location_state = get_current_location_state(
        game_state,
    )

    for item_id in item_ids:
        location_state["items"][item_id] = None


def get_formatted_item_list(item_ids):
    item_names = [
        get_item_display_name(
            itemRegistry[item_id],
        )
        for item_id in item_ids
    ]

    return format_item_names(
        item_names,
    )


def append_narrator_response(
    response,
    narrator_text,
):
    messages = normalize_response_messages(
        response,
    )

    messages.append(
        {
            "speaker": "narrator",
            "text": narrator_text,
        }
    )

    return messages


def get_pending_action_prompt(game_state):
    pending_action = game_state.get(
        "pendingAction",
    )

    if not pending_action:
        return None

    player_state = game_state["player"]
    action = pending_action["action"]
    item_id = pending_action["itemId"]
    item_name = get_item_display_name(
        itemRegistry[item_id],
    )

    if pending_action["type"] == "equippedDrop":
        return (
            f"The {item_name} is currently equipped. "
            "Drop it anyway? Yes or No."
        )

    if action == "wear":
        equipped_item_id = pending_action["equippedItemId"]
        equipped_item_name = get_item_display_name(
            itemRegistry[equipped_item_id],
        )
        final_inventory = [
            inventory_item_id
            for inventory_item_id in player_state["inventory"]
            if inventory_item_id != item_id
        ]
        final_equipped = [
            equipped_id
            for equipped_id in player_state["equipped"]
            if equipped_id != equipped_item_id
        ]
        final_equipped.append(
            item_id,
        )
        additional_drop_count = get_carry_overflow_count(
            player_state,
            final_inventory,
            final_equipped,
        )

        if additional_drop_count:
            drop_description = (
                f"the {equipped_item_name} and {additional_drop_count} "
                f"additional carried "
                f"{'item' if additional_drop_count == 1 else 'items'}"
            )
        else:
            drop_description = f"the {equipped_item_name}"

        return (
            f"The {item_name} has less carrying space. Equipping it will "
            f"cause {drop_description} to be dropped on the ground. "
            "Continue? Yes or No."
        )

    final_equipped = [
        equipped_id
        for equipped_id in player_state["equipped"]
        if equipped_id != item_id
    ]

    if action == "remove":
        final_inventory = [
            *player_state["inventory"],
            item_id,
        ]
        overflow_count = get_carry_overflow_count(
            player_state,
            final_inventory,
            final_equipped,
        )

        return (
            f"Removing the {item_name} will reduce your carrying space and "
            f"cause {overflow_count} carried "
            f"{'item' if overflow_count == 1 else 'items'} to fall to the "
            "ground. Continue? Yes or No."
        )

    overflow_count = get_carry_overflow_count(
        player_state,
        player_state["inventory"],
        final_equipped,
    )

    return (
        f"Dropping the {item_name} will reduce your carrying space and cause "
        f"{overflow_count} additional carried "
        f"{'item' if overflow_count == 1 else 'items'} to fall to the ground. "
        "Continue? Yes or No."
    )


def execute_pending_action(game_state):
    pending_action = game_state["pendingAction"]
    player_state = game_state["player"]

    if not is_valid_pending_action(
        pending_action,
        player_state,
    ):
        game_state["pendingAction"] = None

        return "That pending action can no longer be completed."

    action = pending_action["action"]
    item_id = pending_action["itemId"]
    item = itemRegistry[item_id]
    item_name = get_item_display_name(
        item,
    )

    if pending_action["type"] == "equippedDrop":
        player_state["equipped"] = [
            equipped_id
            for equipped_id in player_state["equipped"]
            if equipped_id != item_id
        ]
        place_items_loose(
            game_state,
            [item_id],
        )
        game_state["pendingAction"] = None

        return item.get(
            "dropResponse",
            f"You drop the {item_name}.",
        )

    if action == "wear":
        equipped_item_id = pending_action["equippedItemId"]
        final_inventory = [
            inventory_item_id
            for inventory_item_id in player_state["inventory"]
            if inventory_item_id != item_id
        ]
        final_equipped = [
            equipped_id
            for equipped_id in player_state["equipped"]
            if equipped_id != equipped_item_id
        ]
        final_equipped.append(
            item_id,
        )
        overflow_count = get_carry_overflow_count(
            player_state,
            final_inventory,
            final_equipped,
        )
        overflow_item_ids = select_overflow_items(
            final_inventory,
            overflow_count,
        )
        dropped_item_ids = [
            equipped_item_id,
            *overflow_item_ids,
        ]

        player_state["inventory"] = [
            inventory_item_id
            for inventory_item_id in final_inventory
            if inventory_item_id not in overflow_item_ids
        ]
        player_state["equipped"] = final_equipped
        place_items_loose(
            game_state,
            dropped_item_ids,
        )
        game_state["pendingAction"] = None

        response = item.get(
            "wearResponse",
            f"You equip the {item_name}.",
        )

        return append_narrator_response(
            response,
            "The reduced carrying space causes "
            f"{get_formatted_item_list(dropped_item_ids)} to fall to the ground.",
        )

    final_equipped = [
        equipped_id
        for equipped_id in player_state["equipped"]
        if equipped_id != item_id
    ]

    if action == "remove":
        final_inventory = [
            *player_state["inventory"],
            item_id,
        ]
        overflow_count = get_carry_overflow_count(
            player_state,
            final_inventory,
            final_equipped,
        )
        dropped_item_ids = select_overflow_items(
            final_inventory,
            overflow_count,
        )

        player_state["inventory"] = [
            inventory_item_id
            for inventory_item_id in final_inventory
            if inventory_item_id not in dropped_item_ids
        ]
        player_state["equipped"] = final_equipped
        place_items_loose(
            game_state,
            dropped_item_ids,
        )
        game_state["pendingAction"] = None

        response = item.get(
            "removeResponse",
            f"You remove the {item_name}.",
        )

        return append_narrator_response(
            response,
            "The reduced carrying space causes "
            f"{get_formatted_item_list(dropped_item_ids)} to fall to the ground.",
        )

    final_inventory = list(
        player_state["inventory"],
    )
    overflow_count = get_carry_overflow_count(
        player_state,
        final_inventory,
        final_equipped,
    )
    overflow_item_ids = select_overflow_items(
        final_inventory,
        overflow_count,
    )
    dropped_item_ids = [
        item_id,
        *overflow_item_ids,
    ]

    player_state["inventory"] = [
        inventory_item_id
        for inventory_item_id in final_inventory
        if inventory_item_id not in overflow_item_ids
    ]
    player_state["equipped"] = final_equipped
    place_items_loose(
        game_state,
        dropped_item_ids,
    )
    game_state["pendingAction"] = None

    response = item.get(
        "dropResponse",
        f"You drop the {item_name}.",
    )

    if not overflow_item_ids:
        return response

    return append_narrator_response(
        response,
        "The reduced carrying space also causes "
        f"{get_formatted_item_list(overflow_item_ids)} to fall to the ground.",
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

        scenery_data = location_definition.get(
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
