a1_wornout_work_gloves = (
    "a1_wornout_work_gloves",
    {
        "name": "Work Gloves",
        "aliases": [
            "work gloves",
            "gloves",
        ],
        "description": "A pair of heavily used, worn out work gloves.",
        "inspect": [
            {
                "speaker": "narrator",
                "text": "A pair of heavily used, worn out work gloves. They have several holes and rips, but they won't offer much protection.",
            },
            {
                "speaker": "voice",
                "text": "Well... they might still be useful for something...",
            },
        ],
        "worldDescription": (
            "a pair of worn out <em><span class='item-highlight'>work gloves</span></em> "
            "lying next to the tree base."
        ),
        "looseDescription": (
            "a pair of worn out <em><span class='item-highlight'>work gloves</span></em> "
            "lying on the ground."
        ),
        "takeable": True,
        "wearable": False,
        "wearFailResponse": [
            {
                "speaker": "narrator",
                "text": (
                    "You can't wear the "
                    "<em><span class='item-highlight'>Work Gloves</span></em>."
                ),
            },
            {
                "speaker": "voice",
                "text": "Right... Because massive holes and rips are exactly what protective gloves need.",
            },
        ],
        "onThrow": {
            "default": {
                "response": ("You toss the gloves onto the ground."),
                "destroyItem": False,
            },
        },
    },
)
