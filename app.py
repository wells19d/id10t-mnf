from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/command", methods=["POST"])
def command():
    narrator_response = request.json.get("command")
    

    return jsonify({
        "response": narrator_response
    })


if __name__ == "__main__":
    app.run(debug=True)