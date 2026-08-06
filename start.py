# start.py

import subprocess
import sys
import threading
import webbrowser


def install_flask():
    print("Flask is not installed. Installing Flask...")

    subprocess.check_call(
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            "Flask",
        ]
    )


def load_app():
    try:
        from app import app

        return app

    except ModuleNotFoundError as error:
        if error.name != "flask":
            raise

        install_flask()

        from app import app

        return app


def open_browser():
    webbrowser.open("http://127.0.0.1:5000")


def run_game():
    sys.dont_write_bytecode = True

    app = load_app()

    threading.Timer(1, open_browser).start()

    app.run(
        debug=True,
        use_reloader=False,
    )


if __name__ == "__main__":
    run_game()
