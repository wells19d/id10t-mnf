a1_watering_can = (
    "a1_watering_can",
    {
        "name": "Watering Can",
        "aliases": [
            "watering can",
            "can",
        ],
        "description": "A rusty watering can",
        "inspect": [
            {
                "speaker": "narrator",
                "text": "A rusty watering can. It looks like it hasn't been used in a while.",
            },
            {
                "speaker": "voice",
                "text": "I could use this to carry water... probably not safe to drink from it though.",
            },
        ],
        "inspectState": [
            {
                "requiresState": {
                    "liquidType": "water",
                },
                "description": [
                    {
                        "speaker": "narrator",
                        "text": "A rusty watering can filled with water.",
                    },
                ],
            },
        ],
        "worldDescription": (
            "a <em><span class='item-highlight'>watering can</span></em> "
            "lying next to the tree."
        ),
        "looseDescription": (
            "a <em><span class='item-highlight'>watering can</span></em> "
            "lying on the ground."
        ),
        "takeable": True,
        "wearable": False,
        "flammable": False,
        "state": {
            "liquidType": "empty",
        },
        "emptyActions": [
            {
                "requiresState": {
                    "liquidType": "water",
                },
                "effects": {
                    "liquidType": "empty",
                },
                "response": [
                    {
                        "speaker": "narrator",
                        "text": (
                            "You tip the watering can over and spill its water onto "
                            "the ground."
                        ),
                    },
                ],
            },
        ],
        "emptyFailResponse": "The watering can is already empty.",
        "interactions": {},
        "onThrow": {
            "default": {
                "response": (
                    "You toss the watering can onto the ground. It lands with a dull thud."
                ),
                "destroyItem": False,
            },
        },
    },
)
