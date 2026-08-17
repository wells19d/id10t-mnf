# game/commands.py

from areas.registry import locationRegistry
from game.compCommands import runCompound
from game.failedActions import failedActions
from game.movement import (
    fullDirections,
    movePlayer,
    movePlayerToRoom,
)
from game.parsing import (
    parseParts,
    parseCompound,
)

from game.handlers.common import (
    CommandFailure,
    commandFailure,
    runPending,
    currentLocation,
    locationText,
    pendingPrompt,
    normalizeResponseMessages,
)
from game.handlers.drop import handleDrop
from game.handlers.empty import handleEmpty
from game.handlers.hint import handleHint
from game.handlers.inventory import (
    handleInventory,
    handlePlayerStatus,
)
from game.handlers.look import handleLook
from game.handlers.open_close import (
    handleClose,
    handleOpen,
)
from game.handlers.search import handleSearch
from game.handlers.take import handleTake
from game.handlers.throw import handleThrow
from game.handlers.use import handleUse
from game.handlers.wear import (
    handleRemove,
    handleWear,
)
from game.help import helpResponse


def movementResponse(
    movement_result,
    game_state,
):
    if movement_result.destination:
        new_location_definition = locationRegistry[movement_result.destination]

        new_location_state = currentLocation(
            game_state,
        )

        if not new_location_state["visited"]:
            new_location_state["visited"] = True

            intro_response = new_location_definition.get(
                "intro",
                [],
            )

            intro_messages = normalizeResponseMessages(
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

        return locationText(
            new_location_definition,
            game_state,
        )

    return commandFailure(
        movement_result.response,
    )


def runOne(player_command, game_state):
    player_state = game_state["player"]

    if player_command in [
        "help",
        "h",
    ]:
        return helpResponse

    current_location = player_state["currentLocation"]

    location_definition = locationRegistry[current_location]

    # Movement is checked before normal command parsing.
    movement_result = movePlayer(
        player_command,
        location_definition,
        player_state,
        game_state,
    )

    if movement_result:
        return movementResponse(
            movement_result,
            game_state,
        )

    command = parseParts(
        player_command,
    )

    command_verb = command["verb"]

    if not command_verb:
        return commandFailure(
            failedActions["default"].format(
                target=player_command,
            )
        )

    if command_verb == "go":
        room_name = command["target"] or command["object"]

        if room_name in fullDirections:
            movement_result = movePlayer(
                room_name,
                location_definition,
                player_state,
                game_state,
            )
        else:
            movement_result = movePlayerToRoom(
                room_name,
                location_definition,
                player_state,
                game_state,
            )

        return movementResponse(
            movement_result,
            game_state,
        )

    if command_verb == "look":
        return handleLook(
            command,
            location_definition,
            game_state,
        )

    if command_verb == "search":
        return handleSearch(
            command,
            location_definition,
            game_state,
        )

    if command_verb == "hint":
        return handleHint(
            location_definition,
            game_state,
        )

    if command_verb == "open":
        return handleOpen(
            command,
            location_definition,
            game_state,
        )

    if command_verb == "close":
        return handleClose(
            command,
            location_definition,
            game_state,
        )

    if command_verb in ["inventory", "inv", "bag", "i"]:
        return handleInventory(
            game_state,
        )

    if command_verb in ["player", "p"]:
        return handlePlayerStatus(
            game_state,
        )

    if command_verb == "take":
        return handleTake(
            command,
            location_definition,
            game_state,
        )

    if command_verb == "drop":
        return handleDrop(
            command,
            game_state,
        )

    if command_verb == "throw":
        return handleThrow(
            command,
            location_definition,
            game_state,
        )

    if command_verb == "empty":
        return handleEmpty(
            command,
            game_state,
        )

    if command_verb == "wear":
        return handleWear(
            command,
            game_state,
        )

    if command_verb == "remove":
        return handleRemove(
            command,
            game_state,
        )

    if command_verb == "use":
        return handleUse(
            command,
            location_definition,
            game_state,
        )

    return commandFailure(
        failedActions["default"].format(
            target=player_command,
        )
    )


def parseCommand(player_command, game_state):
    if game_state.get(
        "pendingAction",
    ):
        confirmation = player_command.strip().lower()

        if confirmation in ["yes", "y"]:
            return runPending(
                game_state,
            )

        if confirmation in ["no", "n"]:
            game_state["pendingAction"] = None

            return "You decide not to continue."

        return pendingPrompt(
            game_state,
        )

    commands = parseCompound(
        player_command,
    )

    if not commands:
        return failedActions["default"].format(
            target=player_command,
        )

    # Normal single command keeps the exact same
    # response behavior as before.
    if len(commands) == 1:
        response = runOne(
            commands[0],
            game_state,
        )

        if isinstance(
            response,
            CommandFailure,
        ):
            return response.response

        return response

    return runCompound(
        commands,
        game_state,
        runOne,
    )
