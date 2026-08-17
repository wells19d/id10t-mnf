a1_code_2 = (
    "a1_code_2",
    {
        "name": "Birthday Card",
        "aliases": [
            "birthday card",
            "card",
        ],
        "description": "A slightly worn birthday card.",
        "inspect": [
            {
                "speaker": "narrator",
                "text": (
                    "A slightly worn birthday card. The front reads 'Happy 11th Birthday!' in colorful letters. "
                    "It looks like it was meant for someone named 'Alex'."
                ),
            },
            {
                "speaker": "voice",
                "text": "...I wonder who Alex is. Maybe I should hold onto this for now. It might be important later.",
            },
        ],
        "looseDescription": (
            "a slightly worn <em><span class='item-highlight'>birthday card</span></em> "
            "lying on the ground."
        ),
        "takeable": True,
        "wearable": False,
        "flammable": False,
        "onThrow": {
            "default": {
                "response": "You toss the birthday card onto the ground.",
                "destroyItem": False,
            },
        },
    },
)

# “Larry… Your son's age, the day David gets back, and the inspection date. You should know by now which one comes first. Charles.”
