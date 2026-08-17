a1_matchbox_1 = (
    "a1_matchbox_1",
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
        "inspect": [
            {
                "speaker": "narrator",
                "text": (
                    "The small cardboard matchbox is worn around the edges, "
                    "with a faded striking strip along one side."
                ),
            },
            {
                "speaker": "voice",
                "text": "Still has a few matches left. Could be useful.",
            },
        ],
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
        "mergeOnTake": {
            "group": "matchbox",
            "stateKey": "matches",
        },
        "mergeResponse": (
            "You combine the matches into one box and discard the empty one "
            "to save space."
        ),
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
            "showInInventory": True,
            "requiresState": {
                "isOpen": True,
            },
        },
        "openResponse": "You slide the matchbox open.",
        "closeResponse": "You slide the matchbox closed.",
        "searchClosedResponse": "The matchbox is closed.",
        "searchEmptyResponse": "You inspect the open matchbox, but find it empty.",
        "onThrow": {
            "default": {
                "response": "You toss the matchbox onto the ground.",
                "destroyItem": False,
            },
        },
    },
)
