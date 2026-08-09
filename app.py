import logging
import time

from flask import (
    Flask,
    jsonify,
    render_template,
    request,
)

from areas.areaRegistry import areaRegistry
from game.commandParser import parse_command
from game.handlers.common import get_current_location_state
from states.gameState import (
    create_game_state,
    restore_game_state,
)

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

    current_area = areaRegistry[current_location]

    location_state = get_current_location_state(
        game_state,
    )

    location_state["visited"] = True

    return jsonify(
        {
            "messages": current_area.get(
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
                }
            ),
            400,
        )

    current_location = game_state["player"].get(
        "currentLocation",
        "clearing",
    )

    current_area = areaRegistry.get(
        current_location,
    )

    if not current_area:
        return (
            jsonify(
                {
                    "error": "Saved location no longer exists.",
                }
            ),
            400,
        )

    return jsonify(
        {
            "messages": [
                {
                    "speaker": "narrator",
                    "text": current_area.get(
                        "description",
                        "You look around.",
                    ),
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
                }
            ),
            400,
        )

    response = parse_command(
        player_command,
        game_state,
    )

    return jsonify(
        {
            "response": response,
            "state": game_state,
        }
    )
