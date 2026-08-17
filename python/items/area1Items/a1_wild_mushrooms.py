a1_wild_mushrooms = (
    "a1_wild_mushrooms",
    {
        "name": "Wild Mushrooms",
        "aliases": [
            "wild mushrooms",
            "mushrooms",
            "fungi",
        ],
        "description": "A cluster of <em><span class='item-highlight'>wild mushrooms</span></em>",
        "inspect": [
            {
                "speaker": "narrator",
                "text": "A cluster of wild mushrooms. They look like they could be edible...",
            },
            {
                "speaker": "voice",
                "text": "...maybe with proper research, they could be poisonous.",
            },
        ],
        "worldDescription": (
            "a cluster of <em><span class='item-highlight'>wild mushrooms</span></em> "
            "growing wildly along the edge of the fallen tree."
        ),
        "looseDescription": (
            "a cluster of <em><span class='item-highlight'>wild mushrooms</span></em> "
            "lying on the ground."
        ),
        "takeable": True,
        "wearable": False,
        "flammable": False,
        "interactions": {},
        "onThrow": {
            "default": {
                "response": (
                    "You toss the wild mushrooms onto the ground. They scatter slightly."
                ),
                "destroyItem": False,
            },
        },
    },
)
