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
    # Runtime changes are created automatically as the game is played.
    "areas": {},
}


currentState = deepcopy(initialState)
