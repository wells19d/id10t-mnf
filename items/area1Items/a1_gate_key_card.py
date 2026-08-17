a1_gate_key_card = (
    "a1_gate_key_card",
    {
        "name": "Gate Key Card",
        "aliases": ["gate key card", "key card", "keycard", "card"],
        "description": "A plastic security key card marked for gate access.",
        "inspect": "The card's magnetic strip is scratched but intact. It is labeled 'Guard Station'.",
        "looseDescription": "a gate key card lying on the ground",
        "takeable": True,
        "wearable": False,
        "onThrow": {
            "default": {
                "response": "You toss the Gate Key Card onto the ground.",
                "destroyItem": False,
            },
        },
    },
)
