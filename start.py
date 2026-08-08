# start.py

import subprocess
import sys
import threading
import time
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


def ensure_flask():
    try:
        import flask  # noqa: F401
    except ModuleNotFoundError:
        install_flask()


def open_browser():
    time.sleep(1)
    webbrowser.open("http://127.0.0.1:5000")


def run_game():
    sys.dont_write_bytecode = True

    ensure_flask()

    threading.Thread(
        target=open_browser,
        daemon=True,
    ).start()

    try:
        subprocess.call(
            [
                sys.executable,
                "-m",
                "flask",
                "--app",
                "app",
                "run",
                "--debug",
            ]
        )
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    run_game()
