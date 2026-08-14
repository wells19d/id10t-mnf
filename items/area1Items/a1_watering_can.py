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
