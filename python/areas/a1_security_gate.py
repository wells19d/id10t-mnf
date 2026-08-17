a1_security_gate = {
    "name": "Security Gate",
    "intro": [
        {
            "speaker": "narrator",
            "text": "A high security gate blocks the road. A small guard station stands beside it, with a fuse box mounted on its west wall and a card reader beside the station door.",
        }
    ],
    "description": "The sealed Security Gate spans the road. The powerless guard station has an exterior fuse box and a card reader beside its door. The road returns south.",
    "stateDescriptions": [
        {
            "requires": {"flags": {"guardPower": True}},
            "description": "Power hums through the guard station beside the closed Security Gate. The card reader glows beside the station door.",
        },
    ],
    "items": [],
    "scenery": {
        "fuse box": {
            "aliases": ["fuse box", "box", "electrical box", "panel"],
            "description": "An exterior fuse box on the west wall contains a burned-out fuse socket.",
            "state": {"isRepaired": False},
            "interactions": {
                "a1_replacement_fuse": {
                    "requires": {"sceneryState": {"isRepaired": False}},
                    "effects": {
                        "sceneryState": {"isRepaired": True},
                        "flags": {"guardPower": True},
                        "destroyItem": True,
                    },
                    "response": "You install the Replacement Fuse. The fuse box closes with a heavy click, and power returns to the guard station.",
                    "failResponse": "The replacement fuse has already been installed.",
                },
            },
        },
        "card reader": {
            "aliases": ["card reader", "reader", "key card reader", "station door"],
            "description": "A security card reader controls access to the guard station.",
            "state": {"isAuthorized": False},
            "interactions": {
                "a1_gate_key_card": {
                    "requires": {
                        "sceneryState": {"isAuthorized": False},
                        "flags": {"guardPower": True},
                        "equipped": [
                            "a1_security_hat",
                            "a1_security_jacket",
                            "a1_security_pants",
                        ],
                    },
                    "effects": {
                        "sceneryState": {"isAuthorized": True},
                        "destroyItem": True,
                    },
                    "response": "The powered reader accepts the Gate Key Card and unlocks the Guard Station. The card is no longer needed, so you discard it.",
                    "failResponse": "Access is denied. The reader needs power and expects a complete security uniform.",
                },
            },
        },
        "gate": {
            "aliases": ["gate", "security gate"],
            "description": "The reinforced gate is controlled from inside the guard station.",
        },
    },
    "roomExits": {
        "guard station": {
            "location": "a1_guard_station",
            "requires": {"sceneryState": {"card reader": {"isAuthorized": True}}},
            "blockedResponse": "The Guard Station is locked. Its card reader has not granted access.",
        },
        "station": {
            "location": "a1_guard_station",
            "requires": {"sceneryState": {"card reader": {"isAuthorized": True}}},
            "blockedResponse": "The Guard Station is locked. Its card reader has not granted access.",
        },
    },
    "exits": {"north": False, "south": "a1_road_access", "east": False, "west": False},
}


a1_guard_station = {
    "name": "Guard Station",
    "intro": [
        {
            "speaker": "narrator",
            "text": "You enter the cramped Guard Station. A large gate-control button dominates the powered console.",
        }
    ],
    "description": "Dusty security monitors surround a powered control console. A heavy button is labeled 'OPEN GATE'. The station door leads outside.",
    "items": [],
    "scenery": {
        "gate button": {
            "aliases": ["gate button", "button", "control button", "gate control"],
            "description": "A heavy illuminated button controls the security gate.",
            "state": {"isPressed": False},
            "interactions": {
                "environment": {
                    "requires": {
                        "flags": {"guardPower": True},
                        "sceneryState": {"isPressed": False},
                    },
                    "effects": {
                        "flags": {"gateOpen": True},
                        "sceneryState": {"isPressed": True},
                    },
                    "response": "You press the control button. Motors strain to life, and the Security Gate slides open across the road.",
                    "failResponse": "The gate controls cannot do anything right now.",
                },
            },
        },
    },
    "roomExits": {"outside": "a1_security_gate", "security gate": "a1_security_gate"},
    "exits": {
        "north": {
            "location": "a2_entry",
            "requires": {"flags": {"gateOpen": True}},
            "blockedResponse": "The Security Gate is still closed.",
            "effects": {
                "flags": {
                    "area1Complete": True,
                    "guardPower": False,
                    "gateOpen": False,
                    "gateJammed": True,
                }
            },
        },
        "south": False,
        "east": False,
        "west": False,
    },
}
