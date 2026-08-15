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
        "inspect": [
            {
                "speaker": "narrator",
                "text": (
                    "A thin, faded rain poncho that smells faintly of damp canvas. "
                    "The fabric is worn and frayed at the edges, but it still seems "
                    "functional enough to provide some protection from the rain."
                ),
            },
            {
                "speaker": "voice",
                "text": (
                    "Still usable... This should keep me somewhat dry in a downpour."
                ),
            },
        ],
        "looseDescription": (
            "an old <em><span class='equipment-highlight'>rain poncho</span></em> "
            "lying on the ground."
        ),
        "takeable": True,
        "wearable": True,
        "flammable": False,
        "slot": "outerwear",
        "onThrow": {
            "default": {
                "response": "You toss the rain poncho onto the ground.",
                "destroyItem": False,
            },
        },
    },
)
