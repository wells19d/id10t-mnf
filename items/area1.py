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
            "inspect": [
                {
                    "speaker": "narrator",
                    "text": "A simple tree branch. It could be used to start a fire.",
                },
                {
                    "speaker": "voice",
                    "text": "Nice... some kindling material. Now if only I had some way to light it...",
                },
            ],
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
                    "response": [
                        {
                            "speaker": "narrator",
                            "text": (
                                "You strike a match and hold it beneath the fallen branch. "
                                "The dry wood catches, burns rapidly, and collapses into ash."
                            ),
                        },
                        {
                            "speaker": "voice",
                            "text": "Well... That was a bit of a waste of a match, but at least the branch is gone now.",
                        },
                    ],
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
                    "response": [
                        {
                            "speaker": "narrator",
                            "text": (
                                "You flick the lighter and hold its flame beneath the fallen "
                                "branch. The dry wood catches, burns rapidly, and collapses "
                                "into ash."
                            ),
                        },
                        {
                            "speaker": "voice",
                            "text": "Well... That was a bit of a waste of some lighter fluid, but at least the branch is gone now.",
                        },
                    ],
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
            "inspect": [
                {
                    "speaker": "narrator",
                    "text": "A rusty axe. The blade is dulled and the handle is worn from years of use.",
                },
                {
                    "speaker": "voice",
                    "text": "It's seen better days, but it could still be useful...",
                },
            ],
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
            "inspect": [
                {
                    "speaker": "narrator",
                    "text": "A backpack with some wear and tear, but it still appears to be in fair condition.",
                },
                {
                    "speaker": "voice",
                    "text": "I bet we could still use it. It looks like it could still hold a decent amount of <em><span class='item-highlight'>items</span></em>",
                },
            ],
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
                "brass key",
                "key",
            ],
            "description": "A tarnished brass key.",
            "inspect": [
                {
                    "speaker": "narrator",
                    "text": "A tarnished, old fashioned, brass key. It looks sturdy enough to still work...",
                },
                {
                    "speaker": "voice",
                    "text": "This could come in handy. I wonder what it unlocks...",
                },
            ],
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
