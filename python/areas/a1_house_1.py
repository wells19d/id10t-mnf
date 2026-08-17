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
        "a1_house_key_1": "The key turns with effort. You unlock and open the red house door; the old key snaps in the lock and is no longer usable.",
        "a1_house_key_2": "The key turns with effort. You unlock and open the red house door; the old key snaps in the lock and is no longer usable.",
        "a1_rusty_axe": "You break the door open with the Rusty Axe. The axe head splits from its handle and is no longer usable.",
        "a1_lock_pick": "You pick the old lock. The door opens, but the Lock Pick bends beyond use.",
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
            "failResponse": "The red house door is already unlocked.",
        }

    return {
        "aliases": ["door", "front door", "red house door", "house door"],
        "description": "A weathered front door secured by an old mechanical lock.",
        "openable": True,
        "closeable": True,
        "state": {"isLocked": True, "isOpen": False, "isBroken": False},
        "lockedResponse": "The red house door is locked.",
        "brokenCloseResponse": "The shattered red house door can no longer be closed.",
        "interactions": interactions,
    }


a1_house_1 = {
    "name": "Red House",
    "intro": [
        {
            "speaker": "narrator",
            "text": "A small red house stands among the trees, its paint faded and its front door shut tight.",
        }
    ],
    "description": "A weathered red house sits at the forest edge. Its front door leads inside, while paths run east and west.",
    "items": [],
    "scenery": {"door": _house_door()},
    "roomExits": {
        "inside": {
            "location": "a1_house_1_living_room",
            "requires": {"sceneryState": {"door": {"isOpen": True}}},
            "blockedResponse": "The red house door is closed and locked.",
        },
        "living room": {
            "location": "a1_house_1_living_room",
            "requires": {"sceneryState": {"door": {"isOpen": True}}},
            "blockedResponse": "The red house door is closed and locked.",
        },
    },
    "exits": {
        "north": False,
        "south": False,
        "east": "a1_road_access",
        "west": "a1_silent_grove",
    },
}


a1_house_1_living_room = {
    "name": "Red House - Living Room",
    "intro": [
        {
            "speaker": "narrator",
            "text": "You step into the red house's dusty living room.",
        }
    ],
    "description": "A dusty living room serves as the center of the red house. A calendar lies on the floor beside an old drawer. The kitchen, bathroom, and two bedrooms open from here, and the front door leads outside.",
    "items": ["a1_code_3"],
    "scenery": {
        "drawer": _storage("drawer", ["drawer", "living room drawer"], ["a1_lock_pick"])
    },
    "roomExits": {
        "kitchen": "a1_house_1_kitchen",
        "bathroom": "a1_house_1_bathroom",
        "bedroom 1": "a1_house_1_bedroom_1",
        "bedroom 2": "a1_house_1_bedroom_2",
        "outside": "a1_house_1",
        "living room": "a1_house_1_living_room",
    },
    "exits": {"north": False, "south": False, "east": False, "west": False},
}


a1_house_1_kitchen = {
    "name": "Red House - Kitchen",
    "intro": [],
    "description": "A cramped kitchen with worn cabinets and a shallow drawer. The living room is nearby.",
    "items": [],
    "scenery": {
        "drawer": _storage("drawer", ["drawer", "kitchen drawer"], ["a1_flashlight"]),
        "cabinet": _storage("cabinet", ["cabinet", "cabinets", "kitchen cabinet"]),
    },
    "roomExits": {"living room": "a1_house_1_living_room", "outside": "a1_house_1"},
    "exits": {"north": False, "south": False, "east": False, "west": False},
}


a1_house_1_bathroom = {
    "name": "Red House - Bathroom",
    "intro": [],
    "description": "A small bathroom with a cracked mirror and a medicine cabinet. The living room is nearby.",
    "items": [],
    "scenery": {
        "medicine cabinet": _storage(
            "medicine cabinet", ["medicine cabinet", "cabinet"]
        )
    },
    "roomExits": {"living room": "a1_house_1_living_room", "outside": "a1_house_1"},
    "exits": {"north": False, "south": False, "east": False, "west": False},
}


a1_house_1_bedroom_1 = {
    "name": "Red House - Bedroom 1",
    "intro": [],
    "description": "A neglected bedroom containing a narrow bed, a drawer, and a closet. The living room is nearby.",
    "items": [],
    "scenery": {
        "drawer": _storage("drawer", ["drawer", "bedroom drawer"]),
        "closet": _storage("closet", ["closet", "bedroom closet"], ["a1_security_hat"]),
    },
    "roomExits": {"living room": "a1_house_1_living_room", "outside": "a1_house_1"},
    "exits": {"north": False, "south": False, "east": False, "west": False},
}


a1_house_1_bedroom_2 = {
    "name": "Red House - Bedroom 2",
    "intro": [],
    "description": "A second dusty bedroom with an empty drawer and closet. The living room is nearby.",
    "items": [],
    "scenery": {
        "drawer": _storage("drawer", ["drawer", "bedroom drawer"]),
        "closet": _storage("closet", ["closet", "bedroom closet"]),
    },
    "roomExits": {"living room": "a1_house_1_living_room", "outside": "a1_house_1"},
    "exits": {"north": False, "south": False, "east": False, "west": False},
}
