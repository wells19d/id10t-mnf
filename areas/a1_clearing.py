a1_clearing = {
    "name": "Grassy Clearing",
    "intro": [
        {
            "speaker": "voice",
            "text": "Come on... get up!",
        },
        {
            "speaker": "narrator",
            "text": (
                "As your eyes open, sunlight filters through the leaves overhead. You blink until your "
                "vision clears. You're sitting against a large tree at the edge of a "
                "<em><span class='area-highlight'>Grassy Clearing</span></em>, surrounded by thick forest. "
                "Birds call somewhere among the trees."
            ),
        },
        {
            "speaker": "narrator",
            "text": (
                "In the middle of the clearing, a sword is driven into a large, moss-covered stone, "
                "ferns growing thick around its base. Several worn paths lead away from the clearing, "
                "heading North, South, East, and West."
            ),
        },
        {
            "speaker": "narrator",
            "text": (
                "As you push yourself up, a dull pain hits the left side of your head. You reach up "
                "and find a small lump, with a thin trickle of blood running down your face."
            ),
        },
        {
            "speaker": "voice",
            "text": "What happened?",
        },
        {
            "speaker": "narrator",
            "text": (
                "You search your memory, but nothing comes back. No clear image. No familiar voice. No sense "
                "of where you were before this. Reaching for something as simple as your own name yields nothing."
            ),
        },
        {
            "speaker": "voice",
            "text": (
                "...I don’t remember. Maybe I should "
                "<span class='command-highlight'>look</span> around and "
                "<span class='command-highlight'>search</span> for answers."
            ),
        },
    ],
    "description": (
        "You are standing in a <em><span class='area-highlight'>Grassy Clearing</span></em> surrounded by thick forest. "
        "Sunlight shines through the trees above. A sword is driven into a "
        "moss-covered stone in the middle of the clearing. Worn paths lead "
        "North, South, East, and West."
    ),
    "items": ["a1_fallen_branch"],
    "scenery": {
        "sword": {
            "aliases": ["sword", "old sword", "stuck sword"],
            "description": (
                "A sword is buried to the hilt in the ground near the tree roots, blade down. "
                "The metal is dull and pitted with rust. It hasn't moved in a long time."
            ),
            "takeFail": [
                {
                    "speaker": "narrator",
                    "text": "You grip the hilt and pull. The sword doesn't move.",
                },
                {
                    "speaker": "voice",
                    "text": "Okay, I'm not the chosen one. Good to know.",
                },
            ],
            "searchable": False,
        },
    },
    "exits": {
        "north": "a1_massive_tree",
        "south": "a1_silent_grove",
        "east": "a1_house_2",
        "west": "a1_fallen_nursery",
    },
}
