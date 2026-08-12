# states/game.py

from states.model import (
    BASE_CARRY_LIMIT,
    EQUIPMENT_SLOT_ORDER,
    EQUIPMENT_SLOTS,
    GAME_STATE_REQUIREMENT_KEYS,
    SAVE_VERSION,
    WORLD_ITEM_PLACEMENT,
    newGame,
    carryLimit,
    initialState,
    mergeState,
)
from states.validator import (
    isValidPendingAction,
    isValidSave,
)


def restoreGame(saved_state):
    if not isValidSave(
        saved_state,
    ):
        return None

    restored_state = mergeState(
        initialState,
        saved_state,
    )

    return restored_state
