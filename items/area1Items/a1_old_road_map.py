a1_old_road_map = (
    "a1_old_road_map",
    {
        "name": "Old Road Map",
        "aliases": ["old road map", "road map", "map"],
        "description": "A water-stained road map of the surrounding region.",
        "inspect": "Most markings have faded, though a security checkpoint is still visible near the edge.",
        "worldDescription": "an old road map snagged beneath roadside debris",
        "looseDescription": "an old road map lying on the ground",
        "takeable": True,
        "wearable": False,
        "onThrow": {
            "default": {
                "response": "You toss the old road map onto the ground.",
                "destroyItem": False,
            },
        },
    },
)
