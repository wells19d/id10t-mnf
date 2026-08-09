from areas.clearing import clearing
from areas.fallen_nursery import fallen_nursery
from areas.house_1 import house_1
from areas.house_2 import house_2
from areas.house_3 import house_3
from areas.lake_east import lake_east
from areas.lake_south import lake_south
from areas.massive_tree import massive_tree
from areas.road_access import road_access
from areas.security_gate import security_gate
from areas.silent_grove import silent_grove
from areas.stone_ring import stone_ring
from game.itemRegistry import (
    get_item_definition_errors,
    itemRegistry,
)
from states.gameState import GAME_STATE_REQUIREMENT_KEYS

areaRegistry = {
    "clearing": clearing,
    "fallen_nursery": fallen_nursery,
    "house_1": house_1,
    "house_2": house_2,
    "house_3": house_3,
    "lake_east": lake_east,
    "lake_south": lake_south,
    "massive_tree": massive_tree,
    "road_access": road_access,
    "security_gate": security_gate,
    "silent_grove": silent_grove,
    "stone_ring": stone_ring,
}

DIRECTIONS = {
    "north",
    "south",
    "east",
    "west",
}

ACTION_REQUIREMENT_KEYS = {
    "itemState",
    "sceneryState",
    "inventory",
    "equipped",
    "flags",
}

ACTION_EFFECT_KEYS = {
    "sceneryState",
    "itemState",
    "flags",
    "destroyItem",
}


def add_item_reference_errors(
    item_ids,
    definition_path,
    errors,
):
    if not isinstance(item_ids, list):
        errors.append(
            f"{definition_path} must be a list of registered item IDs."
        )
        return

    for item_id in item_ids:
        if not isinstance(item_id, str) or item_id not in itemRegistry:
            errors.append(
                f"{definition_path} references unknown item ID {item_id!r}."
            )


def add_requirement_errors(
    requirements,
    definition_path,
    errors,
    allowed_keys,
    scenery_ids=None,
    scenery_state_is_map=False,
):
    if not isinstance(requirements, dict):
        errors.append(
            f"{definition_path} must be a dictionary."
        )
        return

    for key in requirements:
        if key not in allowed_keys:
            errors.append(
                f"{definition_path} uses unsupported requirement {key!r}."
            )

    for item_list_key in [
        "inventory",
        "equipped",
    ]:
        if item_list_key in requirements:
            add_item_reference_errors(
                requirements[item_list_key],
                f"{definition_path}.{item_list_key}",
                errors,
            )

    dictionary_keys = {
        "player",
        "flags",
        "itemState",
        "sceneryState",
        "itemStates",
    }

    for key in dictionary_keys.intersection(requirements):
        if not isinstance(requirements[key], dict):
            errors.append(
                f"{definition_path}.{key} must be a dictionary."
            )

    item_states = requirements.get(
        "itemStates",
        {},
    )

    if isinstance(item_states, dict):
        for item_id in item_states:
            if item_id not in itemRegistry:
                errors.append(
                    f"{definition_path}.itemStates references unknown item ID "
                    f"{item_id!r}."
                )

    scenery_states = requirements.get(
        "sceneryState",
        {},
    )

    if (
        scenery_state_is_map
        and isinstance(scenery_states, dict)
        and scenery_ids is not None
    ):
        for scenery_id in scenery_states:
            if scenery_id not in scenery_ids:
                errors.append(
                    f"{definition_path}.sceneryState references unknown scenery "
                    f"ID {scenery_id!r}."
                )


def add_effect_errors(
    effects,
    definition_path,
    errors,
):
    if not isinstance(effects, dict):
        errors.append(
            f"{definition_path} must be a dictionary."
        )
        return

    for key in effects:
        if key not in ACTION_EFFECT_KEYS:
            errors.append(
                f"{definition_path} uses unsupported effect {key!r}."
            )

    for key in [
        "sceneryState",
        "itemState",
        "flags",
    ]:
        if key in effects and not isinstance(
            effects[key],
            dict,
        ):
            errors.append(
                f"{definition_path}.{key} must be a dictionary."
            )

    if "destroyItem" in effects and not isinstance(
        effects["destroyItem"],
        bool,
    ):
        errors.append(
            f"{definition_path}.destroyItem must be a boolean."
        )


