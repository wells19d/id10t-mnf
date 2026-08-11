from areas.locationRegistry import (
    locationDefinitionsByArea,
    locationRegistry,
)
from game.handlers.common import VALID_RESPONSE_SPEAKERS
from items.itemRegistry import (
    itemDefinitionsByArea,
    itemRegistry,
)
from states.gameState import (
    EQUIPMENT_SLOTS,
    GAME_STATE_REQUIREMENT_KEYS,
)

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

COMBINATION_EFFECT_KEYS = {
    "sceneryState",
}

ITEM_RESPONSE_KEYS = {
    "takeFail",
    "takeResponse",
    "dropResponse",
    "wearFailResponse",
    "alreadyWearingResponse",
    "wearResponse",
    "removeResponse",
}

SCENERY_RESPONSE_KEYS = {
    "takeFail",
    "takeClosedResponse",
    "takeBlockedResponse",
    "searchResponse",
    "searchClosedResponse",
    "searchBlockedResponse",
    "searchEmptyResponse",
    "openFailResponse",
    "brokenOpenResponse",
    "lockedResponse",
    "alreadyOpenResponse",
    "openBlockedResponse",
    "openResponse",
    "closeFailResponse",
    "brokenCloseResponse",
    "alreadyClosedResponse",
    "closeBlockedResponse",
    "closeResponse",
}


def add_message_errors(
    message,
    definition_path,
    errors,
    allow_empty_text=False,
):
    if not isinstance(message, dict):
        errors.append(
            f"{definition_path} must be a response message dictionary."
        )
        return

    speaker = message.get(
        "speaker",
    )

    if (
        not isinstance(speaker, str)
        or speaker not in VALID_RESPONSE_SPEAKERS
    ):
        errors.append(
            f"{definition_path}.speaker must be one of: "
            f"{', '.join(sorted(VALID_RESPONSE_SPEAKERS))}."
        )

    text = message.get(
        "text",
    )

    if not isinstance(text, str) or (
        not allow_empty_text
        and not text.strip()
    ):
        text_requirement = (
            "a string"
            if allow_empty_text
            else "a non-empty string"
        )
        errors.append(
            f"{definition_path}.text must be {text_requirement}."
        )


def add_response_errors(
    response,
    definition_path,
    errors,
):
    if isinstance(response, str):
        if not response.strip():
            errors.append(
                f"{definition_path} must not be empty."
            )
        return

    if isinstance(response, dict):
        add_message_errors(
            response,
            definition_path,
            errors,
        )
        return

    if isinstance(response, list):
        if not response:
            errors.append(
                f"{definition_path} must not be an empty response list."
            )
            return

        for index, message in enumerate(response):
            add_message_errors(
                message,
                f"{definition_path}[{index}]",
                errors,
            )
        return

    errors.append(
        f"{definition_path} must be a response string, message, or message list."
    )


def add_intro_response_errors(
    response,
    definition_path,
    errors,
):
    if isinstance(response, str):
        return

    if isinstance(response, dict):
        add_message_errors(
            response,
            definition_path,
            errors,
            allow_empty_text=True,
        )
        return

    if isinstance(response, list):
        for index, message in enumerate(response):
            add_message_errors(
                message,
                f"{definition_path}[{index}]",
                errors,
                allow_empty_text=True,
            )
        return

    errors.append(
        f"{definition_path} must be an intro string, message, or message list."
    )


def add_definition_source_errors(
    definitions_by_area,
    definition_label,
    source_label,
    errors,
):
    definition_sources = {}

    if not isinstance(definitions_by_area, dict):
        errors.append(
            f"{source_label} must be a dictionary of definition groups."
        )
        return

    for area_id, definitions in definitions_by_area.items():
        source_path = f"{source_label}[{area_id!r}]"

        if not isinstance(area_id, str) or not area_id:
            errors.append(
                f"{source_path} must use a non-empty string group ID."
            )

        if not isinstance(definitions, (list, tuple)):
            errors.append(
                f"{source_path} must be an ordered list of ID/definition pairs."
            )
            continue

        for index, entry in enumerate(definitions):
            entry_path = f"{source_path}[{index}]"

            if not isinstance(entry, (list, tuple)) or len(entry) != 2:
                errors.append(
                    f"{entry_path} must contain an ID and definition."
                )
                continue

            definition_id, _ = entry

            if not isinstance(definition_id, str) or not definition_id:
                errors.append(
                    f"{entry_path} must use a non-empty string ID."
                )
                continue

            if definition_id in definition_sources:
                errors.append(
                    f"{definition_label} ID {definition_id!r} is defined in both "
                    f"{definition_sources[definition_id]!r} and {area_id!r}."
                )
                continue

            definition_sources[definition_id] = area_id


