# game/commandParser.py

from areas.locationRegistry import locationRegistry
from game.failedActions import failedActions
from game.movement import (
    move_player,
    move_player_to_room,
)
from game.parserUtils import (
    parse_command_parts,
    parse_compound_commands,
)

from game.handlers.common import (
    CommandFailure,
    command_failure,
    get_current_location_state,
    get_item_display_name,
    get_location_description,
    get_visible_item_ids,
    normalize_response_messages,
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
from game.handlers.wear import (
    handle_remove,
    handle_wear,
)
from game.help import helpResponse
from items.itemRegistry import itemRegistry


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
    game_state,
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
            game_state["player"]["inventory"],
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
    current_location = game_state["player"]["currentLocation"]

    location_definition = locationRegistry[current_location]

    visible_items = get_visible_item_ids(
        location_definition,
        game_state,
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


def get_movement_response(
    movement_result,
    game_state,
):
    if movement_result.destination:
        new_location_definition = locationRegistry[
            movement_result.destination
        ]

        new_location_state = get_current_location_state(
            game_state,
        )

        if not new_location_state["visited"]:
            new_location_state["visited"] = True

            intro_response = new_location_definition.get(
                "intro",
                [],
            )

            intro_messages = normalize_response_messages(
                intro_response,
                allow_empty_list=True,
                allow_empty_text=True,
            )

            has_intro_text = any(
                message.get(
                    "text",
                    "",
                ).strip()
                for message in intro_messages
            )

            if has_intro_text:
                return intro_messages

        return get_location_description(
            new_location_definition,
            game_state,
        )

    return command_failure(
        movement_result.response,
    )


def execute_single_command(player_command, game_state):
    player_state = game_state["player"]

    if player_command in [
        "help",
        "h",
    ]:
        return helpResponse

    current_location = player_state["currentLocation"]

    location_definition = locationRegistry[current_location]

    # Movement is checked before normal command parsing.
    movement_result = move_player(
        player_command,
        location_definition,
        player_state,
        game_state,
    )

    if movement_result:
        return get_movement_response(
            movement_result,
            game_state,
        )

    command = parse_command_parts(
        player_command,
    )

    command_verb = command["verb"]

    if not command_verb:
        return command_failure(
            failedActions["default"].format(
                target=player_command,
            )
        )

    if command_verb == "go":
        room_name = command["target"] or command["object"]

        movement_result = move_player_to_room(
            room_name,
            location_definition,
            player_state,
        )

        return get_movement_response(
            movement_result,
            game_state,
        )

    if command_verb == "look":
        return handle_look(
            command,
            location_definition,
            game_state,
        )

    if command_verb == "search":
        return handle_search(
            command,
            location_definition,
            game_state,
        )

    if command_verb == "open":
        return handle_open(
            command,
            location_definition,
            game_state,
        )

    if command_verb == "close":
        return handle_close(
            command,
            location_definition,
            game_state,
        )

    if command_verb in [
        "inventory",
        "inv",
        "bag",
        "i",
    ]:
        return handle_inventory(
            game_state,
        )

    if command_verb == "take":
        return handle_take(
            command,
            location_definition,
            game_state,
        )

    if command_verb == "drop":
        return handle_drop(
            command,
            game_state,
        )

    if command_verb == "throw":
        return handle_throw(
            command,
            location_definition,
            game_state,
        )

    if command_verb == "wear":
        return handle_wear(
            command,
            game_state,
        )

    if command_verb == "remove":
        return handle_remove(
            command,
            game_state,
        )

    if command_verb == "use":
        return handle_use(
            command,
            location_definition,
            game_state,
        )

    failed_action = failedActions.get(
        command_verb,
    )

    if not failed_action:
        return command_failure(
            failedActions["default"].format(
                target=player_command,
            )
        )

    command_target = command["object"]

    if command_target:
        return command_failure(
            failed_action["invalidTarget"].format(
                target=command_target,
            )
        )

    return command_failure(
        failed_action["missingTarget"],
    )


def parse_command(player_command, game_state):
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
        response = execute_single_command(
            commands[0],
            game_state,
        )

        if isinstance(
            response,
            CommandFailure,
        ):
            return response.response

        return response

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
            game_state,
        )

        result = execute_single_command(
            command,
            game_state,
        )

        failed = isinstance(
            result,
            CommandFailure,
        )

        response = result.response if failed else result

        response_messages = normalize_response_messages(
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
