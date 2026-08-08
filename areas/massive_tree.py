massive_tree = {
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
    "lookResponse": [
        {
            "speaker": "narrator",
            "text": (
                "You are standing in a clearing against a massive tree stretching high into the sky. "
                "no other direction to go except back the way you came."
            ),
        },
    ],
    # No loose items initially.
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
            "lookResponse": [
                {
                    "speaker": "narrator",
                    "text": (
                        "You look up at the massive tree, marveling at its size and age. "
                        "The branches seem to reach out in all directions, creating a canopy "
                        "that filters the sunlight."
                    ),
                },
            ],
            "takeFail": [
                {
                    "speaker": "narrator",
                    "text": (
                        "You can't take the massive tree with you. It's far too large and rooted "
                        "deeply in the ground."
                    ),
                },
            ],
            # The axe begins embedded in the tree.
            "items": [
                "a1_rusty_axe",
            ],
            "searchable": False,
            "throwInteractions": {
                "a1_rusty_axe": {
                    "response": (
                        "You throw the axe. With dumb luck, it sticks into the tree, "
                        "leaving it embedded in the trunk."
                    ),
                },
            },
        },
    },
    "exits": {
        "north": False,
        "south": "clearing",
        "east": False,
        "west": False,
    },
}
