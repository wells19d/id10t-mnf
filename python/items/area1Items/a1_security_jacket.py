a1_security_jacket = (
    "a1_security_jacket",
    {
        "name": "Security Jacket",
        "aliases": ["security jacket", "jacket", "uniform jacket"],
        "description": "A dark security jacket with a faded facility patch.",
        "inspect": "The jacket is weathered but still recognizable as part of a security uniform.",
        "looseDescription": "a security jacket lying on the ground",
        "takeable": True,
        "wearable": True,
        "slot": "outerwear",
        "wearResponse": "You put on the Security Jacket.",
        "removeResponse": "You remove the Security Jacket.",
        "onThrow": {
            "default": {
                "response": "You toss the Security Jacket onto the ground.",
                "destroyItem": False,
            },
        },
    },
)
