# states/gameState.py

from copy import deepcopy

SAVE_VERSION = 1

GAME_STATE_REQUIREMENT_KEYS = frozenset(
    {
        "player",
        "inventory",
        "equipped",
        "flags",
        "sceneryState",
        "itemStates",
    }
)

initialState = {
    "saveVersion": SAVE_VERSION,
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


def create_game_state():
    return deepcopy(
        initialState,
    )


def restore_game_state(saved_state):
    if not isinstance(
        saved_state,
        dict,
    ):
        return None

    if saved_state.get(
        "saveVersion",
    ) != SAVE_VERSION:
        return None

    saved_player = saved_state.get(
        "player",
    )

    if not isinstance(
        saved_player,
        dict,
    ):
        return None

    restored_state = merge_state(
        initialState,
        saved_state,
    )

    return restored_state
