from game.validators.common import (
    checkDefSource,
    checkIntegerMap,
    checkLocalStateText,
    checkRequirements,
    checkResponse,
    checkThrow,
)
from items.registry import (
    itemDefinitionsByArea,
    itemRegistry,
)
from states.game import EQUIPMENT_SLOTS

ITEM_INTERACTION_REQUIREMENT_KEYS = {
    "sourceItemState",
    "sourceItemStateMinimums",
    "targetItemState",
    "targetItemStateMinimums",
    "targetOwnership",
    "targetPlacement",
    "inventory",
    "equipped",
    "flags",
}


ITEM_INTERACTION_EFFECT_KEYS = {
    "sourceItemState",
    "sourceItemStateDeltas",
    "targetItemState",
    "targetItemStateDeltas",
    "flags",
    "destroySource",
    "destroyTarget",
}


ITEM_RESPONSE_KEYS = {
    "inspect",
    "takeFail",
    "takeResponse",
    "takeWearResponse",
    "mergeResponse",
    "dropResponse",
    "wearFailResponse",
    "alreadyWearingResponse",
    "wearResponse",
    "removeResponse",
    "searchResponse",
    "searchClosedResponse",
    "searchBlockedResponse",
    "searchEmptyResponse",
    "openFailResponse",
    "lockedResponse",
    "alreadyOpenResponse",
    "openBlockedResponse",
    "openResponse",
    "closeFailResponse",
    "alreadyClosedResponse",
    "closeBlockedResponse",
    "closeResponse",
    "takeBlockedResponse",
}