def add_local_state_description_errors(
    state_descriptions,
    definition_path,
    errors,
):
    if not isinstance(state_descriptions, list):
        errors.append(
            f"{definition_path} must be a list."
        )
        return

    for index, state_description in enumerate(state_descriptions):
        state_path = f"{definition_path}[{index}]"

        if not isinstance(state_description, dict):
            errors.append(
                f"{state_path} must be a dictionary."
            )
            continue

        if not isinstance(
            state_description.get(
                "requiresState",
            ),
            dict,
        ):
            errors.append(
                f"{state_path}.requiresState must be a dictionary."
            )

        description = state_description.get(
            "description",
        )

        if not isinstance(description, str) or not description.strip():
            errors.append(
                f"{state_path}.description must be a non-empty string."
            )


def add_throw_action_errors(
    throw_action,
    definition_path,
    errors,
):
    if not isinstance(throw_action, dict):
        errors.append(
            f"{definition_path} must be a dictionary."
        )
        return

    add_response_errors(
        throw_action.get(
            "response",
        ),
        f"{definition_path}.response",
        errors,
    )

    if "destroyItem" in throw_action and not isinstance(
        throw_action["destroyItem"],
        bool,
    ):
        errors.append(
            f"{definition_path}.destroyItem must be a boolean."
        )


