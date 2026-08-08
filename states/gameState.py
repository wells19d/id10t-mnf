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
    # Runtime state for items.
    # Example:
    # "a1_watering_can": {
    #     "filled": False,
    # }
    "itemStates": {},
    # Runtime changes to areas and scenery.
    "areas": {},
}


currentState = deepcopy(
    initialState,
)
