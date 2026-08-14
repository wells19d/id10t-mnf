a1_disposable_lighter = (
    "a1_disposable_lighter",
    {
        "name": "Disposable Lighter",
        "aliases": [
            "disposable lighter",
            "lighter",
        ],
        "description": (
            "A cheap plastic lighter. Its translucent body reveals very little "
            "fuel, though there is no reliable way to judge how much remains."
        ),
        "worldDescription": (
            "a scratched <em><span class='item-highlight'>disposable lighter</span></em> "
            "lying near the water's edge."
        ),
        "looseDescription": (
            "a scratched <em><span class='item-highlight'>disposable lighter</span></em> "
            "lying on the ground."
        ),
        "takeable": True,
        "wearable": False,
        "state": {
            "usesRemaining": 5,
        },
        "targetDefinitionRequires": {
            "flammable": True,
        },
        "onThrow": {
            "default": {
                "response": "You toss the lighter onto the ground.",
                "destroyItem": False,
            },
        },
    },
)
