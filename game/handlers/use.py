from game.handlers.common import (
    apply_state_changes,
    command_failure,
    find_scenery,
    get_current_area_state,
    get_current_location_state,
    get_item_display_name,
    get_item_state,
    get_scenery_state,
    resolve_item,
    state_matches,
    unequip_item,
)
from game.itemRegistry import itemRegistry


def handle_use(command, current_area, game_state):
    values = command["values"]
    target = command["target"]

    # Numeric interactions such as safe combinations.
    if values and target:
        scenery_id, scenery_data = find_scenery(
            target,
            current_area,
        )

        if not scenery_data:
            return command_failure(
                f"I don't see a {target} here.",
            )

        area_interaction = current_area.get(
            "interactions",
            {},
        ).get(
            scenery_id,
        )

        if area_interaction and area_interaction.get("type") == "combination":
            correct_combination = area_interaction.get(
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

                effects = area_interaction.get(
                    "effects",
                    {},
                )

                apply_state_changes(
                    scenery_state,
                    effects.get(
                        "sceneryState",
                        {
                            "isOpen": True,
                        },
                    ),
                )

                return area_interaction["onSuccess"]

            return command_failure(
                area_interaction["onFail"],
            )

    item_name = command["object"]

    if not item_name:
        return command_failure(
            "I don't know what I want to use.",
        )

    inventory = game_state["player"]["inventory"]

    item_id, clarification = resolve_item(
        item_name,
        inventory,
    )

    if clarification:
        return command_failure(
            clarification,
        )

    if not item_id:
        return command_failure(
            f"You aren't carrying {item_name}.",
        )

    item = itemRegistry[item_id]

    display_name = get_item_display_name(
        item,
    )

    if not target:
        return command_failure(
            f"I don't know what I want to use " f"the {display_name} on.",
        )

    scenery_id, scenery_data = find_scenery(
        target,
        current_area,
    )

    if not scenery_data:
        return command_failure(
            f"I don't see a {target} here.",
        )

    # The target scenery defines which items can
    # interact with it and what those interactions do.
    interaction = scenery_data.get(
        "interactions",
        {},
    ).get(
        item_id,
    )

    if not interaction:
        return command_failure(
            f"You can't use the " f"{display_name} on {scenery_id} here.",
        )

    location_state = get_current_location_state(
        game_state,
    )

    scenery_state = get_scenery_state(
        location_state,
        scenery_id,
    )

    item_state = get_item_state(
        game_state,
        item_id,
    )

    area_state = get_current_area_state(
        game_state,
    )

    requirements = interaction.get(
        "requires",
        {},
    )

    # Required state of the item being used.
    required_item_state = requirements.get(
        "itemState",
        {},
    )

    if not state_matches(
        item_state,
        required_item_state,
    ):
        return command_failure(
            interaction.get(
                "failResponse",
                "That won't work right now.",
            )
        )

    # Required state of the target scenery.
    required_scenery_state = requirements.get(
        "sceneryState",
        {},
    )

    if not state_matches(
        scenery_state,
        required_scenery_state,
    ):
        return command_failure(
            interaction.get(
                "failResponse",
                "That won't work right now.",
            )
        )

    # Required inventory items.
    for required_item_id in requirements.get(
        "inventory",
        [],
    ):
        if required_item_id not in inventory:
            return command_failure(
                interaction.get(
                    "failResponse",
                    "You don't have everything you need.",
                )
            )

    # Required equipped items.
    equipped = game_state["player"]["equipped"]

    for required_item_id in requirements.get(
        "equipped",
        [],
    ):
        if required_item_id not in equipped:
            return command_failure(
                interaction.get(
                    "failResponse",
                    "You aren't properly equipped.",
                )
            )

    # Required area flags.
    required_flags = requirements.get(
        "flags",
        {},
    )

    if not state_matches(
        area_state["flags"],
        required_flags,
    ):
        return command_failure(
            interaction.get(
                "failResponse",
                "That won't work right now.",
            )
        )

    # All requirements passed.
    effects = interaction.get(
        "effects",
        {},
    )

    apply_state_changes(
        scenery_state,
        effects.get(
            "sceneryState",
        ),
    )

    apply_state_changes(
        item_state,
        effects.get(
            "itemState",
        ),
    )

    apply_state_changes(
        area_state["flags"],
        effects.get(
            "flags",
        ),
    )

    if effects.get(
        "destroyItem",
        False,
    ):
        unequip_item(
            game_state,
            item_id,
        )

        inventory.remove(
            item_id,
        )

    return interaction.get(
        "response",
        f"You use the {display_name} on the {scenery_id}.",
    )
