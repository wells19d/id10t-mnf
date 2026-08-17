a1_security_hat = (
    "a1_security_hat",
    {
        "name": "Security Hat",
        "aliases": ["security hat", "hat", "cap"],
        "description": "A faded security-service cap.",
        "inspect": "The cap bears the worn emblem of the facility security staff.",
        "looseDescription": "a faded security hat lying on the ground",
        "takeable": True,
        "wearable": True,
        "slot": "head",
        "wearResponse": "You put on the Security Hat.",
        "removeResponse": "You remove the Security Hat.",
        "onThrow": {
            "default": {
                "response": "You toss the Security Hat onto the ground.",
                "destroyItem": False,
            },
        },
    },
)
