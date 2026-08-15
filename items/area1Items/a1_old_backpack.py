a1_old_backpack = (
    "a1_old_backpack",
    {
        "name": "FSS Backpack",
        "aliases": [
            "fss backpack",
            "backpack",
            "old pack",
            "old bag",
        ],
        "description": (
            "An old canvas <em><span  class='equipment-highlight'>FSS backpack</span></em>, faded and worn from years of use. "
            "The fabric is scuffed and dirty, and the leather straps are cracked with age."
        ),
        "inspect": [
            {
                "speaker": "narrator",
                "text": (
                    "The old canvas backpack is faded and worn, but the fabric is still intact. "
                    "Its leather straps are cracked with age, though the main shoulder straps remain sturdy enough to use."
                ),
            },
            {
                "speaker": "voice",
                "text": (
                    "Still usable... This should let me carry a few more "
                    "<em><span class='item-highlight'>items</span></em>."
                ),
            },
        ],
        "worldDescription": (
            "an old <em><span class='equipment-highlight'>FSS backpack</span></em> "
            "lying on the ground beside the base of a large tree."
        ),
        "looseDescription": (
            "an old <em><span class='equipment-highlight'>FSS backpack</span></em> "
            "lying on the ground."
        ),
        "takeable": True,
        "wearable": True,
        "flammable": False,
        "slot": "back",
        "carryCapacity": 10,
        "container": True,
        "searchable": True,
        "contentsRequireSearch": True,
        "transferContentsOnTake": True,
        "state": {
            "isSearched": False,
        },
        "takeResponse": (
            "You take the <em><span class='equipment-highlight'>FSS Backpack</span></em> "
            "and move everything still inside it into your general inventory."
        ),
        "wearResponse": [
            {
                "speaker": "narrator",
                "text": (
                    "You've equipped the "
                    "<em><span class='equipment-highlight'>FSS Backpack</span></em>. "
                    "The world feels lighter now, as you can carry more items."
                ),
            },
            {
                "speaker": "voice",
                "text": '*Sings* "<em>Lay your world on me... I can take the weight.</em>"',
            },
        ],
        "takeWearResponse": [
            {
                "speaker": "narrator",
                "text": (
                    "You've taken and equipped the "
                    "<em><span class='equipment-highlight'>FSS Backpack</span></em>. "
                    "You combine its contents with your own, giving you more room to carry items."
                ),
            },
            {
                "speaker": "voice",
                "text": (
                    "*Sings* "
                    "<em>I'll lay my world on you... "
                    "Yeah, that's right, backpack. You can take the weight.</em>"
                ),
            },
        ],
        "searchEmptyResponse": "You search the backpack but find it empty.",
        "onThrow": {
            "default": {
                "response": "You throw the empty backpack onto the ground.",
                "destroyItem": False,
            },
        },
    },
)
