VALID_RESPONSE_SPEAKERS = frozenset(
    {
        "narrator",
        "voice",
        "system",
    }
)


class CommandFailure:
    def __init__(self, response):
        self.response = response


def command_failure(response):
    return CommandFailure(
        response,
    )


def is_valid_response_message(
    message,
    allow_empty_text=False,
):
    if not isinstance(message, dict):
        return False

    speaker = message.get(
        "speaker",
    )
    text = message.get(
        "text",
    )

    if not isinstance(speaker, str) or speaker not in VALID_RESPONSE_SPEAKERS:
        return False

    if not isinstance(text, str):
        return False

    return allow_empty_text or bool(text.strip())


def is_valid_response(
    response,
    allow_empty_list=False,
    allow_empty_text=False,
):
    if isinstance(response, str):
        return allow_empty_text or bool(response.strip())

    if isinstance(response, dict):
        return is_valid_response_message(
            response,
            allow_empty_text,
        )

    if isinstance(response, list):
        if not response and not allow_empty_list:
            return False

        return all(
            is_valid_response_message(
                message,
                allow_empty_text,
            )
            for message in response
        )

    return False


def normalize_response_messages(
    response,
    default_speaker="narrator",
    allow_empty_list=False,
    allow_empty_text=False,
):
    if not is_valid_response(
        response,
        allow_empty_list,
        allow_empty_text,
    ):
        raise ValueError("Invalid response shape.")

    if isinstance(response, str):
        return [
            {
                "speaker": default_speaker,
                "text": response,
            }
        ]

    if isinstance(response, dict):
        return [
            response,
        ]

    return list(
        response,
    )