def add_scenery_errors(
    location_path,
    scenery,
    errors,
    initial_item_placements,
):
    for scenery_id, scenery_data in scenery.items():
        scenery_path = f"{location_path}.scenery[{scenery_id!r}]"

        if not isinstance(scenery_data, dict):
            errors.append(
                f"{scenery_path} must be a dictionary."
            )
            continue

        aliases = scenery_data.get(
            "aliases",
            [],
        )

        if not isinstance(aliases, list) or not all(
            isinstance(alias, str)
            and alias.strip()
            and alias == alias.lower()
            for alias in aliases
        ):
            errors.append(
                f"{scenery_path}.aliases must be a list of lowercase strings."
            )

        if "state" in scenery_data and not isinstance(
            scenery_data["state"],
            dict,
        ):
            errors.append(
                f"{scenery_path}.state must be a dictionary."
            )

        scenery_items = scenery_data.get(
            "items",
            [],
        )
        item_path = f"{scenery_path}.items"
        add_item_reference_errors(
            scenery_items,
            item_path,
            errors,
        )

        if isinstance(scenery_items, list):
            for item_id in scenery_items:
                if item_id in itemRegistry:
                    initial_item_placements.setdefault(
                        item_id,
                        [],
                    ).append(
                        item_path
                    )

        for interaction_key in [
            "interactions",
            "throwInteractions",
        ]:
            interactions = scenery_data.get(
                interaction_key,
                {},
            )

            if not isinstance(interactions, dict):
                errors.append(
                    f"{scenery_path}.{interaction_key} must be a dictionary."
                )
                continue

            for item_id, interaction in interactions.items():
                interaction_path = (
                    f"{scenery_path}.{interaction_key}[{item_id!r}]"
                )

                if item_id not in itemRegistry:
                    errors.append(
                        f"{interaction_path} references unknown item ID {item_id!r}."
                    )

                if not isinstance(interaction, dict):
                    errors.append(
                        f"{interaction_path} must be a dictionary."
                    )
                    continue

                if interaction_key == "interactions":
                    if "requires" in interaction:
                        add_requirement_errors(
                            interaction["requires"],
                            f"{interaction_path}.requires",
                            errors,
                            ACTION_REQUIREMENT_KEYS,
                        )

                    if "effects" in interaction:
                        add_effect_errors(
                            interaction["effects"],
                            f"{interaction_path}.effects",
                            errors,
                        )

        for requirement_key in [
            "openRequires",
            "closeRequires",
        ]:
            if requirement_key in scenery_data:
                add_requirement_errors(
                    scenery_data[requirement_key],
                    f"{scenery_path}.{requirement_key}",
                    errors,
                    ACTION_REQUIREMENT_KEYS,
                )


def add_exit_errors(
    location_path,
    exits,
    scenery_ids,
    errors,
):
    if not isinstance(exits, dict):
        errors.append(
            f"{location_path}.exits must be a dictionary."
        )
        return

    exit_requirement_keys = {
        "inventory",
        "equipped",
        "flags",
        "sceneryState",
    }

    for direction, exit_data in exits.items():
        exit_path = f"{location_path}.exits[{direction!r}]"

        if direction not in DIRECTIONS:
            errors.append(
                f"{exit_path} uses an unsupported direction."
            )

        if exit_data is False or exit_data is None:
            continue

        if isinstance(exit_data, str):
            destination = exit_data
        elif isinstance(exit_data, dict):
            destination = exit_data.get(
                "location",
            )

            if "requires" in exit_data:
                add_requirement_errors(
                    exit_data["requires"],
                    f"{exit_path}.requires",
                    errors,
                    exit_requirement_keys,
                    scenery_ids,
                    True,
                )
        else:
            errors.append(
                f"{exit_path} must be a location ID, dictionary, or False."
            )
            continue

        if destination not in areaRegistry:
            errors.append(
                f"{exit_path} references unknown location ID {destination!r}."
            )


