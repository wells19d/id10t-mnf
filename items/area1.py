area1Items = [
    (
        "a1_light_blue_dress_shirt",
        {
            "name": "Light Blue Dress Shirt",
            "aliases": [
                "light blue dress shirt",
                "blue dress shirt",
                "dress shirt",
                "shirt",
            ],
            "description": (
                "A light blue dress shirt, rumpled and marked with the dirt "
                "of the forest floor."
            ),
            "looseDescription": (
                "a <em><span class='equipment-highlight'>light blue dress shirt</span></em> "
                "lying on the ground."
            ),
            "takeable": True,
            "wearable": True,
            "slot": "chest",
            "onThrow": {
                "default": {
                    "response": (
                        "You throw the shirt. It lands in a rumpled heap on the ground."
                    ),
                    "destroyItem": False,
                },
            },
        },
    ),
    (
        "a1_loose_fit_blue_jeans",
        {
            "name": "Loose-Fit Blue Jeans",
            "aliases": [
                "loose-fit blue jeans",
                "loose fit blue jeans",
                "blue jeans",
                "jeans",
                "pants",
            ],
            "description": (
                "A pair of loose-fit blue jeans, worn soft and streaked with dirt."
            ),
            "looseDescription": (
                "a pair of <em><span class='equipment-highlight'>loose-fit blue jeans</span></em> "
                "lying on the ground."
            ),
            "takeable": True,
            "wearable": True,
            "slot": "legs",
            "onThrow": {
                "default": {
                    "response": (
                        "You throw the jeans. They land in a crumpled heap on the ground."
                    ),
                    "destroyItem": False,
                },
            },
        },
    ),
    (
        "a1_grey_casual_shoes",
        {
            "name": "Grey Casual Shoes",
            "aliases": [
                "grey casual shoes",
                "gray casual shoes",
                "casual shoes",
                "grey shoes",
                "gray shoes",
                "shoes",
            ],
            "description": (
                "A pair of grey casual shoes, scuffed and dusted with dry soil."
            ),
            "looseDescription": (
                "a pair of <em><span class='equipment-highlight'>grey casual shoes</span></em> "
                "lying on the ground."
            ),
            "takeable": True,
            "wearable": True,
            "slot": "feet",
            "onThrow": {
                "default": {
                    "response": ("You throw the shoes. They tumble to the ground."),
                    "destroyItem": False,
                },
            },
        },
    ),
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
