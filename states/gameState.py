# states/gameState.py

from copy import deepcopy

initialState = {
    "player": {
        "introComplete": False,
        "currentArea": "area1",
        "currentLocation": "clearing",
        "currentDirection": None,
        "currentShortDirection": None,
        "lastDirection": None,
        "lastShortDirection": None,
        "inventory": [],
        "equipped": [],
        "health": "Medium",
    },
    "itemStates": {},
    "areas": {},
}


currentState = deepcopy(
    initialState,
)


def merge_state(
    default_state,
    saved_state,
):
    merged_state = deepcopy(
        default_state,
    )

    for key, saved_value in saved_state.items():
        default_value = merged_state.get(
            key,
        )

        if isinstance(default_value, dict) and isinstance(saved_value, dict):
            merged_state[key] = merge_state(
                default_value,
                saved_value,
            )
        else:
            merged_state[key] = deepcopy(
                saved_value,
            )

    return merged_state


def reset_game_state():
    currentState.clear()

    currentState.update(
        deepcopy(
            initialState,
        )
    )

    return currentState


def restore_game_state(saved_state):
    if not isinstance(
        saved_state,
        dict,
    ):
        return False

    saved_player = saved_state.get(
        "player",
    )

    if not isinstance(
        saved_player,
        dict,
    ):
        return False

    restored_state = merge_state(
        initialState,
        saved_state,
    )

    currentState.clear()

    currentState.update(
        restored_state,
    )

    return True
