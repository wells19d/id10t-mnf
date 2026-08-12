from game.validators import items, locations


def validateGameDefs():
    errors = items.getErrors() + locations.getErrors()

    if errors:
        formatted_errors = "\n".join(
            f"- {error}"
            for error in errors
        )

        raise ValueError(
            "Invalid game definitions:\n"
            f"{formatted_errors}"
        )
