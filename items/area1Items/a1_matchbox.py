a1_matchbox = (
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
)
