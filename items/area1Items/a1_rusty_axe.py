a1_rusty_axe = (
    "a1_rusty_axe",
    {
        "name": "Rusty Axe",
        "aliases": [
            "rusty axe",
            "axe",
            "hatchet",
        ],
        "description": "A rusty axe with a worn wooden handle.",
        "inspect": [
            {
                "speaker": "narrator",
                "text": "A rusty axe. The blade is dulled and the handle is worn from years of use.",
            },
            {
                "speaker": "voice",
                "text": "It's seen better days, but it could still be useful...",
            },
        ],
        "worldDescription": (
            "a <em><span class='item-highlight'>rusty axe</span></em> "
            "embedded into the base of the massive tree, its blade dulled and handle worn from years of use."
        ),
        "looseDescription": (
            "a <em><span class='item-highlight'>rusty axe</span></em> "
            "lying on the ground."
        ),
        "takeable": True,
        "wearable": False,
        "onThrow": {
            "default": {
                "response": (
                    "You throw the axe. It spins through the air and drops to the ground."
                ),
                "destroyItem": False,
            },
        },
    },
)
