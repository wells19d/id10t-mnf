from areas.registry import locationRegistry
from game.handlers.drop import resolveDropItem
from game.handlers.take import findMergeInventoryItem
from game.itemAccess import (
    visibleItemIds,
    resolveItem,
)
from game.itemDisplay import displayName
from game.parsing import parseParts
from game.responses import (
    CommandFailure,
    normalizeResponseMessages,
)
from items.registry import itemRegistry


def formatItems(
    item_names,
):
    if len(item_names) == 1:
        return item_names[0]

    if len(item_names) == 2:
        return f"{item_names[0]} " f"and {item_names[1]}"

    return ", ".join(item_names[:-1]) + f", and {item_names[-1]}"


def aggregateResponse(
    verb,
    item_names,
):
    formatted_names = formatItems(
        item_names,
    )

    if verb == "take":
        return f"You took the " f"{formatted_names}."

    if verb == "drop":
        return f"You dropped the " f"{formatted_names}."

    return None


def aggregateCandidate(
    player_command,
    game_state,
):
    command = parseParts(
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

    # DROP prioritizes carried items over equipped items.
    if verb == "drop":
        item_id, clarification, is_equipped = resolveDropItem(
            item_name,
            game_state["player"],
        )

        if clarification or not item_id:
            return None

        if is_equipped:
            return None

        item = itemRegistry[item_id]

        # Preserve custom responses instead of
        # replacing them with a generic combined one.
        if item.get("dropResponse"):
            return None

        if item.get("carryCapacity", 0):
            return None

        return {
            "verb": verb,
            "itemName": displayName(
                item,
            ),
        }

    # TAKE resolves against visible items in
    # the player's current location.
    current_location = game_state["player"]["currentLocation"]

    location_definition = locationRegistry[current_location]

    visible_items = visibleItemIds(
        location_definition,
        game_state,
    )

    item_id, clarification = resolveItem(
        item_name,
        visible_items,
    )

    if clarification or not item_id:
        return None

    item = itemRegistry[item_id]

    if findMergeInventoryItem(
        item_id,
        game_state["player"]["inventory"],
    ):
        return None

    # Preserve custom TAKE responses.
    if item.get("takeResponse"):
        return None

    # Container bundle transfers must keep their own
    # response and pending-overflow behavior.
    if item.get(
        "transferContentsOnTake",
        False,
    ):
        return None

    return {
        "verb": verb,
        "itemName": displayName(
            item,
        ),
    }


def isTakeWearPair(commands):
    if len(commands) != 2:
        return False

    take_command = parseParts(
        commands[0],
    )
    wear_command = parseParts(
        commands[1],
    )

    return (
        take_command["verb"] == "take"
        and wear_command["verb"] == "wear"
        and bool(take_command["object"])
        and take_command["object"] == wear_command["object"]
        and take_command["target"] is None
        and wear_command["target"] is None
        and take_command["preposition"] is None
        and wear_command["preposition"] is None
    )


def runCompound(
    commands,
    game_state,
    runOne,
):
    responses = []
    take_wear_pair = isTakeWearPair(
        commands,
    )
    initially_equipped = set(
        game_state["player"]["equipped"],
    )
    completed_commands = 0

    # Successful TAKE/DROP commands can be buffered
    # and combined into one natural narrator response.
    aggregate_verb = None
    aggregate_names = []
    aggregate_original_responses = []

    def flushAggregate():
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
            aggregate_response = aggregateResponse(
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
        aggregate_candidate = aggregateCandidate(
            command,
            game_state,
        )

        result = runOne(
            command,
            game_state,
        )

        failed = isinstance(
            result,
            CommandFailure,
        )

        response = result.response if failed else result

        response_messages = normalizeResponseMessages(
            response,
        )

        if game_state.get(
            "pendingAction",
        ):
            flushAggregate()

            responses.extend(
                response_messages,
            )

            break

        # Failed commands are never folded into an
        # aggregate response.
        if failed:
            flushAggregate()

            responses.extend(
                response_messages,
            )

            break

        completed_commands += 1

        if aggregate_candidate:
            candidate_verb = aggregate_candidate["verb"]

            candidate_name = aggregate_candidate["itemName"]

            # A different aggregateable verb starts
            # a new group.
            if aggregate_verb and candidate_verb != aggregate_verb:
                flushAggregate()

            aggregate_verb = candidate_verb

            aggregate_names.append(
                candidate_name,
            )

            aggregate_original_responses.append(
                response_messages,
            )

            continue

        # Non-aggregateable actions preserve order.
        flushAggregate()

        responses.extend(
            response_messages,
        )

    flushAggregate()

    if take_wear_pair and completed_commands == len(commands):
        newly_equipped = [
            item_id
            for item_id in game_state["player"]["equipped"]
            if item_id not in initially_equipped
        ]

        if len(newly_equipped) == 1:
            item = itemRegistry[newly_equipped[0]]

            take_wear_response = item.get(
                "takeWearResponse",
            )

            if take_wear_response is not None:
                return normalizeResponseMessages(
                    take_wear_response,
                )

    return responses
