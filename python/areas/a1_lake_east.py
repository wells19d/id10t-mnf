a1_lake_east = {
    "name": "Lake (East)",
    "intro": [
        {
            "speaker": "narrator",
            "text": (
                "The path reaches the eastern shore of a secluded "
                "<em><span class='area-highlight'>Lake (East)</span></em>, where clear, "
                "dark water stretches west beneath the surrounding pines. Beyond the "
                "far shore, a broken mountain ridge rises above the forest. A flattened "
                "patch of ground and a rough circle of blackened stones suggest this "
                "rocky spot once served as a small campsite. The water gives off a deep "
                "cold that numbs your fingers at the slightest touch; trying to swim it "
                "would be dangerous. Paths lead south and east."
            ),
        },
    ],
    "description": (
        "From the eastern shore of the "
        "<em><span class='area-highlight'>Lake (East)</span></em>, you can see across its "
        "cold, dark water toward the forest and distant mountain ridge. The remains of "
        "a small campsite sit among the shoreline rocks. The water is far too cold for "
        "safe swimming. Paths lead south and east."
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
                "The lake water is clear near the rocky edge, then quickly deepens to "
                "a dark blue-green. Cold rises from its surface, and even brief contact "
                "leaves your skin aching. Swimming across would not be safe."
            ),
            "searchResponse": (
                "You study the clear water near the eastern shore, but find nothing "
                "worth retrieving from its dangerously cold depths."
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
                "A patch of flattened earth sits between the shoreline rocks. A crude "
                "fire circle and a few weathered scraps are all that remain of the old "
                "campsite."
            ),
            "searchable": True,
            "searchEmptyResponse": (
                "You search through the eastern campsite rocks but find nothing else useful."
            ),
            "items": [
                "a1_disposable_lighter",
            ],
            "itemDescriptions": {
                "a1_disposable_lighter": (
                    "a scratched "
                    "<em><span class='item-highlight'>disposable lighter</span></em> "
                    "wedged between rocks near the water's edge"
                ),
            },
        },
    },
    "exits": {
        "north": False,
        "south": "a1_lake_south",
        "east": "a1_stone_ring",
        "west": False,
    },
}
