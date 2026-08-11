from areas.locationRegistry import locationRegistry
from game.handlers.drop import resolve_drop_item
from game.itemAccess import (
    get_visible_item_ids,
    resolve_item,
)
from game.itemPresentation import get_item_display_name
from game.parserUtils import parse_command_parts
from game.responses import (
    CommandFailure,
    normalize_response_messages,
)
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

    # DROP prioritizes carried items over equipped items.
    if verb == "drop":
        item_id, clarification, is_equipped = resolve_drop_item(
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

    # Container bundle transfers must keep their own
    # response and pending-overflow behavior.
    if item.get(
        "transferContentsOnTake",
        False,
    ):
        return None

    return {
        "verb": verb,
        "itemName": get_item_display_name(
            item,
        ),
    }


def execute_compound_commands(
    commands,
    game_state,
    execute_single_command,
):
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

        if game_state.get(
            "pendingAction",
        ):
            flush_aggregate()

            responses.extend(
                response_messages,
            )

            break

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
