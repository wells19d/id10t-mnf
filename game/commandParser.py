# game/commandParser.py

from areas.areaRegistry import areaRegistry
from game.failedActions import failedActions
from game.movement import move_player
from game.parserUtils import (
    parse_command_parts,
    parse_compound_commands,
)

from game.handlers.common import (
    get_current_location_state,
    get_item_display_name,
    get_visible_item_ids,
    resolve_item,
)
from game.handlers.drop import handle_drop
from game.handlers.inventory import handle_inventory
from game.handlers.look import handle_look
from game.handlers.open_close import (
    handle_close,
    handle_open,
)
from game.handlers.search import handle_search
from game.handlers.take import handle_take
from game.handlers.throw import handle_throw
from game.handlers.use import handle_use
from game.handlers.wear import handle_wear
from game.help import helpResponse
from game.itemRegistry import itemRegistry

from states.gameState import currentState as gameState


def response_to_messages(response):
    if isinstance(response, list):
        return response

    if isinstance(response, dict):
        return [
            response,
        ]

    return [
        {
            "speaker": "narrator",
            "text": response,
        },
    ]


def response_failed(
    command,
    response,
):
    parsed = parse_command_parts(
        command,
    )

    verb = parsed["verb"]

    # These commands don't stop a command chain
    # simply because they found nothing.
    if verb in [
        "look",
        "search",
        "inventory",
        "inv",
        "bag",
        "i",
        "help",
        "h",
    ]:
        return False

    messages = response_to_messages(
        response,
    )

    narrator_text = " ".join(
        str(
            message.get(
                "text",
                "",
            )
        )
        for message in messages
        if message.get("speaker") != "voice"
    ).lower()

    failure_phrases = [
        "i don't ",
        "i can't ",
        "you can't ",
        "you aren't ",
        "that won't ",
        "don't have ",
        "not carrying ",
        "is locked",
        "is closed",
        "can't reach",
        "can't search",
        "can't open",
        "can't close",
        "can't use",
        "can't throw",
        "can't take",
        "can't wear",
    ]

    return any(phrase in narrator_text for phrase in failure_phrases)


def format_compound_item_names(
    item_names,
):
    if len(item_names) == 1:
        return item_names[0]

    if len(item_names) == 2:
        return f"{item_names[0]} " f"and {item_names[1]}"

    return ", ".join(item_names[:-1]) + f", and {item_names[-1]}"


def build_aggregate_response(
    verb,
    item_names,
):
    formatted_names = format_compound_item_names(
        item_names,
    )

    if verb == "take":
        return f"You took the " f"{formatted_names}."

    if verb == "drop":
        return f"You dropped the " f"{formatted_names}."

    return None


def get_aggregate_candidate(
    player_command,
):
    command = parse_command_parts(
        player_command,
    )

    verb = command["verb"]
    item_name = command["object"]
    target = command["target"]

    # For now, only simple TAKE and DROP commands
    # are combined into one narrator response.
    if verb not in [
        "take",
        "drop",
    ]:
        return None

    if not item_name:
        return None

    # Targeted TAKE commands such as:
    #
    # take key from cupboard
    #
    # keep their normal individual response.
    if target:
        return None

    # DROP resolves against inventory.
    if verb == "drop":
        item_id, clarification = resolve_item(
            item_name,
            gameState["player"]["inventory"],
        )

        if clarification or not item_id:
            return None

        item = itemRegistry[item_id]

        # Preserve custom responses instead of
        # replacing them with a generic combined one.
        if item.get("dropResponse"):
            return None

        return {
            "verb": verb,
            "itemName": get_item_display_name(
                item,
            ),
        }

    # TAKE resolves against visible items in
    # the player's current location.
    current_location = gameState["player"]["currentLocation"]

    current_area = areaRegistry[current_location]

    visible_items = get_visible_item_ids(
        current_area,
        gameState,
    )

    item_id, clarification = resolve_item(
        item_name,
        visible_items,
    )

    if clarification or not item_id:
        return None

    item = itemRegistry[item_id]

    # Preserve custom TAKE responses.
    if item.get("takeResponse"):
        return None

    return {
        "verb": verb,
        "itemName": get_item_display_name(
            item,
        ),
    }


