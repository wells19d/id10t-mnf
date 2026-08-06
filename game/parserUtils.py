verbAliases = {
    "grab": "take",
    "get": "take",
    "pickup": "take",
    "equip": "wear",
    "inspect": "look",
    "examine": "look",
}


def normalize_command(player_command):
    command = player_command.lower().strip()
    command = command.replace(",", " ")
    command = " ".join(command.split())

    return command


def parse_command_parts(player_command):
    command = normalize_command(player_command)

    if not command:
        return {
            "raw": "",
            "verb": "",
            "object": None,
            "target": None,
            "values": [],
        }

    parts = command.split()

    if len(parts) >= 2 and parts[0] == "pick" and parts[1] == "up":
        verb = "take"
        remaining_words = parts[2:]
    else:
        verb = verbAliases.get(parts[0], parts[0])
        remaining_words = parts[1:]

    target = None
    object_words = remaining_words

    for preposition in [
        "on",
        "in",
        "into",
        "with",
        "at",
        "from",
        "to",
    ]:
        if preposition in remaining_words:
            split_index = remaining_words.index(preposition)

            object_words = remaining_words[:split_index]
            target_words = remaining_words[split_index + 1 :]

            target = " ".join(target_words).strip() or None
            break

    object_name = " ".join(object_words).strip() or None

    if object_name and object_name.startswith("the "):
        object_name = object_name[4:]

    if target and target.startswith("the "):
        target = target[4:]

    values = [word for word in object_words if word.isdigit()]

    return {
        "raw": command,
        "verb": verb,
        "object": object_name,
        "target": target,
        "values": values,
    }
