from game.itemAccess import (
    visibleItemIds,
    resolveItem,
)
from game.itemDisplay import displayName
from game.responses import commandFailure
from game.worldState import (
    applyChanges,
    currentLocation,
    getItemStateSnapshot,
    getSceneryState,
    stateMatches,
)
from items.registry import itemRegistry
from states.game import WORLD_ITEM_PLACEMENT


def resolveProvider(
    use_name,
    inventory,
):
    matches = []

    for provider_item_id in inventory:
        provider_item = itemRegistry[provider_item_id]

        for use_id, provided_use in provider_item.get(
            "providedUses",
            {},
        ).items():
            aliases = provided_use.get(
                "aliases",
                [],
            )

            if use_name == use_id or use_name in aliases:
                matches.append(
                    (
                        provider_item_id,
                        use_id,
                        provided_use,
                    )
                )

    if not matches:
        return None, None, None, None

    if len(matches) > 1:
        provider_names = [
            displayName(
                itemRegistry[provider_item_id],
            )
            for provider_item_id, _, _ in matches
        ]

        if len(provider_names) == 2:
            choices = " or ".join(
                provider_names,
            )
        else:
            choices = ", ".join(provider_names[:-1]) + f", or {provider_names[-1]}"

        return (
            None,
            None,
            None,
            f"Which {use_name} source do you mean: {choices}?",
        )

    provider_item_id, use_id, provided_use = matches[0]

    return provider_item_id, use_id, provided_use, None


def minimumsMet(
    current_state,
    minimums,
):
    for key, minimum in minimums.items():
        current_value = current_state.get(
            key,
        )

        if type(current_value) is not int or current_value < minimum:
            return False

    return True


def previewChanges(
    current_state,
    updates=None,
    deltas=None,
):
    final_state = dict(
        current_state,
    )
    final_state.update(
        updates or {},
    )

    for key, delta in (deltas or {}).items():
        current_value = final_state.get(
            key,
        )

        if type(current_value) is not int:
            return None

        final_value = current_value + delta

        if final_value < 0:
            return None

        final_state[key] = final_value

    return final_state


def requirementsMet(
    requirements,
    game_state,
):
    player_state = game_state["player"]

    for item_id in requirements.get(
        "inventory",
        [],
    ):
        if item_id not in player_state["inventory"]:
            return False

    for item_id in requirements.get(
        "equipped",
        [],
    ):
        if item_id not in player_state["equipped"]:
            return False

    return stateMatches(
        game_state["flags"],
        requirements.get(
            "flags",
            {},
        ),
    )


def targetOwner(
    target_item_id,
    game_state,
):
    player_state = game_state["player"]

    if target_item_id in player_state["inventory"]:
        return "inventory", None

    if target_item_id in player_state["equipped"]:
        return "equipped", None

    location_state = currentLocation(
        game_state,
    )

    if target_item_id in location_state["items"]:
        return "currentLocation", location_state["items"][target_item_id]

    return None, None


def removeOwnedItem(
    item_id,
    ownership,
    game_state,
):
    if ownership == "inventory":
        game_state["player"]["inventory"].remove(
            item_id,
        )
        return

    if ownership == "equipped":
        game_state["player"]["equipped"].remove(
            item_id,
        )
        return

    currentLocation(
        game_state,
    )["items"].pop(
        item_id,
        None,
    )


