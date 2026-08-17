a1_house_key_2 = (
    "a1_house_key_2",
    {
        "name": "House Key",
        "aliases": [
            "house key",
            "brass key",
            "key",
        ],
        "description": "A tarnished brass key.",
        "inspect": [
            {
                "speaker": "narrator",
                "text": "A tarnished, old fashioned, brass key. It looks sturdy enough to still work...",
            },
            {
                "speaker": "voice",
                "text": "This could come in handy. I wonder what it unlocks...",
            },
        ],
        "looseDescription": (
            "a tarnished <em><span class='item-highlight'>house key</span></em> "
            "lying on the ground."
        ),
        "takeable": True,
        "wearable": False,
        "flammable": False,
        "interchangeableGroup": "house_key",
        "onThrow": {
            "default": {
                "response": "You toss the house key onto the ground.",
                "destroyItem": False,
            },
        },
    },
)
