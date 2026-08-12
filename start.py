# start.py

import subprocess
import sys
import threading
import time
import webbrowser


def installFlask():
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


def ensureFlask():
    try:
        import flask  # noqa: F401
    except ModuleNotFoundError:
        installFlask()


def openBrowser():
    time.sleep(1)
    webbrowser.open("http://127.0.0.1:5000")


def runGame():
    sys.dont_write_bytecode = True

    ensureFlask()

    threading.Thread(
        target=openBrowser,
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
    runGame()
