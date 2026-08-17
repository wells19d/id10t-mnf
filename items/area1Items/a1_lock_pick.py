a1_lock_pick = (
    "a1_lock_pick",
    {
        "name": "Lock Pick",
        "aliases": ["lock pick", "lockpick", "pick"],
        "description": "A thin, improvised lock pick.",
        "inspect": "The metal pick is worn and likely has one good lock left in it.",
        "looseDescription": "a thin lock pick lying on the ground",
        "takeable": True,
        "wearable": False,
        "onThrow": {
            "default": {
                "response": "You toss the lock pick onto the ground.",
                "destroyItem": False,
            },
        },
    },
)
