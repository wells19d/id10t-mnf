a1_rain_poncho = (
    "a1_rain_poncho",
    {
        "name": "Old Rain Poncho",
        "aliases": [
            "old rain poncho",
            "rain poncho",
            "poncho",
        ],
        "description": (
            "A thin, faded rain poncho that smells faintly of damp canvas."
        ),
        "looseDescription": (
            "an old <em><span class='equipment-highlight'>rain poncho</span></em> "
            "lying on the ground."
        ),
        "takeable": True,
        "wearable": True,
        "slot": "outerwear",
        "onThrow": {
            "default": {
                "response": "You toss the rain poncho onto the ground.",
                "destroyItem": False,
            },
        },
    },
)
