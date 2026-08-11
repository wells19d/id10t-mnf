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
            "flammable": True,
            "interactions": {
                "match": {
                    "requires": {
                        "targetOwnership": "currentLocation",
                        "targetPlacement": "loose",
                    },
                    "effects": {
                        "destroyTarget": True,
                    },
                    "targetLocationFailResponse": (
                        "You need to put the branch on the ground before trying "
                        "to set it on fire."
                    ),
                    "response": (
                        "You strike a match and hold it beneath the fallen branch. "
                        "The dry wood catches, burns rapidly, and collapses into ash."
                    ),
                },
                "a1_disposable_lighter": {
                    "requires": {
                        "sourceItemStateMinimums": {
                            "usesRemaining": 1,
                        },
                        "targetOwnership": "currentLocation",
                        "targetPlacement": "loose",
                    },
                    "effects": {
                        "sourceItemStateDeltas": {
                            "usesRemaining": -1,
                        },
                        "destroyTarget": True,
                    },
                    "sourceStateFailResponse": (
                        "The lighter clicks, but it is completely empty."
                    ),
                    "targetLocationFailResponse": (
                        "You need to put the branch on the ground before trying "
                        "to set it on fire."
                    ),
                    "response": (
                        "You flick the lighter and hold its flame beneath the fallen "
                        "branch. The dry wood catches, burns rapidly, and collapses "
                        "into ash."
                    ),
                },
            },
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
            "description": "A pair of heavily used, worn out work gloves with holes and tears. They are practically useless for any protection.",
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
    (
        "a1_backpack",
        {
            "name": "Backpack",
            "aliases": [
                "backpack",
                "pack",
                "bag",
            ],
            "description": (
                "A weathered canvas backpack with several faded patches and "
                "surprisingly sturdy straps."
            ),
            "worldDescription": (
                "a weathered <em><span class='equipment-highlight'>backpack</span></em> "
                "resting against a tree."
            ),
            "looseDescription": (
                "a weathered <em><span class='equipment-highlight'>backpack</span></em> "
                "lying on the ground."
            ),
            "takeable": True,
            "wearable": True,
            "slot": "back",
            "carryCapacity": 5,
            "container": True,
            "searchable": True,
            "contentsRequireSearch": True,
            "transferContentsOnTake": True,
            "state": {
                "isSearched": False,
            },
            "takeResponse": (
                "You take the <em><span class='equipment-highlight'>Backpack</span></em> "
                "and move everything still inside it into your general inventory."
            ),
            "searchEmptyResponse": "You search the backpack but find it empty.",
            "onThrow": {
                "default": {
                    "response": "You throw the empty backpack onto the ground.",
                    "destroyItem": False,
                },
            },
        },
    ),
    (
        "a1_house_key",
        {
            "name": "House Key",
            "aliases": [
                "house key",
                "key",
            ],
            "description": (
                "A tarnished brass key stamped with the outline of a small house."
            ),
            "looseDescription": (
                "a tarnished <em><span class='item-highlight'>house key</span></em> "
                "lying on the ground."
            ),
            "takeable": True,
            "wearable": False,
            "onThrow": {
                "default": {
                    "response": "You toss the house key onto the ground.",
                    "destroyItem": False,
                },
            },
        },
    ),
    (
        "a1_rain_poncho",
        {
            "name": "Old Rain Poncho",
            "aliases": [
                "old rain poncho",
                "rain poncho",
                "poncho",
            ],
            "description": (
                "A thin, faded rain poncho that smells faintly of damp canvas."
            ),
            "looseDescription": (
                "an old <em><span class='equipment-highlight'>rain poncho</span></em> "
                "lying on the ground."
            ),
            "takeable": True,
            "wearable": True,
            "slot": "outerwear",
            "onThrow": {
                "default": {
                    "response": "You toss the rain poncho onto the ground.",
                    "destroyItem": False,
                },
            },
        },
    ),
    (
        "a1_matchbox",
        {
            "name": "Matchbox",
            "aliases": [
                "matchbox",
                "box of matches",
                "matches",
            ],
            "description": (
                "A small cardboard matchbox with a worn striking strip along one side."
            ),
            "worldDescription": (
                "a small <em><span class='item-highlight'>matchbox</span></em> "
                "lying between two stones."
            ),
            "looseDescription": (
                "a small <em><span class='item-highlight'>matchbox</span></em> "
                "lying on the ground."
            ),
            "takeable": True,
            "wearable": False,
            "searchable": True,
            "openable": True,
            "closeable": True,
            "state": {
                "isOpen": False,
                "matches": 3,
            },
            "providedUses": {
                "match": {
                    "aliases": [
                        "match",
                    ],
                    "requiresState": {
                        "isOpen": True,
                    },
                    "resource": {
                        "stateKey": "matches",
                        "minimum": 1,
                        "consume": 1,
                    },
                    "failResponse": (
                        "The matchbox must be open and contain at least one match."
                    ),
                    "targetDefinitionRequires": {
                        "flammable": True,
                    },
                },
            },
            "quantityDisplay": {
                "stateKey": "matches",
                "singular": "match",
                "plural": "matches",
                "requiresState": {
                    "isOpen": True,
                },
            },
            "openResponse": "You slide the matchbox open.",
            "closeResponse": "You slide the matchbox closed.",
            "searchClosedResponse": "The matchbox is closed.",
            "searchEmptyResponse": "You inspect the open matchbox.",
            "onThrow": {
                "default": {
                    "response": "You toss the matchbox onto the ground.",
                    "destroyItem": False,
                },
            },
        },
    ),
    (
        "a1_disposable_lighter",
        {
            "name": "Disposable Lighter",
            "aliases": [
                "disposable lighter",
                "lighter",
            ],
            "description": (
                "A cheap plastic lighter. Its translucent body reveals very little "
                "fuel, though there is no reliable way to judge how much remains."
            ),
            "worldDescription": (
                "a scratched <em><span class='item-highlight'>disposable lighter</span></em> "
                "lying near the water's edge."
            ),
            "looseDescription": (
                "a scratched <em><span class='item-highlight'>disposable lighter</span></em> "
                "lying on the ground."
            ),
            "takeable": True,
            "wearable": False,
            "state": {
                "usesRemaining": 5,
            },
            "targetDefinitionRequires": {
                "flammable": True,
            },
            "onThrow": {
                "default": {
                    "response": "You toss the lighter onto the ground.",
                    "destroyItem": False,
                },
            },
        },
    ),
]