def get_item_definition_errors():
    errors = []

    add_definition_source_errors(
        itemDefinitionsByArea,
        "Item",
        "itemDefinitionsByArea",
        errors,
    )

    for item_id, item_data in itemRegistry.items():
        item_path = f"itemRegistry[{item_id!r}]"

        if not isinstance(item_id, str) or not item_id:
            errors.append(
                f"{item_path} must use a non-empty string ID."
            )

        if not isinstance(item_data, dict):
            errors.append(
                f"{item_path} must be a dictionary."
            )
            continue

        name = item_data.get(
            "name",
        )

        if not isinstance(name, str) or not name.strip():
            errors.append(
                f"{item_path}.name must be a non-empty string."
            )

        aliases = item_data.get(
            "aliases",
        )

        if not isinstance(aliases, list) or not aliases:
            errors.append(
                f"{item_path}.aliases must be a non-empty list."
            )
        else:
            for alias in aliases:
                if not isinstance(alias, str) or not alias.strip():
                    errors.append(
                        f"{item_path}.aliases contains an invalid alias."
                    )
                elif alias != alias.lower():
                    errors.append(
                        f"{item_path}.aliases must use lowercase text: {alias!r}."
                    )

            if (
                all(
                    isinstance(alias, str)
                    for alias in aliases
                )
                and len(aliases) != len(set(aliases))
            ):
                errors.append(
                    f"{item_path}.aliases contains duplicate aliases."
                )

        for boolean_key in [
            "takeable",
            "wearable",
        ]:
            if boolean_key in item_data and not isinstance(
                item_data[boolean_key],
                bool,
            ):
                errors.append(
                    f"{item_path}.{boolean_key} must be a boolean."
                )

        if item_data.get(
            "wearable",
            False,
        ):
            slot = item_data.get(
                "slot",
            )

            if not isinstance(slot, str) or slot not in EQUIPMENT_SLOTS:
                errors.append(
                    f"{item_path}.slot must be one of: "
                    f"{', '.join(sorted(EQUIPMENT_SLOTS))}."
                )

        if "carryCapacity" in item_data:
            carry_capacity = item_data["carryCapacity"]

            if (
                type(carry_capacity) is not int
                or carry_capacity <= 0
            ):
                errors.append(
                    f"{item_path}.carryCapacity must be a positive integer."
                )

            if (
                not item_data.get("wearable", False)
                or item_data.get("slot") != "back"
            ):
                errors.append(
                    f"{item_path}.carryCapacity requires a wearable back-slot item."
                )

        for text_key in [
            "description",
            "worldDescription",
            "looseDescription",
        ]:
            if text_key in item_data and (
                not isinstance(item_data[text_key], str)
                or not item_data[text_key].strip()
            ):
                errors.append(
                    f"{item_path}.{text_key} must be a non-empty string."
                )

        for response_key in ITEM_RESPONSE_KEYS.intersection(item_data):
            add_response_errors(
                item_data[response_key],
                f"{item_path}.{response_key}",
                errors,
            )

        if "state" in item_data and not isinstance(
            item_data["state"],
            dict,
        ):
            errors.append(
                f"{item_path}.state must be a dictionary."
            )

        if "stateDescriptions" in item_data:
            add_local_state_description_errors(
                item_data["stateDescriptions"],
                f"{item_path}.stateDescriptions",
                errors,
            )

        if "onThrow" in item_data:
            throw_actions = item_data["onThrow"]

            if not isinstance(throw_actions, dict):
                errors.append(
                    f"{item_path}.onThrow must be a dictionary."
                )
            else:
                for action_id, throw_action in throw_actions.items():
                    action_path = f"{item_path}.onThrow[{action_id!r}]"

                    if not isinstance(action_id, str) or not action_id:
                        errors.append(
                            f"{action_path} must use a non-empty string ID."
                        )

                    if action_id != "default":
                        errors.append(
                            f"{action_path} uses unsupported action "
                            f"{action_id!r}; item onThrow only supports 'default'."
                        )

                    add_throw_action_errors(
                        throw_action,
                        action_path,
                        errors,
                    )

    return errors


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
        for item_id, required_state in item_states.items():
            if item_id not in itemRegistry:
                errors.append(
                    f"{definition_path}.itemStates references unknown item ID "
                    f"{item_id!r}."
                )

            if not isinstance(required_state, dict):
                errors.append(
                    f"{definition_path}.itemStates[{item_id!r}] "
                    "must be a dictionary."
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
        for scenery_id, required_state in scenery_states.items():
            if scenery_id not in scenery_ids:
                errors.append(
                    f"{definition_path}.sceneryState references unknown scenery "
                    f"ID {scenery_id!r}."
                )

            if not isinstance(required_state, dict):
                errors.append(
                    f"{definition_path}.sceneryState[{scenery_id!r}] "
                    "must be a dictionary."
                )


def add_effect_errors(
    effects,
    definition_path,
    errors,
    allowed_keys=ACTION_EFFECT_KEYS,
):
    if not isinstance(effects, dict):
        errors.append(
            f"{definition_path} must be a dictionary."
        )
        return

    for key in effects:
        if key not in allowed_keys:
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

        if not isinstance(scenery_id, str) or not scenery_id:
            errors.append(
                f"{scenery_path} must use a non-empty string ID."
            )

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

        if "description" in scenery_data and (
            not isinstance(scenery_data["description"], str)
            or not scenery_data["description"].strip()
        ):
            errors.append(
                f"{scenery_path}.description must be a non-empty string."
            )

        for boolean_key in [
            "searchable",
            "openable",
            "closeable",
        ]:
            if boolean_key in scenery_data and not isinstance(
                scenery_data[boolean_key],
                bool,
            ):
                errors.append(
                    f"{scenery_path}.{boolean_key} must be a boolean."
                )

        for response_key in SCENERY_RESPONSE_KEYS.intersection(scenery_data):
            add_response_errors(
                scenery_data[response_key],
                f"{scenery_path}.{response_key}",
                errors,
            )

        if "state" in scenery_data and not isinstance(
            scenery_data["state"],
            dict,
        ):
            errors.append(
                f"{scenery_path}.state must be a dictionary."
            )

        if "stateDescriptions" in scenery_data:
            add_local_state_description_errors(
                scenery_data["stateDescriptions"],
                f"{scenery_path}.stateDescriptions",
                errors,
            )

        for state_key in [
            "contentsRequiresState",
            "openEffects",
            "closeEffects",
        ]:
            if state_key in scenery_data and not isinstance(
                scenery_data[state_key],
                dict,
            ):
                errors.append(
                    f"{scenery_path}.{state_key} must be a dictionary."
                )

        item_descriptions = scenery_data.get(
            "itemDescriptions",
            {},
        )

        if not isinstance(item_descriptions, dict):
            errors.append(
                f"{scenery_path}.itemDescriptions must be a dictionary."
            )
        else:
            for item_id, description in item_descriptions.items():
                description_path = (
                    f"{scenery_path}.itemDescriptions[{item_id!r}]"
                )

                if not isinstance(item_id, str) or item_id not in itemRegistry:
                    errors.append(
                        f"{description_path} references unknown item ID "
                        f"{item_id!r}."
                    )

                if not isinstance(description, str) or not description.strip():
                    errors.append(
                        f"{description_path} must be a non-empty string."
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
                if isinstance(item_id, str) and item_id in itemRegistry:
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

                if not isinstance(item_id, str) or item_id not in itemRegistry:
                    errors.append(
                        f"{interaction_path} references unknown item ID {item_id!r}."
                    )

                if not isinstance(interaction, dict):
                    errors.append(
                        f"{interaction_path} must be a dictionary."
                    )
                    continue

                if interaction_key == "interactions":
                    for response_key in [
                        "response",
                        "failResponse",
                    ]:
                        if response_key in interaction:
                            add_response_errors(
                                interaction[response_key],
                                f"{interaction_path}.{response_key}",
                                errors,
                            )

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
                else:
                    add_throw_action_errors(
                        interaction,
                        interaction_path,
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

    exit_keys = {
        "location",
        "requires",
        "blockedResponse",
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
            for key in exit_data:
                if key not in exit_keys:
                    errors.append(
                        f"{exit_path} uses unsupported exit field {key!r}."
                    )

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

            if "blockedResponse" in exit_data:
                add_response_errors(
                    exit_data["blockedResponse"],
                    f"{exit_path}.blockedResponse",
                    errors,
                )
        else:
            errors.append(
                f"{exit_path} must be a location ID, dictionary, or False."
            )
            continue

        if (
            not isinstance(destination, str)
            or destination not in locationRegistry
        ):
            errors.append(
                f"{exit_path} references unknown location ID {destination!r}."
            )


def add_room_exit_errors(
    location_path,
    room_exits,
    errors,
):
    if not isinstance(room_exits, dict):
        errors.append(
            f"{location_path}.roomExits must be a dictionary."
        )
        return

    for room_name, destination in room_exits.items():
        room_exit_path = f"{location_path}.roomExits[{room_name!r}]"

        if not isinstance(room_name, str) or not room_name.strip():
            errors.append(
                f"{room_exit_path} must use a non-empty string room name."
            )

        if (
            not isinstance(destination, str)
            or destination not in locationRegistry
        ):
            errors.append(
                f"{room_exit_path} references unknown location ID "
                f"{destination!r}."
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


def get_location_definition_errors():
    errors = []
    initial_item_placements = {}

    add_definition_source_errors(
        locationDefinitionsByArea,
        "Location",
        "locationDefinitionsByArea",
        errors,
    )

    for location_id, location_data in locationRegistry.items():
        location_path = f"locationRegistry[{location_id!r}]"

        if not isinstance(location_id, str) or not location_id:
            errors.append(
                f"{location_path} must use a non-empty string ID."
            )

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

        if "intro" in location_data:
            add_intro_response_errors(
                location_data["intro"],
                f"{location_path}.intro",
                errors,
            )

        if "searchVoice" in location_data:
            add_response_errors(
                location_data["searchVoice"],
                f"{location_path}.searchVoice",
                errors,
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
                if isinstance(item_id, str) and item_id in itemRegistry:
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
        if "roomExits" in location_data:
            add_room_exit_errors(
                location_path,
                location_data["roomExits"],
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

        location_interactions = location_data.get(
            "interactions",
            {},
        )

        if not isinstance(location_interactions, dict):
            errors.append(
                f"{location_path}.interactions must be a dictionary."
            )
        else:
            for scenery_id, interaction in location_interactions.items():
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

                interaction_type = interaction.get(
                    "type",
                )

                if interaction_type != "combination":
                    errors.append(
                        f"{interaction_path}.type must be 'combination'."
                    )
                    continue

                if interaction_type == "combination":
                    combination = interaction.get(
                        "combination",
                    )

                    if (
                        not isinstance(combination, list)
                        or not combination
                        or not all(
                            isinstance(value, str) and value.isdigit()
                            for value in combination
                        )
                    ):
                        errors.append(
                            f"{interaction_path}.combination must be a non-empty "
                            "list of numeric strings."
                        )

                    for response_key in [
                        "onSuccess",
                        "onFail",
                    ]:
                        add_response_errors(
                            interaction.get(
                                response_key,
                            ),
                            f"{interaction_path}.{response_key}",
                            errors,
                        )

                    effects = interaction.get(
                        "effects",
                    )

                    add_effect_errors(
                        effects,
                        f"{interaction_path}.effects",
                        errors,
                        COMBINATION_EFFECT_KEYS,
                    )

                    if isinstance(effects, dict):
                        scenery_effects = effects.get(
                            "sceneryState",
                        )

                        if (
                            not isinstance(scenery_effects, dict)
                            or not scenery_effects
                        ):
                            errors.append(
                                f"{interaction_path}.effects.sceneryState "
                                "must be a non-empty dictionary."
                            )

    for item_id, placements in initial_item_placements.items():
        if len(placements) > 1:
            errors.append(
                f"Item ID {item_id!r} has multiple initial placements: "
                f"{', '.join(placements)}."
            )

    return errors


def validate_game_definitions():
    errors = get_item_definition_errors() + get_location_definition_errors()

    if errors:
        formatted_errors = "\n".join(
            f"- {error}"
            for error in errors
        )

        raise ValueError(
            "Invalid game definitions:\n"
            f"{formatted_errors}"
        )
