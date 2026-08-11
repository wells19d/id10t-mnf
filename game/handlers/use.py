from game.itemAccess import (
    find_scenery,
    get_visible_item_ids,
    resolve_item,
)
from game.itemPresentation import get_item_display_name
from game.responses import command_failure
from game.useEngine import (
    build_changed_state,
    common_requirements_met,
    get_target_ownership,
    handle_item_interaction,
    handle_scenery_interaction,
    remove_item_from_owner,
    resolve_provided_use,
    state_minimums_met,
)
from game.worldState import (
    apply_state_changes,
    get_current_location_state,
    get_item_state_snapshot,
    get_scenery_state,
    state_matches,
)
from items.itemRegistry import itemRegistry
from states.gameState import WORLD_ITEM_PLACEMENT


def handle_use(command, location_definition, game_state):
    values = command["values"]
    target = command["target"]

    # Numeric interactions such as safe combinations.
    if values and target:
        scenery_id, scenery_data = find_scenery(
            target,
            location_definition,
        )

        if not scenery_data:
            return command_failure(
                f"I don't see a {target} here.",
            )

        location_interaction = location_definition.get(
            "interactions",
            {},
        ).get(
            scenery_id,
        )

        if (
            location_interaction
            and location_interaction.get("type") == "combination"
        ):
            correct_combination = location_interaction.get(
                "combination",
                [],
            )

            if values == correct_combination:
                location_state = get_current_location_state(
                    game_state,
                )
                scenery_state = get_scenery_state(
                    location_state,
                    scenery_id,
                )
                effects = location_interaction.get(
                    "effects",
                    {},
                )
                apply_state_changes(
                    scenery_state,
                    effects["sceneryState"],
                )

                return location_interaction["onSuccess"]

            return command_failure(
                location_interaction["onFail"],
            )

    item_name = command["object"]

    if not item_name:
        return command_failure(
            "I don't know what I want to use.",
        )

    inventory = game_state["player"]["inventory"]
    source_item_id, clarification = resolve_item(
        item_name,
        inventory,
    )
    provider_use = None

    if clarification:
        return command_failure(
            clarification,
        )

    if source_item_id:
        source_key = source_item_id
        source_state_item_id = source_item_id
        source_state = get_item_state_snapshot(
            game_state,
            source_item_id,
        )
        source_name = get_item_display_name(
            itemRegistry[source_item_id],
        )
    else:
        provider_item_id, source_key, provider_use, clarification = resolve_provided_use(
            item_name,
            inventory,
        )

        if clarification:
            return command_failure(
                clarification,
            )

        if not provider_item_id:
            return command_failure(
                f"You aren't carrying {item_name} or anything that provides it.",
            )

        source_item_id = None
        source_state_item_id = provider_item_id
        source_state = get_item_state_snapshot(
            game_state,
            provider_item_id,
        )
        source_name = item_name

        if not state_matches(
            source_state,
            provider_use.get(
                "requiresState",
                {},
            ),
        ):
            return command_failure(
                provider_use["failResponse"],
            )

        resource = provider_use["resource"]

        if not state_minimums_met(
            source_state,
            {
                resource["stateKey"]: resource["minimum"],
            },
        ):
            return command_failure(
                provider_use["failResponse"],
            )

    if not target:
        return command_failure(
            f"I don't know what I want to use the {source_name} on.",
        )

    scenery_id, scenery_data = find_scenery(
        target,
        location_definition,
    )

    if scenery_data:
        return handle_scenery_interaction(
            source_key,
            source_item_id,
            source_state_item_id,
            source_state,
            provider_use,
            scenery_id,
            scenery_data,
            game_state,
        )

    return handle_item_interaction(
        source_key,
        source_item_id,
        source_state_item_id,
        source_state,
        provider_use,
        target,
        location_definition,
        game_state,
    )
