a1_code_3 = (
    "a1_code_3",
    {
        "name": "Calendar Page",
        "aliases": ["calendar page", "calendar", "code", "inspection date"],
        "description": "A torn calendar page with the 29th circled.",
        "inspect": [
            {
                "speaker": "narrator",
                "text": "The calendar page has 'Inspection' written across the 29th.",
            },
            {
                "speaker": "voice",
                "text": "That date looks deliberate. I should remember 29.",
            },
        ],
        "worldDescription": "a calendar lying open with the 29th circled",
        "looseDescription": "a torn calendar page lying on the floor",
        "takeable": True,
        "wearable": False,
        "takeResponse": "You tear out the page with the inspection date and take it.",
        "onThrow": {
            "default": {
                "response": "You toss the calendar page onto the ground.",
                "destroyItem": False,
            },
        },
    },
)
