a1_flashlight = (
    "a1_flashlight",
    {
        "name": "Flashlight",
        "aliases": ["flashlight", "torch"],
        "description": "A sturdy flashlight with no batteries.",
        "inspect": "The flashlight appears intact, but its battery compartment is empty.",
        "looseDescription": "a batteryless flashlight lying on the ground",
        "takeable": True,
        "wearable": False,
        "onThrow": {
            "default": {
                "response": "You toss the flashlight onto the ground.",
                "destroyItem": False,
            },
        },
    },
)
