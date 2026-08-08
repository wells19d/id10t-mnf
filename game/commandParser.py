# game/commandParser.py

from areas.areaRegistry import areaRegistry
from game.failedActions import failedActions
from game.movement import move_player
from game.parserUtils import parse_command_parts

from game.handlers.common import get_current_location_state
from game.handlers.drop import handle_drop
from game.handlers.inventory import handle_inventory
from game.handlers.look import handle_look
from game.handlers.open_close import handle_close, handle_open
from game.handlers.search import handle_search
from game.handlers.take import handle_take
from game.handlers.throw import handle_throw
from game.handlers.use import handle_use
from game.handlers.wear import handle_wear

from states.gameState import currentState as gameState


def parse_command(player_command):
    player_state = gameState["player"]

    current_location = player_state["currentLocation"]

    current_area = areaRegistry[current_location]

    movement_response = move_player(
        player_command,
        current_area,
        player_state,
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
                    message.get("text", "").strip() for message in intro
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
        return failedActions["default"]

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
        return failedActions["default"]

    command_target = command["object"]

    if command_target:
        return failed_action["invalidTarget"].format(
            target=command_target,
        )

    return failed_action["missingTarget"]
