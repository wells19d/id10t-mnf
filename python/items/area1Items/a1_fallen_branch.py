a1_fallen_branch = (
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
        # "interactions": {
        #     "match": {
        #         "requires": {
        #             "targetOwnership": "currentLocation",
        #             "targetPlacement": "loose",
        #         },
        #         "effects": {
        #             "destroyTarget": True,
        #         },
        #         "targetLocationFailResponse": (
        #             "You need to put the branch on the ground before trying "
        #             "to set it on fire."
        #         ),
        #         "response": [
        #             {
        #                 "speaker": "narrator",
        #                 "text": (
        #                     "You strike a match and hold it beneath the fallen branch. "
        #                     "The dry wood catches, burns rapidly, and collapses into ash."
        #                 ),
        #             },
        #             {
        #                 "speaker": "voice",
        #                 "text": "Well... That was a bit of a waste of a match, but at least the branch is gone now.",
        #             },
        #         ],
        #     },
        #     "a1_disposable_lighter": {
        #         "requires": {
        #             "sourceItemStateMinimums": {
        #                 "usesRemaining": 1,
        #             },
        #             "targetOwnership": "currentLocation",
        #             "targetPlacement": "loose",
        #         },
        #         "effects": {
        #             "sourceItemStateDeltas": {
        #                 "usesRemaining": -1,
        #             },
        #             "destroyTarget": True,
        #         },
        #         "sourceStateFailResponse": (
        #             "The lighter clicks, but it is completely empty."
        #         ),
        #         "targetLocationFailResponse": (
        #             "You need to put the branch on the ground before trying "
        #             "to set it on fire."
        #         ),
        #         "response": [
        #             {
        #                 "speaker": "narrator",
        #                 "text": (
        #                     "You flick the lighter and hold its flame beneath the fallen "
        #                     "branch. The dry wood catches, burns rapidly, and collapses "
        #                     "into ash."
        #                 ),
        #             },
        #             {
        #                 "speaker": "voice",
        #                 "text": "Well... That was a bit of a waste of some lighter fluid, but at least the branch is gone now.",
        #             },
        #         ],
        #     },
        # },
        "onThrow": {
            "default": {
                "response": (
                    "You throw the branch. It spins through the air and drops into the grass."
                ),
                "destroyItem": False,
            },
        },
    },
)
