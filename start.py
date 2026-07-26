# This file is to just provide a fast way to run the app with a short command.

import threading
import webbrowser

from app import app


def open_browser():
    webbrowser.open("http://127.0.0.1:5000")


if __name__ == "__main__":
    threading.Timer(1, open_browser).start()
    app.run(debug=True, use_reloader=False)