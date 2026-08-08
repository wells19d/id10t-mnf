clearing = {
    "name": "Clearing",
    "intro": [
        {
            "speaker": "voice",
            "text": "Come on... get up!",
        },
        {
            "speaker": "narrator",
            "text": (
                "As your eyes slowly open, bright sunlight filters through the green leaves "
                "above you. You blink a few times as your vision clears. You are sitting "
                "against a large tree at the edge of a grassy clearing, surrounded by thick forest. "
                "Birds call from somewhere among the trees, and a light breeze moves through the leaves. "
                "Several worn paths lead away from the clearing."
            ),
        },
        {
            "speaker": "narrator",
            "text": (
                "As you push yourself to your feet, a dull pain hits the left side of your "
                "head. You reach up and feel a small lump on the side of your head, with a thin "
                "trickle of blood running down your face."
            ),
        },
        {
            "speaker": "voice",
            "text": "What happened?",
        },
        {
            "speaker": "narrator",
            "text": (
                "You search your memory, but nothing comes back. No clear image. "
                "No familiar voice. No sense of where you were before this. You reach "
                "for something as simple as your own name and find nothing."
            ),
        },
        {
            "speaker": "voice",
            "text": (
                "...I don't remember. Maybe I should "
                "<span class='command-highlight'>look</span> around and "
                "<span class='command-highlight'>search</span> for answers."
            ),
        },
    ],
    "description": (
        "You are standing in a grassy clearing surrounded by thick forest. "
        "Sunlight shines through the trees above. Worn paths lead north, south, "
        "east, and west."
    ),
    "items": [
        "a1_fallen_branch",
    ],
    "scenery": {},
    "exits": {
        "north": "massive_tree",
        "south": "silent_grove",
        "east": "house_2",
        "west": "fallen_nursery",
    },
}
