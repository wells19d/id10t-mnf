itemRegistry = {
    "a1_silver_key": {
        "name": "Silver Key",
        "aliases": [
            "silver key",
            "key",
        ],
        "description": "A small silver key.",
        "takeable": True,
        "wearable": False,
    },
    "a1_rusty_axe": {
        "name": "Rusty Axe",
        "aliases": [
            "rusty axe",
            "axe",
            "hatchet",
        ],
        "description": "A rusty axe with a worn wooden handle.",
        "takeable": True,
        "wearable": False,
        "onThrow": {
            "tree": {
                "response": (
                    "The axe sails through the air and thunks " "into the tree trunk."
                ),
                "destroyItem": False,
            },
            "default": {
                "response": ("You throw the axe. It lands uselessly " "in the grass."),
                "destroyItem": False,
            },
        },
        "onUse": {
            "safe": {
                "response": [
                    {
                        "speaker": "narrator",
                        "text": (
                            "You swing the axe into the safe. "
                            "The handle splinters, and the blade "
                            "rebounds past your face."
                        ),
                    },
                    {
                        "speaker": "voice",
                        "text": "That was impressively stupid.",
                    },
                ],
                "destroyItem": True,
            },
        },
    },
    "a1_golden_axe": {
        "name": "Golden Axe",
        "aliases": [
            "golden axe",
            "axe",
            "hatchet",
        ],
        "description": "A golden axe with a sturdy wooden handle.",
        "takeable": True,
        "wearable": False,
        "onThrow": {
            "tree": {
                "response": (
                    "The axe sails through the air and thunks " "into the tree trunk."
                ),
                "destroyItem": False,
            },
            "default": {
                "response": ("You throw the axe. It lands uselessly " "in the grass."),
                "destroyItem": False,
            },
        },
        "onUse": {
            "safe": {
                "response": [
                    {
                        "speaker": "narrator",
                        "text": (
                            "You swing the axe into the safe. "
                            "The handle splinters, and the blade "
                            "rebounds past your face."
                        ),
                    },
                    {
                        "speaker": "voice",
                        "text": "That was impressively stupid.",
                    },
                ],
                "destroyItem": True,
            },
        },
    },
    "a1_silver_axe": {
        "name": "Silver Axe",
        "aliases": [
            "silver axe",
            "axe",
            "hatchet",
        ],
        "description": "A silver axe with a sturdy wooden handle.",
        "takeable": True,
        "wearable": False,
        "onThrow": {
            "tree": {
                "response": (
                    "The axe sails through the air and thunks " "into the tree trunk."
                ),
                "destroyItem": False,
            },
            "default": {
                "response": ("You throw the axe. It lands uselessly " "in the grass."),
                "destroyItem": False,
            },
        },
        "onUse": {
            "safe": {
                "response": [
                    {
                        "speaker": "narrator",
                        "text": (
                            "You swing the axe into the safe. "
                            "The handle splinters, and the blade "
                            "rebounds past your face."
                        ),
                    },
                    {
                        "speaker": "voice",
                        "text": "That was impressively stupid.",
                    },
                ],
                "destroyItem": True,
            },
        },
    },
    "note_18": {
        "aliases": [
            "18",
            "note 18",
            "paper 18",
        ],
        "description": ("A scrap of paper with the number 18 " "written on it."),
        "takeable": True,
        "wearable": False,
    },
    "note_11": {
        "aliases": [
            "11",
            "note 11",
            "paper 11",
        ],
        "description": ("A scrap of paper with the number 11 " "written on it."),
        "takeable": True,
        "wearable": False,
    },
    "note_37": {
        "aliases": [
            "37",
            "note 37",
            "paper 37",
        ],
        "description": ("A scrap of paper with the number 37 " "written on it."),
        "takeable": True,
        "wearable": False,
    },
    "fuse": {
        "aliases": [
            "fuse",
        ],
        "description": "A heavy electrical fuse.",
        "takeable": True,
        "wearable": False,
        "onUse": {
            "fuse panel": {
                "response": (
                    "You insert the fuse into the empty slot. "
                    "Power hums back to life."
                ),
                "setsFlag": "gate_power_restored",
            },
        },
    },
    "keycard": {
        "aliases": [
            "keycard",
            "key card",
            "card",
        ],
        "description": "A security keycard.",
        "takeable": True,
        "wearable": False,
    },
    "security_hat": {
        "aliases": [
            "security hat",
            "hat",
            "cap",
        ],
        "description": "A security guard's hat.",
        "takeable": True,
        "wearable": True,
        "slot": "head",
    },
    "security_jacket": {
        "aliases": [
            "security jacket",
            "jacket",
            "coat",
        ],
        "description": ("A dark security jacket with a faded " "shoulder patch."),
        "takeable": True,
        "wearable": True,
        "slot": "body",
    },
    "security_pants": {
        "aliases": [
            "security pants",
            "pants",
            "trousers",
        ],
        "description": ("A pair of standard security uniform pants."),
        "takeable": True,
        "wearable": True,
        "slot": "legs",
    },
}
