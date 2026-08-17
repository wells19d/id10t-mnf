a1_fallen_nursery = {
    "name": "Fallen Nursery",
    "intro": [
        {
            "speaker": "narrator",
            "text": (
                "A massive fallen tree dominates the edge of the "
                "<em><span class='area-highlight'>Fallen Nursery</span></em>, "
                "its trunk covered in moss, ferns, and other new growth. Much of it has begun to sink "
                "into the forest floor, while broken limbs and exposed wood disappear beneath the vegetation. "
                "The remains of the tree stretch deep into the surrounding forest, making passage around "
                "the western side impossible. Worn paths lead north, south, and east."
            ),
        },
    ],
    "description": (
        "A massive fallen tree stretches along the edge of the "
        "<em><span class='area-highlight'>Fallen Nursery</span></em>, "
        "blocking passage to the west. Worn paths lead north, south, and east."
    ),
    "items": [],
    "scenery": {
        "tree": {
            "aliases": ["fallen tree", "tree"],
            "description": (
                "It's a massive tree covered in moss, ferns, and other growth. "
                "It spans the western edge of the area, making passage around it impossible."
            ),
            "takeFail": [
                {
                    "speaker": "narrator",
                    "text": (
                        "You can't take the tree, it's far too large to be moved."
                    ),
                },
                {
                    "speaker": "voice",
                    "text": "...Sure, let me just tuck the entire forest into my pocket real quick.",
                },
            ],
            "items": ["a1_watering_can", "a1_wild_mushrooms"],
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
                "a1_watering_can": {
                    "response": [
                        {
                            "speaker": "narrator",
                            "text": (
                                "You throw the watering can. Bouncing off the mossy bark, "
                                "it lands on the ground with a dull thud."
                            ),
                        },
                        {
                            "speaker": "voice",
                            "text": "Well. That was productive...",
                        },
                    ],
                },
                "a1_wild_mushrooms": {
                    "response": [
                        {
                            "speaker": "narrator",
                            "text": (
                                "You throw the wild mushrooms at the tree. They bounce off and scatter slightly."
                            ),
                        },
                        {
                            "speaker": "voice",
                            "text": "...FOOD FIGHT! Where's the mashed potatoes?!",
                        },
                    ],
                },
            },
        }
    },
    "exits": {
        "north": "a1_lake_south",
        "south": "a1_house_3",
        "east": "a1_clearing",
        "west": False,
    },
}
