a1_silver_locket = (
    "a1_silver_locket",
    {
        "name": "Silver Locket",
        "aliases": [
            "silver locket",
            "locket",
            "pendant",
        ],
        "description": (
            "A small silver locket, blackened and scarred by intense heat."
        ),
        "inspect": [
            {
                "speaker": "narrator",
                "text": (
                    "The silver locket is badly scorched, but its tiny hinge and clasp "
                    "somehow survived the fire."
                ),
            },
            {
                "speaker": "voice",
                "text": "Someone cared enough to keep this close.",
            },
        ],
        "worldDescription": (
            "a blackened <em><span class='item-highlight'>silver locket</span></em> "
            "resting among the burned scraps."
        ),
        "looseDescription": (
            "a blackened <em><span class='item-highlight'>silver locket</span></em> "
            "lying on the ground."
        ),
        "stateDescriptions": [
            {
                "requiresState": {
                    "isOpen": True,
                },
                "description": (
                    "The scorched silver locket hangs open, exposing the ruined remains "
                    "of a photograph."
                ),
            },
        ],
        "takeable": True,
        "wearable": False,
        "flammable": False,
        "openable": True,
        "closeable": True,
        "state": {
            "isOpen": False,
        },
        "openResponse": [
            {
                "speaker": "narrator",
                "text": (
                    "You work the heat-warped clasp loose and open the locket. A photograph "
                    "once rested inside, but the fire reduced it to a dark, featureless scrap."
                ),
            },
            {
                "speaker": "voice",
                "text": "Whatever memory it held is gone now.",
            },
        ],
        "closeResponse": "You close the silver locket.",
        "onThrow": {
            "default": {
                "response": "You toss the silver locket onto the ground.",
                "destroyItem": False,
            },
        },
    },
)