def add_state_description_errors(
    location_path,
    state_descriptions,
    scenery_ids,
    errors,
):
    if not isinstance(state_descriptions, list):
        errors.append(
            f"{location_path}.stateDescriptions must be a list."
        )
        return

    for index, state_description in enumerate(state_descriptions):
        state_path = f"{location_path}.stateDescriptions[{index}]"

        if not isinstance(state_description, dict):
            errors.append(
                f"{state_path} must be a dictionary."
            )
            continue

        description = state_description.get(
            "description",
        )

        if not isinstance(description, str) or not description.strip():
            errors.append(
                f"{state_path}.description must be a non-empty string."
            )

        add_requirement_errors(
            state_description.get(
                "requires",
                {},
            ),
            f"{state_path}.requires",
            errors,
            GAME_STATE_REQUIREMENT_KEYS,
            scenery_ids,
            True,
        )


def get_area_definition_errors():
    errors = []
    initial_item_placements = {}

    for location_id, location_data in areaRegistry.items():
        location_path = f"areaRegistry[{location_id!r}]"

        if not isinstance(location_data, dict):
            errors.append(
                f"{location_path} must be a dictionary."
            )
            continue

        for text_key in [
            "name",
            "description",
        ]:
            text = location_data.get(
                text_key,
            )

            if not isinstance(text, str) or not text.strip():
                errors.append(
                    f"{location_path}.{text_key} must be a non-empty string."
                )

        location_items = location_data.get(
            "items",
            [],
        )
        item_path = f"{location_path}.items"
        add_item_reference_errors(
            location_items,
            item_path,
            errors,
        )

        if isinstance(location_items, list):
            for item_id in location_items:
                if item_id in itemRegistry:
                    initial_item_placements.setdefault(
                        item_id,
                        [],
                    ).append(
                        item_path
                    )

        scenery = location_data.get(
            "scenery",
            {},
        )

        if not isinstance(scenery, dict):
            errors.append(
                f"{location_path}.scenery must be a dictionary."
            )
            scenery = {}

        scenery_ids = set(
            scenery,
        )

        add_scenery_errors(
            location_path,
            scenery,
            errors,
            initial_item_placements,
        )
        add_exit_errors(
            location_path,
            location_data.get(
                "exits",
            ),
            scenery_ids,
            errors,
        )
        add_state_description_errors(
            location_path,
            location_data.get(
                "stateDescriptions",
                [],
            ),
            scenery_ids,
            errors,
        )

        area_interactions = location_data.get(
            "interactions",
            {},
        )

        if not isinstance(area_interactions, dict):
            errors.append(
                f"{location_path}.interactions must be a dictionary."
            )
        else:
            for scenery_id, interaction in area_interactions.items():
                interaction_path = (
                    f"{location_path}.interactions[{scenery_id!r}]"
                )

                if scenery_id not in scenery_ids:
                    errors.append(
                        f"{interaction_path} references unknown scenery ID "
                        f"{scenery_id!r}."
                    )

                if not isinstance(interaction, dict):
                    errors.append(
                        f"{interaction_path} must be a dictionary."
                    )
                    continue

                if interaction.get("type") == "combination":
                    combination = interaction.get(
                        "combination",
                    )

                    if not isinstance(combination, list) or not all(
                        isinstance(value, str) and value.isdigit()
                        for value in combination
                    ):
                        errors.append(
                            f"{interaction_path}.combination must be a list "
                            "of numeric strings."
                        )

    for item_id, placements in initial_item_placements.items():
        if len(placements) > 1:
            errors.append(
                f"Item ID {item_id!r} has multiple initial placements: "
                f"{', '.join(placements)}."
            )

    return errors


def validate_game_definitions():
    errors = get_item_definition_errors() + get_area_definition_errors()

    if errors:
        formatted_errors = "\n".join(
            f"- {error}"
            for error in errors
        )

        raise ValueError(
            "Invalid game definitions:\n"
            f"{formatted_errors}"
        )


validate_game_definitions()
