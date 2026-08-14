a1_massive_tree = {
    "name": "Massive Tree",
    "intro": [
        {
            "speaker": "narrator",
            "text": "",
        },
    ],
    "description": (
        "You stand in a clearing beside a Massive Tree, its thick trunk and branches spreading "
        "high overhead. The bark is rough, deeply grooved, and weathered gray with age. "
        "There's no direction to go except back the way you came."
    ),
    "items": [],
    "scenery": {
        "tree": {
            "aliases": [
                "massive tree",
                "tree",
            ],
            "description": (
                "Up close, the trunk is wide enough that your arms wouldn't reach halfway around it. "
                "Deep grooves run through the bark, and the lowest branches sit well out of reach."
            ),
            "takeFail": [
                {
                    "speaker": "narrator",
                    "text": (
                        "You can't take the massive tree with you. It's too large and deeply rooted in the ground."
                    ),
                },
                {
                    "speaker": "voice",
                    "text": "Sure, let me just tuck a forest into my pocket real quick.",
                },
            ],
            "items": ["a1_rusty_axe", "a1_wornout_work_gloves"],
            "searchable": False,
            "throwInteractions": {
                "a1_rusty_axe": {
                    "response": [
                        {
                            "speaker": "narrator",
                            "text": (
                                "You throw the axe. It embeds itself in the trunk."
                            ),
                        },
                        {
                            "speaker": "voice",
                            "text": "Well. That's one skill confirmed...",
                        },
                    ],
                },
            },
        },
    },
    "exits": {
        "north": False,
        "south": "a1_clearing",
        "east": False,
        "west": False,
    },
}
