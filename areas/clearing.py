clearing = {
    "name": "Clearing",
    "intro": [
        {"speaker": "voice", "text": "Hey, open your eyes..."},
        {
            "speaker": "narrator",
            "text": "You slowly open your eyes. At first, all you can see a blur of green and white light. You blink a few times and your vision begins to clear. The sun is shining through the leaves of the surrounding trees, with birds chirping in the distance. It appears to be about mid day. You find your self propped up against a large tree in a forest clearing.",
        },
        {"speaker": "voice", "text": "...What happened? Where am I? Who am I?"},
        {
            "speaker": "narrator",
            "text": "You slowly get to your feet when suddenly you feel a sharp pain in your head. You stumble back against the tree and place your hand on your forehead. You feel a small lump on the left side of your head, and you notice a small trickle of blood running down the side of your face.",
        },
        {
            "speaker": "voice",
            "text": "...oh, my head hurts... I feel dizzy... I can't remember anything...",
        },
        {
            "speaker": "narrator",
            "text": "Slowly the pain subsides, the dizziness fades, and you begin to take in your surroundings. You notice 4 small paths that lead out of the clearing. Each just look like other, with trampled patchy grass and dirt.",
        },
    ],
    "description": (
        "You are standing in a forest clearing. There are four narrow paths leading North, East, South, and West."
    ),
    "actions": {
        "jump": "You jump into the air and land exactly where you started.",
        "look at tree": "The tree behind you is broad and old, its bark rough beneath your hand.",
    },
    "items": [],
    "exits": {
        "north": "massive_tree",
        "south": "silent_grove",
        "east": "house_2",
        "west": "fallen_nursery",
    },
}