def getErrors():
    errors = []
    merge_group_state_keys = {}

    checkDefSource(
        itemDefinitionsByArea,
        "Item",
        "itemDefinitionsByArea",
        errors,
    )

    provided_use_ids = set()

    for item_data in itemRegistry.values():
        if not isinstance(item_data, dict):
            continue

        provided_uses = item_data.get(
            "providedUses",
            {},
        )

        if not isinstance(provided_uses, dict):
            continue

        provided_use_ids.update(
            use_id for use_id in provided_uses if isinstance(use_id, str) and use_id
        )

    for item_id, item_data in itemRegistry.items():
        item_path = f"itemRegistry[{item_id!r}]"

        if not isinstance(item_id, str) or not item_id:
            errors.append(f"{item_path} must use a non-empty string ID.")

        if not isinstance(item_data, dict):
            errors.append(f"{item_path} must be a dictionary.")
            continue

        name = item_data.get(
            "name",
        )

        if not isinstance(name, str) or not name.strip():
            errors.append(f"{item_path}.name must be a non-empty string.")

        if "interchangeableGroup" in item_data:
            interchangeable_group = item_data["interchangeableGroup"]

            if (
                not isinstance(interchangeable_group, str)
                or not interchangeable_group.strip()
            ):
                errors.append(
                    f"{item_path}.interchangeableGroup must be a non-empty string."
                )

        aliases = item_data.get(
            "aliases",
        )

        if not isinstance(aliases, list) or not aliases:
            errors.append(f"{item_path}.aliases must be a non-empty list.")
        else:
            for alias in aliases:
                if not isinstance(alias, str) or not alias.strip():
                    errors.append(f"{item_path}.aliases contains an invalid alias.")
                elif alias != alias.lower():
                    errors.append(
                        f"{item_path}.aliases must use lowercase text: {alias!r}."
                    )

            if all(isinstance(alias, str) for alias in aliases) and len(aliases) != len(
                set(aliases)
            ):
                errors.append(f"{item_path}.aliases contains duplicate aliases.")

        for boolean_key in [
            "takeable",
            "wearable",
            "container",
            "searchable",
            "openable",
            "closeable",
            "contentsRequireSearch",
            "transferContentsOnTake",
            "flammable",
        ]:
            if boolean_key in item_data and not isinstance(
                item_data[boolean_key],
                bool,
            ):
                errors.append(f"{item_path}.{boolean_key} must be a boolean.")

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

            if type(carry_capacity) is not int or carry_capacity <= 0:
                errors.append(f"{item_path}.carryCapacity must be a positive integer.")

            if not item_data.get("wearable", False) or item_data.get("slot") != "back":
                errors.append(
                    f"{item_path}.carryCapacity requires a wearable back-slot item."
                )

        if item_data.get("transferContentsOnTake", False) and not item_data.get(
            "container",
            False,
        ):
            errors.append(
                f"{item_path}.transferContentsOnTake requires container=True."
            )

        if item_data.get("contentsRequireSearch", False) and not item_data.get(
            "searchable",
            False,
        ):
            errors.append(
                f"{item_path}.contentsRequireSearch requires searchable=True."
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
                errors.append(f"{item_path}.{text_key} must be a non-empty string.")

        for response_key in ITEM_RESPONSE_KEYS.intersection(item_data):
            checkResponse(
                item_data[response_key],
                f"{item_path}.{response_key}",
                errors,
            )

        if "state" in item_data and not isinstance(
            item_data["state"],
            dict,
        ):
            errors.append(f"{item_path}.state must be a dictionary.")

        merge_config = item_data.get(
            "mergeOnTake",
        )

        if "mergeOnTake" in item_data:
            merge_path = f"{item_path}.mergeOnTake"

            if not isinstance(merge_config, dict):
                errors.append(f"{merge_path} must be a dictionary.")
            else:
                if set(merge_config) != {
                    "group",
                    "stateKey",
                }:
                    errors.append(
                        f"{merge_path} must contain exactly group and stateKey."
                    )

                group = merge_config.get(
                    "group",
                )
                state_key = merge_config.get(
                    "stateKey",
                )

                if not isinstance(group, str) or not group.strip():
                    errors.append(f"{merge_path}.group must be a non-empty string.")

                if not isinstance(state_key, str) or not state_key.strip():
                    errors.append(
                        f"{merge_path}.stateKey must be a non-empty string."
                    )
                else:
                    initial_state = item_data.get(
                        "state",
                        {},
                    )

                    if not isinstance(initial_state, dict):
                        initial_state = {}

                    quantity = initial_state.get(
                        state_key,
                    )

                    if type(quantity) is not int or quantity < 0:
                        errors.append(
                            f"{merge_path}.stateKey must reference a non-negative "
                            "integer in the item state."
                        )

                if isinstance(group, str) and group.strip() and isinstance(
                    state_key,
                    str,
                ) and state_key.strip():
                    existing_state_key = merge_group_state_keys.setdefault(
                        group,
                        state_key,
                    )

                    if existing_state_key != state_key:
                        errors.append(
                            f"{merge_path}.stateKey must match the other items in "
                            f"merge group {group!r}."
                        )

            if not item_data.get(
                "takeable",
                False,
            ):
                errors.append(f"{merge_path} requires takeable=True.")

            if item_data.get(
                "transferContentsOnTake",
                False,
            ):
                errors.append(
                    f"{merge_path} cannot be used with transferContentsOnTake."
                )

        if "mergeResponse" in item_data and "mergeOnTake" not in item_data:
            errors.append(f"{item_path}.mergeResponse requires mergeOnTake.")

        if "stateDescriptions" in item_data:
            checkLocalStateText(
                item_data["stateDescriptions"],
                f"{item_path}.stateDescriptions",
                errors,
            )

        provided_uses = item_data.get(
            "providedUses",
            {},
        )

        if not isinstance(provided_uses, dict):
            errors.append(f"{item_path}.providedUses must be a dictionary.")
        else:
            for use_id, provided_use in provided_uses.items():
                use_path = f"{item_path}.providedUses[{use_id!r}]"

                if not isinstance(use_id, str) or not use_id:
                    errors.append(f"{use_path} must use a non-empty string ID.")

                if not isinstance(provided_use, dict):
                    errors.append(f"{use_path} must be a dictionary.")
                    continue

                aliases = provided_use.get(
                    "aliases",
                )

                if (
                    not isinstance(aliases, list)
                    or not aliases
                    or not all(
                        isinstance(alias, str)
                        and alias.strip()
                        and alias == alias.lower()
                        for alias in aliases
                    )
                ):
                    errors.append(
                        f"{use_path}.aliases must be a non-empty list of lowercase strings."
                    )

                requires_state = provided_use.get(
                    "requiresState",
                    {},
                )

                if not isinstance(requires_state, dict):
                    errors.append(f"{use_path}.requiresState must be a dictionary.")

                resource = provided_use.get(
                    "resource",
                )

                if not isinstance(resource, dict) or set(resource) != {
                    "stateKey",
                    "minimum",
                    "consume",
                }:
                    errors.append(
                        f"{use_path}.resource must contain stateKey, minimum, and consume."
                    )
                else:
                    state_key = resource["stateKey"]
                    initial_state = item_data.get(
                        "state",
                        {},
                    )

                    if not isinstance(initial_state, dict):
                        initial_state = {}

                    if (
                        not isinstance(state_key, str)
                        or not state_key
                        or type(initial_state.get(state_key)) is not int
                        or initial_state[state_key] < 0
                    ):
                        errors.append(
                            f"{use_path}.resource.stateKey must reference a non-negative "
                            "integer in the item state."
                        )

                    for resource_key in [
                        "minimum",
                        "consume",
                    ]:
                        if (
                            type(resource[resource_key]) is not int
                            or resource[resource_key] <= 0
                        ):
                            errors.append(
                                f"{use_path}.resource.{resource_key} must be a positive integer."
                            )

                checkResponse(
                    provided_use.get(
                        "failResponse",
                    ),
                    f"{use_path}.failResponse",
                    errors,
                )

                if "targetDefinitionRequires" in provided_use and not isinstance(
                    provided_use["targetDefinitionRequires"],
                    dict,
                ):
                    errors.append(
                        f"{use_path}.targetDefinitionRequires must be a dictionary."
                    )

        if "targetDefinitionRequires" in item_data and not isinstance(
            item_data["targetDefinitionRequires"],
            dict,
        ):
            errors.append(f"{item_path}.targetDefinitionRequires must be a dictionary.")

        quantity_display = item_data.get(
            "quantityDisplay",
        )

        if quantity_display is not None:
            quantity_path = f"{item_path}.quantityDisplay"

            if not isinstance(quantity_display, dict):
                errors.append(f"{quantity_path} must be a dictionary.")
            else:
                state_key = quantity_display.get(
                    "stateKey",
                )
                initial_state = item_data.get(
                    "state",
                    {},
                )

                if not isinstance(initial_state, dict):
                    initial_state = {}

                if (
                    not isinstance(state_key, str)
                    or type(initial_state.get(state_key)) is not int
                    or initial_state[state_key] < 0
                ):
                    errors.append(
                        f"{quantity_path}.stateKey must reference a non-negative integer "
                        "in the item state."
                    )

                for label_key in [
                    "singular",
                    "plural",
                ]:
                    label = quantity_display.get(
                        label_key,
                    )

                    if not isinstance(label, str) or not label.strip():
                        errors.append(
                            f"{quantity_path}.{label_key} must be a non-empty string."
                        )

                if "requiresState" in quantity_display and not isinstance(
                    quantity_display["requiresState"],
                    dict,
                ):
                    errors.append(
                        f"{quantity_path}.requiresState must be a dictionary."
                    )

                if "showInInventory" in quantity_display and not isinstance(
                    quantity_display["showInInventory"],
                    bool,
                ):
                    errors.append(
                        f"{quantity_path}.showInInventory must be a boolean."
                    )

        item_interactions = item_data.get(
            "interactions",
            {},
        )

        if not isinstance(item_interactions, dict):
            errors.append(f"{item_path}.interactions must be a dictionary.")
        else:
            for source_id, interaction in item_interactions.items():
                interaction_path = f"{item_path}.interactions[{source_id!r}]"

                if source_id not in itemRegistry and source_id not in provided_use_ids:
                    errors.append(
                        f"{interaction_path} references unknown item or provided-use ID "
                        f"{source_id!r}."
                    )

                checkInteraction(
                    interaction,
                    interaction_path,
                    errors,
                )

        if "onThrow" in item_data:
            throw_actions = item_data["onThrow"]

            if not isinstance(throw_actions, dict):
                errors.append(f"{item_path}.onThrow must be a dictionary.")
            else:
                for action_id, throw_action in throw_actions.items():
                    action_path = f"{item_path}.onThrow[{action_id!r}]"

                    if not isinstance(action_id, str) or not action_id:
                        errors.append(f"{action_path} must use a non-empty string ID.")

                    if action_id != "default":
                        errors.append(
                            f"{action_path} uses unsupported action "
                            f"{action_id!r}; item onThrow only supports 'default'."
                        )

                    checkThrow(
                        throw_action,
                        action_path,
                        errors,
                    )

    return errors


def checkInteraction(
    interaction,
    definition_path,
    errors,
):
    if not isinstance(interaction, dict):
        errors.append(f"{definition_path} must be a dictionary.")
        return

    for response_key in [
        "response",
        "failResponse",
        "sourceStateFailResponse",
        "targetStateFailResponse",
        "targetLocationFailResponse",
        "targetDefinitionFailResponse",
    ]:
        if response_key in interaction:
            checkResponse(
                interaction[response_key],
                f"{definition_path}.{response_key}",
                errors,
            )

    requirements = interaction.get(
        "requires",
        {},
    )
    checkRequirements(
        requirements,
        f"{definition_path}.requires",
        errors,
        ITEM_INTERACTION_REQUIREMENT_KEYS,
    )

    if isinstance(requirements, dict):
        for state_key in [
            "sourceItemState",
            "targetItemState",
        ]:
            if state_key in requirements and not isinstance(
                requirements[state_key],
                dict,
            ):
                errors.append(
                    f"{definition_path}.requires.{state_key} must be a dictionary."
                )

        for minimum_key in [
            "sourceItemStateMinimums",
            "targetItemStateMinimums",
        ]:
            if minimum_key in requirements:
                checkIntegerMap(
                    requirements[minimum_key],
                    f"{definition_path}.requires.{minimum_key}",
                    errors,
                    require_positive=True,
                )

        if "targetOwnership" in requirements:
            target_ownership = requirements["targetOwnership"]

            if not isinstance(target_ownership, str) or target_ownership not in {
                "inventory",
                "equipped",
                "currentLocation",
            }:
                errors.append(
                    f"{definition_path}.requires.targetOwnership must be inventory, "
                    "equipped, or currentLocation."
                )

        if (
            "targetPlacement" in requirements
            and requirements["targetPlacement"] != "loose"
        ):
            errors.append(
                f"{definition_path}.requires.targetPlacement must be 'loose'."
            )

    effects = interaction.get(
        "effects",
        {},
    )

    if not isinstance(effects, dict):
        errors.append(f"{definition_path}.effects must be a dictionary.")
        return

    for key in effects:
        if key not in ITEM_INTERACTION_EFFECT_KEYS:
            errors.append(f"{definition_path}.effects uses unsupported effect {key!r}.")

    for state_key in [
        "sourceItemState",
        "targetItemState",
        "flags",
    ]:
        if state_key in effects and not isinstance(
            effects[state_key],
            dict,
        ):
            errors.append(
                f"{definition_path}.effects.{state_key} must be a dictionary."
            )

    for delta_key in [
        "sourceItemStateDeltas",
        "targetItemStateDeltas",
    ]:
        if delta_key in effects:
            checkIntegerMap(
                effects[delta_key],
                f"{definition_path}.effects.{delta_key}",
                errors,
            )

    for boolean_key in [
        "destroySource",
        "destroyTarget",
    ]:
        if boolean_key in effects and not isinstance(
            effects[boolean_key],
            bool,
        ):
            errors.append(f"{definition_path}.effects.{boolean_key} must be a boolean.")
