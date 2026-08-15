from game.itemAccess import (
    findScenery,
    resolveItem,
)
from game.itemDisplay import displayName
from game.responses import commandFailure
from game.useActions import (
    useItem,
    useScenery,
    resolveProvider,
    minimumsMet,
)
from game.worldState import (
    applyChanges,
    currentLocation,
    getItemStateSnapshot,
    getSceneryState,
    stateMatches,
)
from items.registry import itemRegistry


def handleUse(command, location_definition, game_state):
    values = command["values"]
    target = command["target"]

    # Numeric interactions such as safe combinations.
    if values and target:
        scenery_id, scenery_data = findScenery(
            target,
            location_definition,
        )

        if not scenery_data:
            return commandFailure(
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
                location_state = currentLocation(
                    game_state,
                )
                scenery_state = getSceneryState(
                    location_state,
                    scenery_id,
                )
                effects = location_interaction.get(
                    "effects",
                    {},
                )
                applyChanges(
                    scenery_state,
                    effects["sceneryState"],
                )

                return location_interaction["onSuccess"]

            return commandFailure(
                location_interaction["onFail"],
            )

    item_name = command["object"]

    if not item_name:
        return commandFailure(
            "I don't know what I want to use.",
        )

    inventory = game_state["player"]["inventory"]
    source_item_id, clarification = resolveItem(
        item_name,
        inventory,
        allow_interchangeable=True,
    )
    provider_use = None

    if clarification:
        return commandFailure(
            clarification,
        )

    if source_item_id:
        source_key = source_item_id
        source_state_item_id = source_item_id
        source_state = getItemStateSnapshot(
            game_state,
            source_item_id,
        )
        source_name = displayName(
            itemRegistry[source_item_id],
        )
    else:
        provider_item_id, source_key, provider_use, clarification = resolveProvider(
            item_name,
            inventory,
        )

        if clarification:
            return commandFailure(
                clarification,
            )

        if not provider_item_id:
            return commandFailure(
                f"You aren't carrying {item_name} or anything that provides it.",
            )

        source_item_id = None
        source_state_item_id = provider_item_id
        source_state = getItemStateSnapshot(
            game_state,
            provider_item_id,
        )
        source_name = item_name

        if not stateMatches(
            source_state,
            provider_use.get(
                "requiresState",
                {},
            ),
        ):
            return commandFailure(
                provider_use["failResponse"],
            )

        resource = provider_use["resource"]

        if not minimumsMet(
            source_state,
            {
                resource["stateKey"]: resource["minimum"],
            },
        ):
            return commandFailure(
                provider_use["failResponse"],
            )

    if not target:
        return commandFailure(
            f"I don't know what I want to use the {source_name} on.",
        )

    scenery_id, scenery_data = findScenery(
        target,
        location_definition,
    )

    if scenery_data:
        return useScenery(
            source_key,
            source_item_id,
            source_state_item_id,
            source_state,
            provider_use,
            scenery_id,
            scenery_data,
            game_state,
        )

    return useItem(
        source_key,
        source_item_id,
        source_state_item_id,
        source_state,
        provider_use,
        target,
        location_definition,
        game_state,
    )
