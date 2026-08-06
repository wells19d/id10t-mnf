from flask import Flask, jsonify, render_template, request

from areas.clearing import clearing
from game.commandParser import parse_command
from states.gameState import currentState as gameState

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/start")
def start_game():
    if not gameState["player"]["introComplete"]:
        gameState["player"]["introComplete"] = True
        gameState["areas"]["area1"]["locations"]["clearing"]["visited"] = True

        return jsonify({"messages": clearing["intro"]})

    return jsonify({"messages": []})


@app.route("/command", methods=["POST"])
def command():
    player_command = request.json.get("command", "").strip().lower()

    response = parse_command(player_command)

    return jsonify({"response": response})
