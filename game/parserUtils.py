verbAliases = {
    "grab": "take",
    "get": "take",
    "pickup": "take",
    "equip": "wear",
    "inspect": "look",
    "examine": "look",
}


prepositions = [
    "on",
    "in",
    "into",
    "with",
    "at",
    "from",
    "to",
]


commandVerbs = {
    "look",
    "search",
    "open",
    "close",
    "inventory",
    "inv",
    "bag",
    "i",
    "take",
    "drop",
    "throw",
    "wear",
    "use",
    "help",
    "h",
}


movementCommands = {
    "n",
    "north",
    "s",
    "south",
    "e",
    "east",
    "w",
    "west",
}


# These commands can reuse the object from the
# previous action when the player leaves it out.
#
# Example:
# take axe and throw at tree
#
# becomes:
# take axe
# throw axe at tree
carryPreviousObjectVerbs = {
    "throw",
    "use",
    "drop",
    "wear",
}


pronouns = {
    "it",
    "them",
}


def normalize_command(player_command):
    command = player_command.lower().strip()
    command = command.replace(",", " ")
    command = " ".join(command.split())

    return command


def parse_command_parts(player_command):
    command = normalize_command(
        player_command,
    )

    if not command:
        return {
            "raw": "",
            "verb": "",
            "object": None,
            "target": None,
            "preposition": None,
            "values": [],
        }

    parts = command.split()

    if len(parts) >= 2 and parts[0] == "pick" and parts[1] == "up":
        verb = "take"
        remaining_words = parts[2:]
    else:
        verb = verbAliases.get(
            parts[0],
            parts[0],
        )

        remaining_words = parts[1:]

    target = None
    preposition_used = None
    object_words = remaining_words

    for preposition in prepositions:
        if preposition in remaining_words:
            split_index = remaining_words.index(
                preposition,
            )

            object_words = remaining_words[:split_index]

            target_words = remaining_words[split_index + 1 :]

            target = (
                " ".join(
                    target_words,
                ).strip()
                or None
            )

            preposition_used = preposition

            break

    object_name = (
        " ".join(
            object_words,
        ).strip()
        or None
    )

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
        "preposition": preposition_used,
        "values": values,
    }


def starts_with_command(command):
    words = command.split()

    if not words:
        return False

    # "pick up" is a two-word verb alias.
    if len(words) >= 2 and words[0] == "pick" and words[1] == "up":
        return True

    first_word = words[0]

    if first_word in movementCommands:
        return True

    verb = verbAliases.get(
        first_word,
        first_word,
    )

    return verb in commandVerbs


def rebuild_command(command):
    verb = command["verb"]

    # Movement commands do not have objects.
    if verb in movementCommands:
        return verb

    rebuilt = verb

    object_name = command.get(
        "object",
    )

    target = command.get(
        "target",
    )

    preposition = command.get(
        "preposition",
    )

    if object_name:
        rebuilt += f" {object_name}"

    if target:
        if not preposition:
            preposition = "at"

        rebuilt += f" {preposition} " f"{target}"

    return rebuilt


def parse_compound_commands(player_command):
    command = normalize_command(
        player_command,
    )

    if not command:
        return []

    # Normal single command.
    if " and " not in command:
        return [
            command,
        ]

    segments = [
        segment.strip() for segment in command.split(" and ") if segment.strip()
    ]

    if not segments:
        return []

    parsed_commands = []

    previous_verb = None
    previous_object = None

    for segment in segments:

        # Example:
        #
        # take axe and branch
        #
        # "branch" has no verb, so it inherits "take".
        if (
            not starts_with_command(
                segment,
            )
            and previous_verb
        ):
            segment = f"{previous_verb} " f"{segment}"

        parsed = parse_command_parts(
            segment,
        )

        verb = parsed["verb"]

        # Replace simple pronouns with the object from
        # the previous action.
        #
        # take hat and wear it
        if parsed["object"] in pronouns and previous_object:
            parsed["object"] = previous_object

        if parsed["target"] in pronouns and previous_object:
            parsed["target"] = previous_object

        # Carry the previous object forward when the
        # next action clearly needs an item but the
        # player omitted it.
        #
        # take axe and throw at tree
        #
        # becomes:
        # throw axe at tree
        if (
            verb in carryPreviousObjectVerbs
            and not parsed["object"]
            and previous_object
        ):
            parsed["object"] = previous_object

        rebuilt_command = rebuild_command(
            parsed,
        )

        parsed_commands.append(
            rebuilt_command,
        )

        previous_verb = verb

        if parsed["object"]:
            previous_object = parsed["object"]

    return parsed_commands
