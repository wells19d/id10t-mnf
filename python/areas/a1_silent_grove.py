a1_silent_grove = {
    "name": "Silent Grove",
    "intro": [
        {
            "speaker": "narrator",
            "text": (
                "You enter a <em><span class='area-highlight'>Silent Grove</span></em>, the air still and filled with the scent of damp earth and moss. "
                "The trees here are tall and ancient, their branches forming a dense canopy overhead. "
                "Sunlight filters through the leaves, casting dappled shadows across the forest floor. "
                "It's peaceful here, but the silence is almost eerie. "
                "A worn path leads north, while other paths continue east and west."
            ),
        },
    ],
    "description": (
        "You are standing in a quiet and secluded "
        "<em><span class='area-highlight'>Silent Grove</span></em>. "
        "Worn paths lead north, east, and west."
    ),
    "scenery": {},
    "items": ["a1_old_backpack"],
    "itemContents": {
        "a1_old_backpack": [
            "a1_house_key_2",
            "a1_code_2",
            "a1_rain_poncho",
            "a1_matchbox_1",
        ],
    },
    "exits": {
        "north": "a1_clearing",
        "south": False,
        "east": "a1_house_1",
        "west": "a1_house_3",
    },
}
