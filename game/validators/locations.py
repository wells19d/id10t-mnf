from areas.registry import (
    locationDefinitionsByArea,
    locationRegistry,
)
from game.validators.common import (
    checkDefSource,
    checkEffects,
    checkIntroResponse,
    checkItemRefs,
    checkLocalStateText,
    checkRequirements,
    checkResponse,
    checkThrow,
)
from items.registry import itemRegistry
from states.game import GAME_STATE_REQUIREMENT_KEYS

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


COMBINATION_EFFECT_KEYS = {
    "sceneryState",
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


def checkScenery(
    location_path,
    scenery,
    errors,
    initial_item_placements,
):
    for scenery_id, scenery_data in scenery.items():
        scenery_path = f"{location_path}.scenery[{scenery_id!r}]"

        if not isinstance(scenery_id, str) or not scenery_id:
            errors.append(f"{scenery_path} must use a non-empty string ID.")

        if not isinstance(scenery_data, dict):
            errors.append(f"{scenery_path} must be a dictionary.")
            continue

        aliases = scenery_data.get(
            "aliases",
            [],
        )

        if not isinstance(aliases, list) or not all(
            isinstance(alias, str) and alias.strip() and alias == alias.lower()
            for alias in aliases
        ):
            errors.append(
                f"{scenery_path}.aliases must be a list of lowercase strings."
            )

        if "description" in scenery_data and (
            not isinstance(scenery_data["description"], str)
            or not scenery_data["description"].strip()
        ):
            errors.append(f"{scenery_path}.description must be a non-empty string.")

        for boolean_key in [
            "searchable",
            "openable",
            "closeable",
        ]:
            if boolean_key in scenery_data and not isinstance(
                scenery_data[boolean_key],
                bool,
            ):
                errors.append(f"{scenery_path}.{boolean_key} must be a boolean.")

        for response_key in SCENERY_RESPONSE_KEYS.intersection(scenery_data):
            checkResponse(
                scenery_data[response_key],
                f"{scenery_path}.{response_key}",
                errors,
            )

        if "state" in scenery_data and not isinstance(
            scenery_data["state"],
            dict,
        ):
            errors.append(f"{scenery_path}.state must be a dictionary.")

        if "stateDescriptions" in scenery_data:
            checkLocalStateText(
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
                errors.append(f"{scenery_path}.{state_key} must be a dictionary.")

        item_descriptions = scenery_data.get(
            "itemDescriptions",
            {},
        )

        if not isinstance(item_descriptions, dict):
            errors.append(f"{scenery_path}.itemDescriptions must be a dictionary.")
        else:
            for item_id, description in item_descriptions.items():
                description_path = f"{scenery_path}.itemDescriptions[{item_id!r}]"

                if not isinstance(item_id, str) or item_id not in itemRegistry:
                    errors.append(
                        f"{description_path} references unknown item ID "
                        f"{item_id!r}."
                    )

                if not isinstance(description, str) or not description.strip():
                    errors.append(f"{description_path} must be a non-empty string.")

        scenery_items = scenery_data.get(
            "items",
            [],
        )
        item_path = f"{scenery_path}.items"
        checkItemRefs(
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
                    ).append(item_path)

        for interaction_key in [
            "interactions",
            "throwInteractions",
        ]:
            interactions = scenery_data.get(
                interaction_key,
                {},
            )

            if not isinstance(interactions, dict):
                errors.append(f"{scenery_path}.{interaction_key} must be a dictionary.")
                continue

            for item_id, interaction in interactions.items():
                interaction_path = f"{scenery_path}.{interaction_key}[{item_id!r}]"

                if not isinstance(item_id, str) or item_id not in itemRegistry:
                    errors.append(
                        f"{interaction_path} references unknown item ID {item_id!r}."
                    )

                if not isinstance(interaction, dict):
                    errors.append(f"{interaction_path} must be a dictionary.")
                    continue

                if interaction_key == "interactions":
                    for response_key in [
                        "response",
                        "failResponse",
                    ]:
                        if response_key in interaction:
                            checkResponse(
                                interaction[response_key],
                                f"{interaction_path}.{response_key}",
                                errors,
                            )

                    if "requires" in interaction:
                        checkRequirements(
                            interaction["requires"],
                            f"{interaction_path}.requires",
                            errors,
                            ACTION_REQUIREMENT_KEYS,
                        )

                    if "effects" in interaction:
                        checkEffects(
                            interaction["effects"],
                            f"{interaction_path}.effects",
                            errors,
                        )
                else:
                    checkThrow(
                        interaction,
                        interaction_path,
                        errors,
                    )

        for requirement_key in [
            "openRequires",
            "closeRequires",
        ]:
            if requirement_key in scenery_data:
                checkRequirements(
                    scenery_data[requirement_key],
                    f"{scenery_path}.{requirement_key}",
                    errors,
                    ACTION_REQUIREMENT_KEYS,
                )


def checkExit(
    location_path,
    exits,
    scenery_ids,
    errors,
):
    if not isinstance(exits, dict):
        errors.append(f"{location_path}.exits must be a dictionary.")
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
            errors.append(f"{exit_path} uses an unsupported direction.")

        if exit_data is False or exit_data is None:
            continue

        if isinstance(exit_data, str):
            destination = exit_data
        elif isinstance(exit_data, dict):
            for key in exit_data:
                if key not in exit_keys:
                    errors.append(f"{exit_path} uses unsupported exit field {key!r}.")

            destination = exit_data.get(
                "location",
            )

            if "requires" in exit_data:
                checkRequirements(
                    exit_data["requires"],
                    f"{exit_path}.requires",
                    errors,
                    exit_requirement_keys,
                    scenery_ids,
                    True,
                )

            if "blockedResponse" in exit_data:
                checkResponse(
                    exit_data["blockedResponse"],
                    f"{exit_path}.blockedResponse",
                    errors,
                )
        else:
            errors.append(f"{exit_path} must be a location ID, dictionary, or False.")
            continue

        if not isinstance(destination, str) or destination not in locationRegistry:
            errors.append(
                f"{exit_path} references unknown location ID {destination!r}."
            )


def checkRoomExit(
    location_path,
    room_exits,
    errors,
):
    if not isinstance(room_exits, dict):
        errors.append(f"{location_path}.roomExits must be a dictionary.")
        return

    for room_name, destination in room_exits.items():
        room_exit_path = f"{location_path}.roomExits[{room_name!r}]"

        if not isinstance(room_name, str) or not room_name.strip():
            errors.append(f"{room_exit_path} must use a non-empty string room name.")

        if not isinstance(destination, str) or destination not in locationRegistry:
            errors.append(
                f"{room_exit_path} references unknown location ID " f"{destination!r}."
            )


def checkStateText(
    location_path,
    state_descriptions,
    scenery_ids,
    errors,
):
    if not isinstance(state_descriptions, list):
        errors.append(f"{location_path}.stateDescriptions must be a list.")
        return

    for index, state_description in enumerate(state_descriptions):
        state_path = f"{location_path}.stateDescriptions[{index}]"

        if not isinstance(state_description, dict):
            errors.append(f"{state_path} must be a dictionary.")
            continue

        description = state_description.get(
            "description",
        )

        if not isinstance(description, str) or not description.strip():
            errors.append(f"{state_path}.description must be a non-empty string.")

        checkRequirements(
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


def getErrors():
    errors = []
    initial_item_placements = {}

    checkDefSource(
        locationDefinitionsByArea,
        "Location",
        "locationDefinitionsByArea",
        errors,
    )

    for location_id, location_data in locationRegistry.items():
        location_path = f"locationRegistry[{location_id!r}]"

        if not isinstance(location_id, str) or not location_id:
            errors.append(f"{location_path} must use a non-empty string ID.")

        if not isinstance(location_data, dict):
            errors.append(f"{location_path} must be a dictionary.")
            continue

        for text_key in [
            "name",
            "description",
        ]:
            text = location_data.get(
                text_key,
            )

            if not isinstance(text, str) or not text.strip():
                errors.append(f"{location_path}.{text_key} must be a non-empty string.")

        if "intro" in location_data:
            checkIntroResponse(
                location_data["intro"],
                f"{location_path}.intro",
                errors,
            )

        if "searchVoice" in location_data:
            checkResponse(
                location_data["searchVoice"],
                f"{location_path}.searchVoice",
                errors,
            )

        location_items = location_data.get(
            "items",
            [],
        )
        item_path = f"{location_path}.items"
        checkItemRefs(
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
                    ).append(item_path)

        scenery = location_data.get(
            "scenery",
            {},
        )

        if not isinstance(scenery, dict):
            errors.append(f"{location_path}.scenery must be a dictionary.")
            scenery = {}

        scenery_ids = set(
            scenery,
        )

        initially_placed_item_ids = {
            item_id
            for item_id in (location_items if isinstance(location_items, list) else [])
            if isinstance(item_id, str)
        }

        for scenery_data in scenery.values():
            if isinstance(scenery_data, dict) and isinstance(
                scenery_data.get("items", []),
                list,
            ):
                initially_placed_item_ids.update(
                    item_id
                    for item_id in scenery_data.get(
                        "items",
                        [],
                    )
                    if isinstance(item_id, str)
                )

        item_contents = location_data.get(
            "itemContents",
            {},
        )

        if not isinstance(item_contents, dict):
            errors.append(f"{location_path}.itemContents must be a dictionary.")
        else:
            for container_item_id, contained_item_ids in item_contents.items():
                contents_path = f"{location_path}.itemContents[{container_item_id!r}]"
                container_item = itemRegistry.get(
                    container_item_id,
                )

                if not container_item or not container_item.get(
                    "container",
                    False,
                ):
                    errors.append(
                        f"{contents_path} must reference a registered container item."
                    )

                if container_item_id not in initially_placed_item_ids:
                    errors.append(
                        f"{contents_path} requires its container to be initially placed "
                        "in the same location."
                    )

                if (
                    container_item
                    and container_item.get("transferContentsOnTake", False)
                    and container_item_id
                    not in (location_items if isinstance(location_items, list) else [])
                ):
                    errors.append(
                        f"{contents_path} requires transfer-on-TAKE containers to be "
                        "top-level location items."
                    )

                checkItemRefs(
                    contained_item_ids,
                    contents_path,
                    errors,
                )

                if isinstance(contained_item_ids, list):
                    if all(
                        isinstance(item_id, str) for item_id in contained_item_ids
                    ) and len(contained_item_ids) != len(set(contained_item_ids)):
                        errors.append(f"{contents_path} contains duplicate item IDs.")

                    for item_id in contained_item_ids:
                        if item_id == container_item_id:
                            errors.append(f"{contents_path} cannot contain itself.")

                        contained_item = itemRegistry.get(
                            item_id,
                            {},
                        )

                        if contained_item.get(
                            "container",
                            False,
                        ):
                            errors.append(
                                f"{contents_path} cannot contain another world-item container."
                            )

                        if contained_item and not contained_item.get(
                            "takeable",
                            False,
                        ):
                            errors.append(
                                f"{contents_path} may contain only takeable normal items."
                            )

                        if isinstance(item_id, str) and item_id in itemRegistry:
                            initial_item_placements.setdefault(
                                item_id,
                                [],
                            ).append(contents_path)

        checkScenery(
            location_path,
            scenery,
            errors,
            initial_item_placements,
        )
        checkExit(
            location_path,
            location_data.get(
                "exits",
            ),
            scenery_ids,
            errors,
        )
        if "roomExits" in location_data:
            checkRoomExit(
                location_path,
                location_data["roomExits"],
                errors,
            )
        checkStateText(
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
            errors.append(f"{location_path}.interactions must be a dictionary.")
        else:
            for scenery_id, interaction in location_interactions.items():
                interaction_path = f"{location_path}.interactions[{scenery_id!r}]"

                if scenery_id not in scenery_ids:
                    errors.append(
                        f"{interaction_path} references unknown scenery ID "
                        f"{scenery_id!r}."
                    )

                if not isinstance(interaction, dict):
                    errors.append(f"{interaction_path} must be a dictionary.")
                    continue

                interaction_type = interaction.get(
                    "type",
                )

                if interaction_type != "combination":
                    errors.append(f"{interaction_path}.type must be 'combination'.")
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
                        checkResponse(
                            interaction.get(
                                response_key,
                            ),
                            f"{interaction_path}.{response_key}",
                            errors,
                        )

                    effects = interaction.get(
                        "effects",
                    )

                    checkEffects(
                        effects,
                        f"{interaction_path}.effects",
                        errors,
                        COMBINATION_EFFECT_KEYS,
                    )

                    if isinstance(effects, dict):
                        scenery_effects = effects.get(
                            "sceneryState",
                        )

                        if not isinstance(scenery_effects, dict) or not scenery_effects:
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
