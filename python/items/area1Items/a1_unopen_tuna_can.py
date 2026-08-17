a1_unopen_tuna_can = (
    "a1_unopen_tuna_can",
    {
        "name": "Unopened Tuna Can",
        "aliases": ["unopened tuna can", "tuna can", "tuna", "can"],
        "description": "An unopened can of tuna with a faded label.",
        "inspect": "The can is dented but still sealed. Its expiration date is unreadable.",
        "looseDescription": "an unopened tuna can lying on the ground",
        "takeable": True,
        "wearable": False,
        "onThrow": {
            "default": {
                "response": "You toss the tuna can onto the ground with a dull clank.",
                "destroyItem": False,
            },
        },
    },
)
