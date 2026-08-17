from game.worldState import requirementsMet


def handleHint(location_definition, game_state):
    for hint in location_definition.get(
        "hints",
        [],
    ):
        if requirementsMet(
            hint.get(
                "requires",
                {},
            ),
            game_state,
        ):
            return hint["response"]

    return {
        "speaker": "voice",
        "text": "Nothing useful comes to mind right now.",
    }
