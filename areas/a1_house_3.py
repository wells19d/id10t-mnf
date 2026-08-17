def _storage(name, aliases, items=None, empty_response=None):
    return {
        "aliases": aliases,
        "description": f"A worn {name} built into the room.",
        "searchable": True,
        "openable": True,
        "closeable": True,
        "state": {"isOpen": False},
        "items": items or [],
        "searchEmptyResponse": empty_response or f"The {name} is empty.",
    }


def _house_door():
    interactions = {}

    for source_id, response in {
        "a1_house_key_1": "The key unlocks the green house door, then breaks in the corroded lock.",
        "a1_house_key_2": "The key unlocks the green house door, then breaks in the corroded lock.",
        "a1_rusty_axe": "You break the green house door open. The Rusty Axe splinters with it.",
        "a1_lock_pick": "You pick the green house lock. The Lock Pick bends and snaps as the door opens.",
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
            "failResponse": "The green house door is already unlocked.",
        }

    return {
        "aliases": ["door", "front door", "green house door", "house door"],
        "description": "A green front door held by a badly corroded lock.",
        "openable": True,
        "closeable": True,
        "state": {"isLocked": True, "isOpen": False, "isBroken": False},
        "lockedResponse": "The green house door is locked.",
        "brokenCloseResponse": "The broken green house door cannot be closed.",
        "interactions": interactions,
    }


a1_house_3 = {
    "name": "Green House",
    "intro": [
        {
            "speaker": "narrator",
            "text": "A weathered green house leans beneath the surrounding trees.",
        }
    ],
    "description": "The green house's front door is locked. Paths lead north and east.",
    "items": [],
    "scenery": {"door": _house_door()},
    "roomExits": {
        "inside": {
            "location": "a1_house_3_living_room",
            "requires": {"sceneryState": {"door": {"isOpen": True}}},
            "blockedResponse": "The green house door is closed and locked.",
        },
        "living room": {
            "location": "a1_house_3_living_room",
            "requires": {"sceneryState": {"door": {"isOpen": True}}},
            "blockedResponse": "The green house door is closed and locked.",
        },
    },
    "exits": {
        "north": "a1_fallen_nursery",
        "south": False,
        "east": "a1_silent_grove",
        "west": False,
    },
}


a1_house_3_living_room = {
    "name": "Green House - Living Room",
    "intro": [
        {"speaker": "narrator", "text": "You enter the green house's dim living room."}
    ],
    "description": "A dim living room connects to a kitchen, bathroom, and two bedrooms. A drawer rests beneath a boarded window, and the front door leads outside.",
    "items": [],
    "scenery": {"drawer": _storage("drawer", ["drawer", "living room drawer"])},
    "roomExits": {
        "kitchen": "a1_house_3_kitchen",
        "bathroom": "a1_house_3_bathroom",
        "bedroom 1": "a1_house_3_bedroom_1",
        "bedroom 2": "a1_house_3_bedroom_2",
        "outside": "a1_house_3",
        "living room": "a1_house_3_living_room",
    },
    "exits": {"north": False, "south": False, "east": False, "west": False},
}


a1_house_3_kitchen = {
    "name": "Green House - Kitchen",
    "intro": [],
    "description": "A stripped kitchen with empty cabinets and a single drawer. The living room is nearby.",
    "items": [],
    "scenery": {
        "drawer": _storage("drawer", ["drawer", "kitchen drawer"]),
        "cabinet": _storage("cabinet", ["cabinet", "cabinets", "kitchen cabinet"]),
    },
    "roomExits": {"living room": "a1_house_3_living_room", "outside": "a1_house_3"},
    "exits": {"north": False, "south": False, "east": False, "west": False},
}


a1_house_3_bathroom = {
    "name": "Green House - Bathroom",
    "intro": [],
    "description": "A damp bathroom with a rust-spotted medicine cabinet. The living room is nearby.",
    "items": [],
    "scenery": {
        "medicine cabinet": _storage(
            "medicine cabinet", ["medicine cabinet", "cabinet"], ["a1_first_aid"]
        )
    },
    "roomExits": {"living room": "a1_house_3_living_room", "outside": "a1_house_3"},
    "exits": {"north": False, "south": False, "east": False, "west": False},
}


a1_house_3_bedroom_1 = {
    "name": "Green House - Bedroom 1",
    "intro": [],
    "description": "A calendar lies open on the floor of the first bedroom beside an empty drawer and closet. The living room is nearby.",
    "items": ["a1_code_1"],
    "scenery": {
        "drawer": _storage("drawer", ["drawer", "bedroom drawer"]),
        "closet": _storage("closet", ["closet", "bedroom closet"]),
    },
    "roomExits": {"living room": "a1_house_3_living_room", "outside": "a1_house_3"},
    "exits": {"north": False, "south": False, "east": False, "west": False},
}


a1_house_3_bedroom_2 = {
    "name": "Green House - Bedroom 2",
    "intro": [],
    "description": "A pair of security pants has been left on the bed. A combination safe sits on the floor of the closet beside a note from Charles.",
    "items": [],
    "scenery": {
        "bed": {
            "aliases": ["bed", "security pants", "pants"],
            "description": "A narrow bed with a pair of security pants folded on top.",
            "searchable": True,
            "items": ["a1_security_pants"],
            "searchEmptyResponse": "The bed holds nothing else useful.",
        },
        "drawer": _storage("drawer", ["drawer", "bedroom drawer"]),
        "closet": _storage(
            "closet",
            ["closet", "bedroom closet"],
            empty_response="A heavy combination safe sits on the closet floor.",
        ),
        "safe": {
            "aliases": ["safe", "combination safe"],
            "description": "A heavy combination safe. A note reads: 'Larry... Your son's age, the day David gets back, and the inspection date. You should know by now which one comes first. Charles.'",
            "searchable": True,
            "openable": True,
            "closeable": True,
            "state": {"isLocked": True, "isOpen": False},
            "lockedResponse": "The safe is locked. Its keypad accepts a three-part combination.",
            "searchBlockedResponse": "The safe is locked.",
            "searchEmptyResponse": "The safe is empty.",
            "contentsRequiresState": {"isLocked": False},
            "items": ["a1_replacement_fuse", "a1_gate_key_card"],
            "interactions": {
                "environment": {
                    "requires": {"sceneryState": {"isLocked": True}},
                    "effects": {},
                    "response": "The keypad is ready. Enter the combination with 'use 29 11 18 on safe'.",
                    "failResponse": "The safe is already unlocked.",
                },
            },
        },
    },
    "interactions": {
        "safe": {
            "type": "combination",
            "combination": ["29", "11", "18"],
            "effects": {
                "sceneryState": {"isLocked": False, "isOpen": True},
                "destroyInventoryItems": ["a1_code_1", "a1_code_2", "a1_code_3"],
            },
            "onSuccess": "The safe unlocks. The two calendar pages and Birthday Card have served their purpose and are no longer useful, so you discard any of them you still carry.",
            "onFail": "The safe rejects the combination. The numbers may need to be entered in a different order.",
        },
    },
    "roomExits": {"living room": "a1_house_3_living_room", "outside": "a1_house_3"},
    "exits": {"north": False, "south": False, "east": False, "west": False},
}