def useItem(
    source_key,
    source_item_id,
    source_state_item_id,
    source_state,
    provider_use,
    target_name,
    location_definition,
    game_state,
):
    target_candidates = (
        visibleItemIds(
            location_definition,
            game_state,
        )
        + game_state["player"]["inventory"]
        + game_state["player"]["equipped"]
    )
    target_item_id, clarification = resolveItem(
        target_name,
        target_candidates,
    )

    if clarification:
        return commandFailure(
            clarification,
        )

    if not target_item_id:
        return commandFailure(
            f"I don't see a {target_name} here.",
        )

    target_item = itemRegistry[target_item_id]
    interaction = target_item.get(
        "interactions",
        {},
    ).get(
        source_key,
    )

    if not interaction:
        return commandFailure(
            f"You can't use that on the {displayName(target_item)} here.",
        )

    if provider_use:
        target_definition_requirements = provider_use.get(
            "targetDefinitionRequires",
            {},
        )
    else:
        target_definition_requirements = itemRegistry[source_item_id].get(
            "targetDefinitionRequires",
            {},
        )

    if not stateMatches(
        target_item,
        target_definition_requirements,
    ):
        return commandFailure(
            interaction.get(
                "targetDefinitionFailResponse",
                interaction.get(
                    "failResponse",
                    "That item cannot be affected that way.",
                ),
            )
        )

    requirements = interaction.get(
        "requires",
        {},
    )
    fail_response = interaction.get(
        "failResponse",
        "That won't work right now.",
    )

    if not stateMatches(
        source_state,
        requirements.get(
            "sourceItemState",
            {},
        ),
    ) or not minimumsMet(
        source_state,
        requirements.get(
            "sourceItemStateMinimums",
            {},
        ),
    ):
        return commandFailure(
            interaction.get(
                "sourceStateFailResponse",
                fail_response,
            )
        )

    target_state = getItemStateSnapshot(
        game_state,
        target_item_id,
    )

    if not stateMatches(
        target_state,
        requirements.get(
            "targetItemState",
            {},
        ),
    ) or not minimumsMet(
        target_state,
        requirements.get(
            "targetItemStateMinimums",
            {},
        ),
    ):
        return commandFailure(
            interaction.get(
                "targetStateFailResponse",
                fail_response,
            )
        )

    target_ownership, target_placement = targetOwner(
        target_item_id,
        game_state,
    )
    required_ownership = requirements.get(
        "targetOwnership",
    )

    if required_ownership and target_ownership != required_ownership:
        return commandFailure(
            interaction.get(
                "targetLocationFailResponse",
                fail_response,
            )
        )

    if requirements.get("targetPlacement") == "loose" and (
        target_ownership != "currentLocation"
        or target_placement not in {WORLD_ITEM_PLACEMENT, None}
    ):
        return commandFailure(
            interaction.get(
                "targetLocationFailResponse",
                fail_response,
            )
        )

    if not requirementsMet(
        requirements,
        game_state,
    ):
        return commandFailure(
            fail_response,
        )

    effects = interaction.get(
        "effects",
        {},
    )
    source_deltas = dict(
        effects.get(
            "sourceItemStateDeltas",
            {},
        )
    )

    if provider_use:
        resource = provider_use["resource"]
        resource_state_key = resource["stateKey"]
        source_deltas[resource_state_key] = (
            source_deltas.get(resource_state_key, 0) - resource["consume"]
        )

    final_source_state = previewChanges(
        source_state,
        effects.get(
            "sourceItemState",
        ),
        source_deltas,
    )
    final_target_state = previewChanges(
        target_state,
        effects.get(
            "targetItemState",
        ),
        effects.get(
            "targetItemStateDeltas",
        ),
    )

    if final_source_state is None or final_target_state is None:
        return commandFailure(
            fail_response,
        )

    # Commit only after every source, target, and effect check succeeds.
    game_state["itemStates"][source_state_item_id] = final_source_state

    if (
        target_item_id in game_state["itemStates"]
        or effects.get("targetItemState")
        or effects.get("targetItemStateDeltas")
    ):
        game_state["itemStates"][target_item_id] = final_target_state
    applyChanges(
        game_state["flags"],
        effects.get(
            "flags",
        ),
    )

    if (
        effects.get(
            "destroySource",
            False,
        )
        and source_item_id
    ):
        removeOwnedItem(
            source_item_id,
            "inventory",
            game_state,
        )

    if effects.get(
        "destroyTarget",
        False,
    ):
        removeOwnedItem(
            target_item_id,
            target_ownership,
            game_state,
        )

    return interaction.get(
        "response",
        f"You use it on the {displayName(target_item)}.",
    )


def useScenery(
    source_key,
    source_item_id,
    source_state_item_id,
    source_state,
    provider_use,
    scenery_id,
    scenery_data,
    game_state,
):
    interaction = scenery_data.get(
        "interactions",
        {},
    ).get(
        source_key,
    )

    if not interaction:
        return commandFailure(
            f"You can't use that on {scenery_id} here.",
        )

    location_state = currentLocation(
        game_state,
    )
    scenery_state = getSceneryState(
        location_state,
        scenery_id,
    )
    requirements = interaction.get(
        "requires",
        {},
    )
    fail_response = interaction.get(
        "failResponse",
        "That won't work right now.",
    )

    if (
        not stateMatches(
            source_state,
            requirements.get(
                "itemState",
                {},
            ),
        )
        or not stateMatches(
            scenery_state,
            requirements.get(
                "sceneryState",
                {},
            ),
        )
        or not requirementsMet(
            requirements,
            game_state,
        )
    ):
        return commandFailure(
            fail_response,
        )

    effects = interaction.get(
        "effects",
        {},
    )
    source_deltas = {}

    if provider_use:
        resource = provider_use["resource"]
        source_deltas[resource["stateKey"]] = -resource["consume"]

    final_source_state = previewChanges(
        source_state,
        effects.get(
            "itemState",
        ),
        source_deltas,
    )

    if final_source_state is None:
        return commandFailure(
            fail_response,
        )

    game_state["itemStates"][source_state_item_id] = final_source_state
    applyChanges(
        scenery_state,
        effects.get(
            "sceneryState",
        ),
    )
    applyChanges(
        game_state["flags"],
        effects.get(
            "flags",
        ),
    )

    if (
        effects.get(
            "destroyItem",
            False,
        )
        and source_item_id
    ):
        game_state["player"]["inventory"].remove(
            source_item_id,
        )

    return interaction.get(
        "response",
        f"You use it on the {scenery_id}.",
    )
