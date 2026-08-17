a1_security_pants = (
    "a1_security_pants",
    {
        "name": "Security Pants",
        "aliases": ["security pants", "pants", "uniform pants", "trousers"],
        "description": "A pair of dark security-uniform pants.",
        "inspect": "The pants carry the same faded facility markings as the security jacket.",
        "looseDescription": "a pair of security pants lying on the ground",
        "takeable": True,
        "wearable": True,
        "slot": "legs",
        "wearResponse": "You put on the Security Pants.",
        "removeResponse": "You remove the Security Pants.",
        "onThrow": {
            "default": {
                "response": "You toss the Security Pants onto the ground.",
                "destroyItem": False,
            },
        },
    },
)
