area1Items = [
    (
        "a1_fallen_branch",
        {
        "name": "Fallen Branch",
        "aliases": [
            "fallen branch",
            "branch",
            "stick",
        ],
        "description": "A fallen branch from a nearby tree.",
        "worldDescription": (
            "a <em><span class='item-highlight'>fallen branch</span></em> "
            "lying on the ground."
        ),
        "looseDescription": (
            "a <em><span class='item-highlight'>fallen branch</span></em> "
            "lying on the ground."
        ),
        "takeable": True,
        "wearable": False,
        "onThrow": {
            "default": {
                "response": (
                    "You throw the branch. It spins through the air and drops into the grass."
                ),
                "destroyItem": False,
            },
        },
        },
    ),
    (
        "a1_rusty_axe",
        {
        "name": "Rusty Axe",
        "aliases": [
            "rusty axe",
            "axe",
            "hatchet",
        ],
        "description": "A rusty axe with a worn wooden handle.",
        "worldDescription": (
            "a <em><span class='item-highlight'>rusty axe</span></em> "
            "embedded into the base of the massive tree, its blade dulled and handle worn from years of use."
        ),
        "looseDescription": (
            "a <em><span class='item-highlight'>rusty axe</span></em> "
            "lying on the ground."
        ),
        "takeable": True,
        "wearable": False,
        "onThrow": {
            "default": {
                "response": (
                    "You throw the axe. It spins through the air and drops to the ground."
                ),
                "destroyItem": False,
            },
        },
        },
    ),
    (
        "a1_wornout_work_gloves",
        {
        "name": "Work Gloves",
        "aliases": [
            "work gloves",
            "gloves",
        ],
        "description": "A pair of heavily used, worn out work gloves with holes and tears.",
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
    ),
]
