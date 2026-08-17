a1_road_access = {
    "name": "Road Access",
    "intro": [{"speaker": "narrator", "text": "The forest opens onto a cracked access road choked by weeds and fallen branches. A security gate stands farther north."}],
    "description": "A narrow, deteriorating road cuts through the forest toward the Security Gate to the north. The red house lies to the west.",
    "items": ["a1_old_road_map"],
    "scenery": {
        "road": {
            "aliases": ["road", "access road", "roadside"],
            "description": "The old road is fractured by roots and years of neglect.",
            "searchResponse": "The road and surrounding brush offer little beyond the old map caught in the debris.",
        },
    },
    "exits": {
        "north": "a1_security_gate",
        "south": False,
        "east": False,
        "west": "a1_house_1",
    },
}
