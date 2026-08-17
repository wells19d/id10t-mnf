a1_first_aid = (
    "a1_first_aid",
    {
        "name": "First-Aid Kit",
        "aliases": ["first-aid kit", "first aid kit", "medical kit", "kit"],
        "description": "A compact first-aid kit with enough supplies for one treatment.",
        "inspect": "The sealed kit contains bandages, antiseptic, and basic wound dressings.",
        "looseDescription": "a compact first-aid kit lying on the ground",
        "takeable": True,
        "wearable": False,
        "interactions": {
            "a1_first_aid": {
                "requires": {
                    "player": {
                        "health": "Medium",
                    },
                },
                "effects": {
                    "player": {
                        "health": "Good",
                        "healthStatus": "Your wound is cleaned and bandaged. You feel steady again.",
                    },
                    "destroySource": True,
                },
                "response": "You clean and dress the cut, using the remaining supplies in the First-Aid Kit.",
                "failResponse": "You do not need to use the First-Aid Kit right now.",
            },
        },
        "onThrow": {
            "default": {
                "response": "You toss the First-Aid Kit onto the ground.",
                "destroyItem": False,
            },
        },
    },
)
