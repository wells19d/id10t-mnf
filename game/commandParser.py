# game/commandParser.py

from areas.locationRegistry import locationRegistry
from game.compoundCommands import (
    build_aggregate_response,
    execute_compound_commands,
    format_compound_item_names,
    get_aggregate_candidate,
)
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
    execute_pending_action,
    get_current_location_state,
    get_location_description,
    get_pending_action_prompt,
    normalize_response_messages,
)
from game.handlers.drop import handle_drop
from game.handlers.inventory import (
    handle_inventory,
    handle_player_status,
)
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


def get_movement_response(
    movement_result,
    game_state,
):
    if movement_result.destination:
        new_location_definition = locationRegistry[movement_result.destination]

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

    if command_verb in ["inventory", "inv", "bag", "i"]:
        return handle_inventory(
            game_state,
        )

    if command_verb in ["player", "p"]:
        return handle_player_status(
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
    if game_state.get(
        "pendingAction",
    ):
        confirmation = player_command.strip().lower()

        if confirmation in ["yes", "y"]:
            return execute_pending_action(
                game_state,
            )

        if confirmation in ["no", "n"]:
            game_state["pendingAction"] = None

            return "You decide not to continue."

        return get_pending_action_prompt(
            game_state,
        )

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

    return execute_compound_commands(
        commands,
        game_state,
        execute_single_command,
    )
