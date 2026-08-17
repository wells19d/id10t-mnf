a1_code_1 = (
    "a1_code_1",
    {
        "name": "Calendar Page",
        "aliases": ["calendar page", "calendar", "code", "return date"],
        "description": "A torn calendar page with the 18th circled.",
        "inspect": [
            {
                "speaker": "narrator",
                "text": "The calendar page has 'David returns' written across the 18th.",
            },
            {
                "speaker": "voice",
                "text": "The date was important enough to circle. I should remember 18.",
            },
        ],
        "worldDescription": "a calendar lying open with the 18th circled",
        "looseDescription": "a torn calendar page lying on the floor",
        "takeable": True,
        "wearable": False,
        "takeResponse": "You tear out the calendar page marked with David's return date and take it.",
        "onThrow": {
            "default": {
                "response": "You toss the calendar page onto the ground.",
                "destroyItem": False,
            },
        },
    },
)
