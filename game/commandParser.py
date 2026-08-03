from areas.areaRegistry import areaRegistry
from game.failedActions import failedActions
from game.movement import move_player
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
            new_area_state = gameState["areas"][movement_response]

            if not new_area_state["visited"]:
                new_area_state["visited"] = True

                intro = new_area.get("intro", [])

                has_intro_text = any(
                    message.get("text", "").strip() for message in intro
                )

                if has_intro_text:
                    return intro

            return new_area["description"]

        return movement_response

    if player_command == "look":
        return current_area["description"]

    area_actions = current_area.get("actions", {})

    if player_command in area_actions:
        return area_actions[player_command]

    command_parts = player_command.split(maxsplit=1)
    command_verb = command_parts[0]
    command_target = command_parts[1] if len(command_parts) > 1 else None

    failed_action = failedActions.get(command_verb)

    if not failed_action:
        return failedActions["default"]

    if command_target:
        return failed_action["invalidTarget"].format(target=command_target)

    return failed_action["missingTarget"]
