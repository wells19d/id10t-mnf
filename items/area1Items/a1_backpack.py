a1_backpack = (
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
)
