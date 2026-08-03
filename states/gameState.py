# states/gameState.py
from copy import deepcopy

initialState = {
    "player": {
        "introComplete": False,
        "currentLocation": "clearing",
        "currentDirection": None,
        "currentShortDirection": None,
        "lastDirection": None,
        "lastShortDirection": None,
        "inventory": [],
        "health": "Medium",
    },
    "areas": {
        "clearing": {
            "visited": True,
            "itemsAvailable": [],
            "itemsFound": [],
        },
        "fallen_nursery": {
            "visited": False,
            "itemsAvailable": ["axe"],
            "itemsFound": [],
        },
        "house_1": {
            "visited": False,
            "itemsAvailable": [],
            "itemsFound": [],
        },
        "house_2": {
            "visited": False,
            "itemsAvailable": [],
            "itemsFound": [],
        },
        "house_3": {
            "visited": False,
            "itemsAvailable": [],
            "itemsFound": [],
        },
        "lake_east": {
            "visited": False,
            "itemsAvailable": [],
            "itemsFound": [],
        },
        "lake_south": {
            "visited": False,
            "itemsAvailable": [],
            "itemsFound": [],
        },
        "massive_tree": {
            "visited": False,
            "itemsAvailable": [],
            "itemsFound": [],
        },
        "road_access": {
            "visited": False,
            "itemsAvailable": [],
            "itemsFound": [],
        },
        "security_gate": {
            "visited": False,
            "itemsAvailable": [],
            "itemsFound": [],
        },
        "silent_grove": {
            "visited": False,
            "itemsAvailable": [],
            "itemsFound": [],
        },
        "stone_ring": {
            "visited": False,
            "itemsAvailable": [],
            "itemsFound": [],
        },
    },
}

currentState = deepcopy(initialState)
