a1_lake_south = {
    "name": "Lake (South)",
    "intro": [
        {
            "speaker": "narrator",
            "text": (
                "The trees thin along the southern shore of the same secluded "
                "<em><span class='area-highlight'>Lake (South)</span></em>. From here, the "
                "water opens northward between forested banks, reflecting the sky and "
                "the distant mountain ridge. Stones gathered into an old fire circle "
                "and a worn patch beneath the trees suggest another small campsite once "
                "occupied this end of the lake. The water along the shore is bitterly "
                "cold; swimming any distance in it would be unsafe. Paths lead south "
                "and east."
            ),
        },
    ],
    "description": (
        "The southern shore looks north across the "
        "<em><span class='area-highlight'>Lake (South)</span></em>, with dense forest wrapping "
        "around both banks. Signs of an abandoned campsite remain among the rocks. The "
        "water is clear but intensely cold, making swimming too dangerous to attempt. "
        "Paths lead south and east."
    ),
    "items": [],
    "scenery": {
        "lake": {
            "aliases": [
                "lake",
                "water",
                "lake water",
                "shore",
                "shoreline",
            ],
            "description": (
                "The lake spreads north from this shore, its surface dark beneath the "
                "reflection of the trees. The clear shallows are cold enough to make "
                "your hand ache within moments. Swimming would be dangerously impractical."
            ),
            "searchResponse": (
                "You examine the shallows along the southern shore, but the painfully "
                "cold water holds nothing worth reaching for."
            ),
            "interactions": {
                "a1_watering_can": {
                    "requires": {
                        "itemState": {
                            "liquidType": "empty",
                        },
                    },
                    "effects": {
                        "itemState": {
                            "liquidType": "water",
                        },
                    },
                    "failResponse": (
                        "The <em><span class='item-highlight'>Watering Can</span></em> "
                        "must be empty before you can fill it with lake water."
                    ),
                    "response": (
                        "You lower the <em><span class='item-highlight'>Watering Can</span></em> into the lake and fill it with cold, "
                        "clear water."
                    ),
                },
            },
        },
        "rocks": {
            "aliases": [
                "rocks",
                "shoreline rocks",
                "campsite",
                "old campsite",
            ],
            "description": (
                "The scattered shoreline rocks surround a faded fire mark and an area "
                "of flattened ground beneath the trees. Little remains of whoever once "
                "camped here."
            ),
            "searchable": True,
            "searchEmptyResponse": (
                "You search through the southern campsite rocks but find nothing else useful."
            ),
            "items": [
                "a1_pocket_knife",
            ],
            "itemDescriptions": {
                "a1_pocket_knife": (
                    "a weathered <em><span class='item-highlight'>pocket knife</span></em> "
                    "lodged between two shoreline rocks"
                ),
            },
        },
    },
    "exits": {
        "north": False,
        "south": "a1_fallen_nursery",
        "east": "a1_lake_east",
        "west": False,
    },
}
