a1_replacement_fuse = (
    "a1_replacement_fuse",
    {
        "name": "Replacement Fuse",
        "aliases": ["replacement fuse", "fuse"],
        "description": "A heavy replacement fuse sized for an industrial electrical panel.",
        "inspect": "The fuse looks unused and matches the kind fitted in old security equipment.",
        "looseDescription": "a replacement fuse lying on the ground",
        "takeable": True,
        "wearable": False,
        "onThrow": {
            "default": {
                "response": "You carefully set the replacement fuse on the ground.",
                "destroyItem": False,
            },
        },
    },
)
