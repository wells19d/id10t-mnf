from areas.locationRegistry import (
    locationDefinitionsByArea,
    locationRegistry,
)
from game.definitionValidationCommon import (
    ACTION_EFFECT_KEYS,
    add_definition_source_errors,
    add_effect_errors,
    add_integer_map_errors,
    add_intro_response_errors,
    add_item_reference_errors,
    add_local_state_description_errors,
    add_message_errors,
    add_requirement_errors,
    add_response_errors,
    add_throw_action_errors,
)
from game.itemDefinitionValidator import (
    ITEM_INTERACTION_EFFECT_KEYS,
    ITEM_INTERACTION_REQUIREMENT_KEYS,
    ITEM_RESPONSE_KEYS,
    add_item_interaction_errors,
    get_item_definition_errors,
)
from game.locationDefinitionValidator import (
    ACTION_REQUIREMENT_KEYS,
    COMBINATION_EFFECT_KEYS,
    DIRECTIONS,
    SCENERY_RESPONSE_KEYS,
    add_exit_errors,
    add_room_exit_errors,
    add_scenery_errors,
    add_state_description_errors,
    get_location_definition_errors,
)
from game.responses import VALID_RESPONSE_SPEAKERS
from items.itemRegistry import (
    itemDefinitionsByArea,
    itemRegistry,
)
from states.gameState import (
    EQUIPMENT_SLOTS,
    GAME_STATE_REQUIREMENT_KEYS,
)


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
