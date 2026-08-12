import logging
import time

from flask import (
    Flask,
    jsonify,
    render_template,
    request,
)

from areas.registry import locationRegistry
from game.commands import parseCommand
from game.validators import validateGameDefs
from game.handlers.common import (
    currentLocation,
    locationText,
    pendingPrompt,
    isValidResponse,
    normalizeResponseMessages,
)
from states.game import (
    newGame,
    isValidSave,
    restoreGame,
)

validateGameDefs()

app = Flask(__name__)

logging.getLogger("werkzeug").setLevel(logging.ERROR)

SERVER_STARTED_AT = time.time()

STARTUP_MESSAGE = [
    "Project ID10T: A MEMORY NOT FOUND",
    "A Text-Based Adventure",
    "Version 0.1",
    "Developed by AJ Wells at Wellscrypted",
    'Type "help" or "h" for available commands.',
]

INVALID_SAVE_ERROR_CODE = "invalid-save"


@app.route("/")
def home():
    return render_template(
        "index.html",
    )


@app.get("/dev-version")
def devVersion():
    return jsonify(
        {
            "version": SERVER_STARTED_AT,
        }
    )


@app.get("/start")
def startGame():
    return jsonify(
        {
            "startup": STARTUP_MESSAGE,
        }
    )


@app.post("/new-game")
def newGameRoute():
    game_state = newGame()

    game_state["player"]["introComplete"] = True

    current_location = game_state["player"]["currentLocation"]

    location_definition = locationRegistry[current_location]

    location_state = currentLocation(
        game_state,
    )

    location_state["visited"] = True

    if not isValidSave(
        game_state,
    ):
        return (
            jsonify(
                {
                    "error": "The new game produced an invalid game state.",
                    "errorCode": "invalid-result-state",
                }
            ),
            500,
        )

    intro_messages = normalizeResponseMessages(
        location_definition.get(
            "intro",
            [],
        ),
        allow_empty_list=True,
        allow_empty_text=True,
    )

    return jsonify(
        {
            "messages": intro_messages,
            "state": game_state,
        }
    )


@app.post("/load-game")
def loadGame():
    data = (
        request.get_json(
            silent=True,
        )
        or {}
    )

    saved_state = data.get(
        "state",
    )

    game_state = restoreGame(
        saved_state,
    )

    if not game_state:
        return (
            jsonify(
                {
                    "error": "Invalid save data.",
                    "errorCode": INVALID_SAVE_ERROR_CODE,
                }
            ),
            400,
        )

    current_location = game_state["player"].get(
        "currentLocation",
        "a1_clearing",
    )

    location_definition = locationRegistry.get(
        current_location,
    )

    if not location_definition:
        return (
            jsonify(
                {
                    "error": "Saved location no longer exists.",
                    "errorCode": INVALID_SAVE_ERROR_CODE,
                }
            ),
            400,
        )

    location_description = locationText(
        location_definition,
        game_state,
    )

    if not isValidSave(
        game_state,
    ):
        return (
            jsonify(
                {
                    "error": "Loading produced an invalid game state.",
                    "errorCode": "invalid-result-state",
                }
            ),
            500,
        )

    messages = [
        {
            "speaker": "narrator",
            "text": location_description,
        },
    ]

    pending_action_prompt = pendingPrompt(
        game_state,
    )

    if pending_action_prompt:
        messages.append(
            {
                "speaker": "narrator",
                "text": pending_action_prompt,
            }
        )

    return jsonify(
        {
            "messages": messages,
            "state": game_state,
        }
    )


@app.post("/command")
def command():
    data = (
        request.get_json(
            silent=True,
        )
        or {}
    )

    player_command = (
        data.get(
            "command",
            "",
        )
        .strip()
        .lower()
    )

    game_state = restoreGame(
        data.get(
            "state",
        ),
    )

    if not game_state:
        return (
            jsonify(
                {
                    "error": "Invalid game state.",
                    "errorCode": INVALID_SAVE_ERROR_CODE,
                }
            ),
            400,
        )

    response = parseCommand(
        player_command,
        game_state,
    )

    if not isValidSave(
        game_state,
    ):
        return (
            jsonify(
                {
                    "error": "The command produced an invalid game state.",
                    "errorCode": "invalid-result-state",
                }
            ),
            500,
        )

    if not isValidResponse(
        response,
    ):
        return (
            jsonify(
                {
                    "error": "The command produced an invalid response.",
                    "errorCode": "invalid-result-response",
                }
            ),
            500,
        )

    return jsonify(
        {
            "response": response,
            "state": game_state,
        }
    )
