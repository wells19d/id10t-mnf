a1_pocket_knife = (
    "a1_pocket_knife",
    {
        "name": "Pocket Knife",
        "aliases": [
            "pocket knife",
            "folding knife",
            "knife",
        ],
        "description": (
            "A weathered folding pocket knife with its blade tucked safely into the handle."
        ),
        "inspect": [
            {
                "speaker": "narrator",
                "text": (
                    "The pocket knife has a scratched metal handle and a stiff folding "
                    "blade. It is worn, but still sturdy enough to be useful."
                ),
            },
            {
                "speaker": "voice",
                "text": "Small, sharp, and portable. Finally, something practical.",
            },
        ],
        "worldDescription": (
            "a weathered <em><span class='item-highlight'>pocket knife</span></em> "
            "lodged between two shoreline rocks."
        ),
        "looseDescription": (
            "a weathered <em><span class='item-highlight'>pocket knife</span></em> "
            "lying on the ground."
        ),
        "takeable": True,
        "wearable": False,
        "flammable": False,
        "onThrow": {
            "default": {
                "response": "You toss the pocket knife onto the ground.",
                "destroyItem": False,
            },
        },
    },
)
