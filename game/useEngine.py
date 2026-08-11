from game.itemAccess import (
    get_visible_item_ids,
    resolve_item,
)
from game.itemPresentation import get_item_display_name
from game.responses import command_failure
from game.worldState import (
    apply_state_changes,
    get_current_location_state,
    get_item_state_snapshot,
    get_scenery_state,
    state_matches,
)
from items.itemRegistry import itemRegistry
from states.gameState import WORLD_ITEM_PLACEMENT


def resolve_provided_use(
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
            get_item_display_name(
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


def state_minimums_met(
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


def build_changed_state(
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


def common_requirements_met(
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

    return state_matches(
        game_state["flags"],
        requirements.get(
            "flags",
            {},
        ),
    )


def get_target_ownership(
    target_item_id,
    game_state,
):
    player_state = game_state["player"]

    if target_item_id in player_state["inventory"]:
        return "inventory", None

    if target_item_id in player_state["equipped"]:
        return "equipped", None

    location_state = get_current_location_state(
        game_state,
    )

    if target_item_id in location_state["items"]:
        return "currentLocation", location_state["items"][target_item_id]

    return None, None


def remove_item_from_owner(
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

    get_current_location_state(
        game_state,
    )["items"].pop(
        item_id,
        None,
    )


def handle_item_interaction(
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
        get_visible_item_ids(
            location_definition,
            game_state,
        )
        + game_state["player"]["inventory"]
        + game_state["player"]["equipped"]
    )
    target_item_id, clarification = resolve_item(
        target_name,
        target_candidates,
    )

    if clarification:
        return command_failure(
            clarification,
        )

    if not target_item_id:
        return command_failure(
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
        return command_failure(
            f"You can't use that on the {get_item_display_name(target_item)} here.",
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

    if not state_matches(
        target_item,
        target_definition_requirements,
    ):
        return command_failure(
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

    if not state_matches(
        source_state,
        requirements.get(
            "sourceItemState",
            {},
        ),
    ) or not state_minimums_met(
        source_state,
        requirements.get(
            "sourceItemStateMinimums",
            {},
        ),
    ):
        return command_failure(
            interaction.get(
                "sourceStateFailResponse",
                fail_response,
            )
        )

    target_state = get_item_state_snapshot(
        game_state,
        target_item_id,
    )

    if not state_matches(
        target_state,
        requirements.get(
            "targetItemState",
            {},
        ),
    ) or not state_minimums_met(
        target_state,
        requirements.get(
            "targetItemStateMinimums",
            {},
        ),
    ):
        return command_failure(
            interaction.get(
                "targetStateFailResponse",
                fail_response,
            )
        )

    target_ownership, target_placement = get_target_ownership(
        target_item_id,
        game_state,
    )
    required_ownership = requirements.get(
        "targetOwnership",
    )

    if required_ownership and target_ownership != required_ownership:
        return command_failure(
            interaction.get(
                "targetLocationFailResponse",
                fail_response,
            )
        )

    if requirements.get("targetPlacement") == "loose" and (
        target_ownership != "currentLocation"
        or target_placement not in {WORLD_ITEM_PLACEMENT, None}
    ):
        return command_failure(
            interaction.get(
                "targetLocationFailResponse",
                fail_response,
            )
        )

    if not common_requirements_met(
        requirements,
        game_state,
    ):
        return command_failure(
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

    final_source_state = build_changed_state(
        source_state,
        effects.get(
            "sourceItemState",
        ),
        source_deltas,
    )
    final_target_state = build_changed_state(
        target_state,
        effects.get(
            "targetItemState",
        ),
        effects.get(
            "targetItemStateDeltas",
        ),
    )

    if final_source_state is None or final_target_state is None:
        return command_failure(
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
    apply_state_changes(
        game_state["flags"],
        effects.get(
            "flags",
        ),
    )

    if effects.get(
        "destroySource",
        False,
    ) and source_item_id:
        remove_item_from_owner(
            source_item_id,
            "inventory",
            game_state,
        )

    if effects.get(
        "destroyTarget",
        False,
    ):
        remove_item_from_owner(
            target_item_id,
            target_ownership,
            game_state,
        )

    return interaction.get(
        "response",
        f"You use it on the {get_item_display_name(target_item)}.",
    )


def handle_scenery_interaction(
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
        return command_failure(
            f"You can't use that on {scenery_id} here.",
        )

    location_state = get_current_location_state(
        game_state,
    )
    scenery_state = get_scenery_state(
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

    if not state_matches(
        source_state,
        requirements.get(
            "itemState",
            {},
        ),
    ) or not state_matches(
        scenery_state,
        requirements.get(
            "sceneryState",
            {},
        ),
    ) or not common_requirements_met(
        requirements,
        game_state,
    ):
        return command_failure(
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

    final_source_state = build_changed_state(
        source_state,
        effects.get(
            "itemState",
        ),
        source_deltas,
    )

    if final_source_state is None:
        return command_failure(
            fail_response,
        )

    game_state["itemStates"][source_state_item_id] = final_source_state
    apply_state_changes(
        scenery_state,
        effects.get(
            "sceneryState",
        ),
    )
    apply_state_changes(
        game_state["flags"],
        effects.get(
            "flags",
        ),
    )

    if effects.get(
        "destroyItem",
        False,
    ) and source_item_id:
        game_state["player"]["inventory"].remove(
            source_item_id,
        )

    return interaction.get(
        "response",
        f"You use it on the {scenery_id}.",
    )
