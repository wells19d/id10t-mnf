a1_wedding_ring = (
    "a1_wedding_ring",
    {
        "name": "Wedding Ring",
        "aliases": [
            "wedding ring",
            "man's wedding ring",
            "mans wedding ring",
            "ring",
        ],
        "description": (
            "A man's wedding ring. The fire left it undamaged, and a faint gold-colored "
            "luster still shows beneath the ash."
        ),
        "inspect": [
            {
                "speaker": "narrator",
                "text": (
                    "The man's wedding ring is plain and sturdy. It was not damaged by "
                    "the fire, and traces of its gold-colored luster remain."
                ),
            },
            {
                "speaker": "voice",
                "text": "Some things survive even when the memories around them don't.",
            },
        ],
        "worldDescription": (
            "a <em><span class='item-highlight'>wedding ring</span></em> "
            "glinting faintly through the ash."
        ),
        "looseDescription": (
            "a <em><span class='item-highlight'>wedding ring</span></em> "
            "lying on the ground."
        ),
        "takeable": True,
        "wearable": False,
        "flammable": False,
        "onThrow": {
            "default": {
                "response": "You toss the wedding ring onto the ground.",
                "destroyItem": False,
            },
        },
    },
)
