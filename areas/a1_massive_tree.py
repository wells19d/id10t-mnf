a1_massive_tree = {
    "name": "Massive Tree",
    "intro": [
        {
            "speaker": "narrator",
            "text": "",
        },
    ],
    "description": (
        "You are standing in a clearing against a massive tree, its thick trunk and sprawling branches "
        "stretching high into the sky. The bark is rough and weathered, and the "
        "leaves rustle gently in the breeze. There appears to be "
        "no other direction to go except back the way you came."
    ),
    "items": [],
    "scenery": {
        "tree": {
            "aliases": [
                "massive tree",
                "tree",
            ],
            "description": (
                "A massive tree towers above you, its thick trunk and sprawling branches "
                "stretching high into the sky. The bark is rough and weathered, and the "
                "leaves rustle gently in the breeze."
            ),
            "takeFail": [
                {
                    "speaker": "narrator",
                    "text": (
                        "You can't take the massive tree with you. It's far too large and rooted "
                        "deeply in the ground."
                    ),
                },
                {
                    "speaker": "voice",
                    "text": (
                        "...really? You think you can just pick up massive trees now?"
                    ),
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
                                "You throw the axe. With dumb luck, it sticks into the tree, "
                                "leaving it embedded in the trunk."
                            ),
                        },
                        {
                            "speaker": "voice",
                            "text": "Well... that worked.",
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
