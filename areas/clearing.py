clearing = {
    "name": "Clearing",
    "intro": [
        {
            "speaker": "voice",
            "text": "Hey, open your eyes...",
        },
        {
            "speaker": "narrator",
            "text": (
                "You slowly open your eyes. At first, all you can see "
                "is a blur of green and white light. You blink a few "
                "times and your vision begins to clear. The sun is "
                "shining through the leaves of the surrounding trees, "
                "with birds chirping in the distance. It appears to be "
                "about midday. You find yourself propped against a "
                "large tree in a forest clearing."
            ),
        },
        {
            "speaker": "voice",
            "text": "...What happened? Where am I? Who am I?",
        },
        {
            "speaker": "narrator",
            "text": (
                "You slowly get to your feet when a sharp pain suddenly "
                "cuts through your head. You stumble back against the "
                "tree and place your hand on your forehead. You feel a "
                "small lump on the left side of your head and notice a "
                "thin trickle of blood running down your face."
            ),
        },
        {
            "speaker": "voice",
            "text": (
                "...My head hurts. I feel dizzy... " "I can't remember anything..."
            ),
        },
        {
            "speaker": "narrator",
            "text": (
                "Slowly, the pain subsides and the dizziness fades. "
                "You begin to take in your surroundings. Four small "
                "paths lead out of the clearing, each marked by "
                "trampled grass and exposed dirt."
            ),
        },
    ],
    "description": (
        "You are standing in a forest clearing. Four narrow paths "
        "lead North, East, South, and West."
    ),
    "lookResponse": [
        {
            "speaker": "narrator",
            "text": (
                "You are standing in a forest clearing. Four narrow "
                "paths lead North, East, South, and West."
            ),
        },
        {
            "speaker": "voice",
            "text": "One of these paths has to lead somewhere useful.",
        },
    ],
    # "searchVoice": {
    #     "speaker": "voice",
    #     "text": "This place is stranger than it first appeared.",
    # },
    "itemDescriptions": {
        "a1_rusty_axe": {
            "name": "Rusty Axe",
            "description": (
                "A rusty axe with a worn wooden handle. "
                "The blade is dull and chipped."
            ),
            "lookResponse": [
                {
                    "speaker": "narrator",
                    "text": (
                        "The rusty axe has a worn wooden handle. "
                        "Its blade is dull and badly chipped."
                    ),
                },
                {
                    "speaker": "voice",
                    "text": "Useful, assuming the handle survives.",
                },
            ],
        },
        "a1_golden_axe": {
            "name": "Golden Axe",
            "description": (
                "A golden axe with a sturdy wooden handle. "
                "The blade is sharp and shiny."
            ),
            "lookResponse": [
                {
                    "speaker": "narrator",
                    "text": (
                        "The golden axe has a sturdy wooden handle "
                        "and a polished, sharply honed blade."
                    ),
                },
                {
                    "speaker": "voice",
                    "text": "A golden axe. Completely normal.",
                },
            ],
        },
        "a1_silver_axe": {
            "name": "Silver Axe",
            "description": (
                "A silver axe with a sturdy wooden handle. "
                "The blade is sharp and shiny."
            ),
            "lookResponse": [
                {
                    "speaker": "narrator",
                    "text": (
                        "The silver axe has a sturdy wooden handle. "
                        "Its bright blade reflects the surrounding trees."
                    ),
                },
                {
                    "speaker": "voice",
                    "text": "Someone had very specific taste in axes.",
                },
            ],
        },
        "a1_silver_key": {
            "name": "Silver Key",
            "description": "A small silver key.",
            "lookResponse": [
                {
                    "speaker": "narrator",
                    "text": (
                        "The small silver key is lightly tarnished. "
                        "There are no markings on it."
                    ),
                },
                {
                    "speaker": "voice",
                    "text": "Now I just need to find what it opens.",
                },
            ],
        },
    },
    "scenery": {
        "sword": {
            "aliases": [
                "sword",
                "rusty sword",
                "blade",
            ],
            "description": ("A rusty sword is firmly stuck in the ground."),
            "lookResponse": [
                {
                    "speaker": "narrator",
                    "text": (
                        "The sword is deeply embedded in the ground. "
                        "Rust covers most of the blade, and its worn "
                        "handle leans slightly to one side."
                    ),
                },
                {
                    "speaker": "voice",
                    "text": "Someone went to a lot of trouble to leave that there.",
                },
            ],
            "takeFail": [
                {
                    "speaker": "narrator",
                    "text": (
                        "You wrap both hands around the sword and pull, "
                        "but it remains firmly stuck in the ground."
                    ),
                },
                {
                    "speaker": "voice",
                    "text": "Apparently I am not the chosen one.",
                },
            ],
        },
        "tree": {
            "aliases": [
                "tree",
                "oak",
                "trunk",
            ],
            "description": ("A broad tree stands beside the western path."),
            "lookResponse": [
                {
                    "speaker": "narrator",
                    "text": (
                        "The tree is broad and old. Deep grooves run "
                        "through its rough bark, and several axe blades "
                        "have been driven into its trunk."
                    ),
                },
                {
                    "speaker": "voice",
                    "text": "This tree has had a difficult day.",
                },
            ],
            "searchable": True,
            "searchResponse": [
                {
                    "speaker": "narrator",
                    "text": (
                        "You inspect the tree and the objects embedded " "in its trunk."
                    ),
                },
                {
                    "speaker": "voice",
                    "text": "Three axes in one tree. That seems excessive.",
                },
            ],
            "itemPrefix": "Firmly stuck in it:",
            "hideOnEmpty": True,
            "items": [
                "a1_rusty_axe",
                "a1_golden_axe",
                "a1_silver_axe",
            ],
        },
        "cupboard": {
            "aliases": [
                "cupboard",
                "cabinet",
            ],
            "description": (
                "Very oddly, a small wooden cupboard has been mounted "
                "against a tree."
            ),
            "lookResponse": [
                {
                    "speaker": "narrator",
                    "text": (
                        "The small wooden cupboard is securely mounted "
                        "against the tree. Its door is fitted with a "
                        "simple metal handle."
                    ),
                },
                {
                    "speaker": "voice",
                    "text": "A cupboard. On a tree. Of course.",
                },
            ],
            "searchable": True,
            "openable": True,
            "closeable": True,
            "hideOnEmpty": True,
            "openResponse": [
                {
                    "speaker": "narrator",
                    "text": "You pull the handle and open the cupboard.",
                },
                {
                    "speaker": "voice",
                    "text": "At least it wasn't locked.",
                },
            ],
            "alreadyOpenResponse": [
                {
                    "speaker": "narrator",
                    "text": "The cupboard is already open.",
                },
                {
                    "speaker": "voice",
                    "text": "Opening it again probably won't make it more open.",
                },
            ],
            "closeResponse": [
                {
                    "speaker": "narrator",
                    "text": "You close the cupboard door.",
                },
                {
                    "speaker": "voice",
                    "text": "Problem successfully concealed.",
                },
            ],
            "alreadyClosedResponse": [
                {
                    "speaker": "narrator",
                    "text": "The cupboard is already closed.",
                },
                {
                    "speaker": "voice",
                    "text": "It remains impressively closed.",
                },
            ],
            "searchClosedResponse": [
                {
                    "speaker": "narrator",
                    "text": (
                        "You examine the cupboard, but its closed door "
                        "blocks your view of the inside."
                    ),
                },
                {
                    "speaker": "voice",
                    "text": "Opening it might improve the search.",
                },
            ],
            "searchResponse": [
                {
                    "speaker": "narrator",
                    "text": "You search inside the open cupboard.",
                },
                {
                    "speaker": "voice",
                    "text": "Let's see what someone thought belonged in a tree.",
                },
            ],
            "searchEmptyResponse": [
                {
                    "speaker": "narrator",
                    "text": "You search the cupboard but find nothing inside.",
                },
                {
                    "speaker": "voice",
                    "text": "An empty cupboard attached to a tree. Somehow worse.",
                },
            ],
            "items": [
                "a1_silver_key",
            ],
        },
    },
    "exits": {
        "north": "massive_tree",
        "south": "silent_grove",
        "east": "house_2",
        "west": "fallen_nursery",
    },
}
