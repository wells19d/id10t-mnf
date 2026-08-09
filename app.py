import logging
import time

from flask import (
    Flask,
    jsonify,
    render_template,
    request,
)

from areas.locationRegistry import locationRegistry
from game.commandParser import parse_command
from game.definitionValidator import validate_game_definitions
from game.handlers.common import (
    get_current_location_state,
    get_location_description,
)
from states.gameState import (
    create_game_state,
    is_valid_saved_state,
    restore_game_state,
)

validate_game_definitions()

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
def dev_version():
    return jsonify(
        {
            "version": SERVER_STARTED_AT,
        }
    )


@app.get("/start")
def start_game():
    return jsonify(
        {
            "startup": STARTUP_MESSAGE,
        }
    )


@app.post("/new-game")
def new_game():
    game_state = create_game_state()

    game_state["player"]["introComplete"] = True

    current_location = game_state["player"]["currentLocation"]

    location_definition = locationRegistry[current_location]

    location_state = get_current_location_state(
        game_state,
    )

    location_state["visited"] = True

    if not is_valid_saved_state(
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

    return jsonify(
        {
            "messages": location_definition.get(
                "intro",
                [],
            ),
            "state": game_state,
        }
    )


@app.post("/load-game")
def load_game():
    data = (
        request.get_json(
            silent=True,
        )
        or {}
    )

    saved_state = data.get(
        "state",
    )

    game_state = restore_game_state(
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

    location_description = get_location_description(
        location_definition,
        game_state,
    )

    if not is_valid_saved_state(
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

    return jsonify(
        {
            "messages": [
                {
                    "speaker": "narrator",
                    "text": location_description,
                },
            ],
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

    game_state = restore_game_state(
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

    response = parse_command(
        player_command,
        game_state,
    )

    if not is_valid_saved_state(
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

    return jsonify(
        {
            "response": response,
            "state": game_state,
        }
    )
