# states/gameState.py

from states.stateModel import (
    BASE_CARRY_LIMIT,
    EQUIPMENT_SLOT_ORDER,
    EQUIPMENT_SLOTS,
    GAME_STATE_REQUIREMENT_KEYS,
    INITIAL_ITEM_LOCATIONS,
    SAVE_VERSION,
    WORLD_ITEM_PLACEMENT,
    build_initial_item_locations,
    create_game_state,
    get_total_carry_capacity,
    initialState,
    merge_state,
)
from states.stateValidation import (
    has_exclusive_item_ownership,
    is_valid_item_id_list,
    is_valid_item_states,
    is_valid_location_state,
    is_valid_locations_state,
    is_valid_pending_action,
    is_valid_player_state,
    is_valid_saved_state,
)


def restore_game_state(saved_state):
    if not is_valid_saved_state(
        saved_state,
    ):
        return None

    restored_state = merge_state(
        initialState,
        saved_state,
    )

    return restored_state
