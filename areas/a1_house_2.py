def _storage(name, aliases, items=None):
    return {
        "aliases": aliases,
        "description": f"A worn {name} built into the room.",
        "searchable": True,
        "openable": True,
        "closeable": True,
        "state": {"isOpen": False},
        "items": items or [],
        "searchEmptyResponse": f"The {name} is empty.",
    }


def _house_door():
    interactions = {}

    for source_id, response in {
        "a1_house_key_1": "The key unlocks the blue house door, then snaps in the stiff lock.",
        "a1_house_key_2": "The key unlocks the blue house door, then snaps in the stiff lock.",
        "a1_rusty_axe": "You smash the blue house door open. The Rusty Axe breaks apart after the final strike.",
        "a1_lock_pick": "The blue house lock clicks open, but the Lock Pick bends beyond use.",
    }.items():
        effects = {
            "sceneryState": {"isLocked": False, "isOpen": True},
            "destroyItem": True,
        }

        if source_id == "a1_rusty_axe":
            effects["sceneryState"]["isBroken"] = True

        interactions[source_id] = {
            "requires": {"sceneryState": {"isLocked": True}},
            "effects": effects,
            "response": response,
            "failResponse": "The blue house door is already unlocked.",
        }

    return {
        "aliases": ["door", "front door", "blue house door", "house door"],
        "description": "A faded blue front door secured by an old lock.",
        "openable": True,
        "closeable": True,
        "state": {"isLocked": True, "isOpen": False, "isBroken": False},
        "lockedResponse": "The blue house door is locked.",
        "brokenCloseResponse": "The broken blue house door cannot be closed.",
        "interactions": interactions,
    }


a1_house_2 = {
    "name": "Blue House",
    "intro": [
        {
            "speaker": "narrator",
            "text": "A faded blue house stands between the clearing and the stone ring.",
        }
    ],
    "description": "The abandoned blue house has a locked front door. Paths lead north and south.",
    "items": [],
    "scenery": {"door": _house_door()},
    "roomExits": {
        "inside": {
            "location": "a1_house_2_living_room",
            "requires": {"sceneryState": {"door": {"isOpen": True}}},
            "blockedResponse": "The blue house door is closed and locked.",
        },
        "living room": {
            "location": "a1_house_2_living_room",
            "requires": {"sceneryState": {"door": {"isOpen": True}}},
            "blockedResponse": "The blue house door is closed and locked.",
        },
    },
    "exits": {
        "north": "a1_stone_ring",
        "south": "a1_clearing",
        "east": False,
        "west": False,
    },
}


a1_house_2_living_room = {
    "name": "Blue House - Living Room",
    "intro": [
        {"speaker": "narrator", "text": "You enter the blue house's quiet living room."}
    ],
    "description": "A sparse living room connects to the kitchen, bathroom, and bedroom. A drawer sits against one wall, and the front door leads outside.",
    "items": [],
    "scenery": {"drawer": _storage("drawer", ["drawer", "living room drawer"])},
    "roomExits": {
        "kitchen": "a1_house_2_kitchen",
        "bathroom": "a1_house_2_bathroom",
        "bedroom": "a1_house_2_bedroom",
        "bedroom 1": "a1_house_2_bedroom",
        "outside": "a1_house_2",
        "living room": "a1_house_2_living_room",
    },
    "exits": {"north": False, "south": False, "east": False, "west": False},
}


a1_house_2_kitchen = {
    "name": "Blue House - Kitchen",
    "intro": [],
    "description": "A stale kitchen with a row of cabinets and one jammed-looking drawer. The living room is nearby.",
    "items": [],
    "scenery": {
        "drawer": _storage("drawer", ["drawer", "kitchen drawer"], ["a1_matchbox_2"]),
        "cabinet": _storage(
            "cabinet",
            ["cabinet", "cabinets", "kitchen cabinet"],
            ["a1_unopen_tuna_can"],
        ),
    },
    "roomExits": {"living room": "a1_house_2_living_room", "outside": "a1_house_2"},
    "exits": {"north": False, "south": False, "east": False, "west": False},
}


a1_house_2_bathroom = {
    "name": "Blue House - Bathroom",
    "intro": [],
    "description": "A cramped bathroom with a cloudy mirror and medicine cabinet. The living room is nearby.",
    "items": [],
    "scenery": {
        "medicine cabinet": _storage(
            "medicine cabinet", ["medicine cabinet", "cabinet"]
        )
    },
    "roomExits": {"living room": "a1_house_2_living_room", "outside": "a1_house_2"},
    "exits": {"north": False, "south": False, "east": False, "west": False},
}


a1_house_2_bedroom = {
    "name": "Blue House - Bedroom",
    "intro": [],
    "description": "The house's only bedroom contains a drawer and a narrow closet. The living room is nearby.",
    "items": [],
    "scenery": {
        "drawer": _storage(
            "drawer", ["drawer", "bedroom drawer"], ["a1_security_jacket"]
        ),
        "closet": _storage("closet", ["closet", "bedroom closet"]),
    },
    "roomExits": {"living room": "a1_house_2_living_room", "outside": "a1_house_2"},
    "exits": {"north": False, "south": False, "east": False, "west": False},
}