def execute_single_command(player_command):
    player_state = gameState["player"]

    if player_command in [
        "help",
        "h",
    ]:
        return helpResponse

    current_location = player_state["currentLocation"]

    current_area = areaRegistry[current_location]

    # Movement is checked before normal command parsing.
    movement_response = move_player(
        player_command,
        current_area,
        player_state,
        gameState,
    )

    if movement_response:
        if movement_response in areaRegistry:
            new_area = areaRegistry[movement_response]

            new_area_state = get_current_location_state(
                gameState,
            )

            if not new_area_state["visited"]:
                new_area_state["visited"] = True

                intro = new_area.get(
                    "intro",
                    [],
                )

                has_intro_text = any(
                    message.get(
                        "text",
                        "",
                    ).strip()
                    for message in intro
                )

                if has_intro_text:
                    return intro

            return new_area["description"]

        return movement_response

    command = parse_command_parts(
        player_command,
    )

    command_verb = command["verb"]

    if not command_verb:
        return failedActions["default"].format(
            target=player_command,
        )

    if command_verb == "look":
        return handle_look(
            command,
            current_area,
            gameState,
        )

    if command_verb == "search":
        return handle_search(
            command,
            current_area,
            gameState,
        )

    if command_verb == "open":
        return handle_open(
            command,
            current_area,
            gameState,
        )

    if command_verb == "close":
        return handle_close(
            command,
            current_area,
            gameState,
        )

    if command_verb in [
        "inventory",
        "inv",
        "bag",
        "i",
    ]:
        return handle_inventory(
            gameState,
        )

    if command_verb == "take":
        return handle_take(
            command,
            current_area,
            gameState,
        )

    if command_verb == "drop":
        return handle_drop(
            command,
            gameState,
        )

    if command_verb == "throw":
        return handle_throw(
            command,
            current_area,
            gameState,
        )

    if command_verb == "wear":
        return handle_wear(
            command,
            gameState,
        )

    if command_verb == "use":
        return handle_use(
            command,
            current_area,
            gameState,
        )

    failed_action = failedActions.get(
        command_verb,
    )

    if not failed_action:
        return failedActions["default"].format(
            target=player_command,
        )

    command_target = command["object"]

    if command_target:
        return failed_action["invalidTarget"].format(
            target=command_target,
        )

    return failed_action["missingTarget"]


def parse_command(player_command):
    commands = parse_compound_commands(
        player_command,
    )

    if not commands:
        return failedActions["default"].format(
            target=player_command,
        )

    # Normal single command keeps the exact same
    # response behavior as before.
    if len(commands) == 1:
        return execute_single_command(
            commands[0],
        )

    responses = []

    # Successful TAKE/DROP commands can be buffered
    # and combined into one natural narrator response.
    aggregate_verb = None
    aggregate_names = []
    aggregate_original_responses = []

    def flush_aggregate():
        nonlocal aggregate_verb
        nonlocal aggregate_names
        nonlocal aggregate_original_responses

        if not aggregate_names:
            return

        # If there was only one action, preserve its
        # original response exactly.
        if len(aggregate_names) == 1:
            responses.extend(aggregate_original_responses[0])

        else:
            aggregate_response = build_aggregate_response(
                aggregate_verb,
                aggregate_names,
            )

            responses.append(
                {
                    "speaker": "narrator",
                    "text": aggregate_response,
                }
            )

        aggregate_verb = None
        aggregate_names = []
        aggregate_original_responses = []

    # Compound commands execute left to right.
    for command in commands:
        aggregate_candidate = get_aggregate_candidate(
            command,
        )

        response = execute_single_command(
            command,
        )

        response_messages = response_to_messages(
            response,
        )

        failed = response_failed(
            command,
            response,
        )

        # Failed commands are never folded into an
        # aggregate response.
        if failed:
            flush_aggregate()

            responses.extend(
                response_messages,
            )

            break

        if aggregate_candidate:
            candidate_verb = aggregate_candidate["verb"]

            candidate_name = aggregate_candidate["itemName"]

            # A different aggregateable verb starts
            # a new group.
            if aggregate_verb and candidate_verb != aggregate_verb:
                flush_aggregate()

            aggregate_verb = candidate_verb

            aggregate_names.append(
                candidate_name,
            )

            aggregate_original_responses.append(
                response_messages,
            )

            continue

        # Non-aggregateable actions preserve order.
        flush_aggregate()

        responses.extend(
            response_messages,
        )

    flush_aggregate()

    return responses
