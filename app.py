import time

from flask import (
    Flask,
    jsonify,
    render_template,
    request,
)

from areas.clearing import clearing
from game.commandParser import parse_command
from game.handlers.common import get_current_location_state
from states.gameState import currentState as gameState

app = Flask(__name__)

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
    return render_template("index.html")


@app.get("/dev-version")
def dev_version():
    return jsonify(
        {
            "version": SERVER_STARTED_AT,
        }
    )


@app.route("/start")
def start_game():
    if not gameState["player"]["introComplete"]:
        gameState["player"]["introComplete"] = True

        location_state = get_current_location_state(
            gameState,
        )

        location_state["visited"] = True

        return jsonify(
            {
                "startup": STARTUP_MESSAGE,
                "messages": clearing["intro"],
            }
        )

    return jsonify(
        {
            "messages": [],
        }
    )


@app.route("/command", methods=["POST"])
def command():
    player_command = (
        request.json.get(
            "command",
            "",
        )
        .strip()
        .lower()
    )

    response = parse_command(
        player_command,
    )

    return jsonify(
        {
            "response": response,
        }
    )
