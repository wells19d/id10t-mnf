from game.responses import VALID_RESPONSE_SPEAKERS
from items.itemRegistry import itemRegistry


ACTION_EFFECT_KEYS = {
    "sceneryState",
    "itemState",
    "flags",
    "destroyItem",
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


def add_integer_map_errors(
    values,
    definition_path,
    errors,
    require_positive=False,
):
    if not isinstance(values, dict):
        errors.append(
            f"{definition_path} must be a dictionary."
        )
        return

    for state_key, value in values.items():
        if not isinstance(state_key, str) or not state_key:
            errors.append(
                f"{definition_path} must use non-empty string state keys."
            )

        if type(value) is not int or (require_positive and value <= 0):
            value_requirement = "a positive integer" if require_positive else "an integer"
            errors.append(
                f"{definition_path}[{state_key!r}] must be {value_requirement}."
            )
