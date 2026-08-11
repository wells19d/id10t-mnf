from game.responses import normalize_response_messages
from game.worldState import state_matches
from items.itemRegistry import itemRegistry


def get_item_name(item):
    return item.get(
        "name",
        item["aliases"][0],
    )


def get_item_display_name(item):
    item_name = get_item_name(
        item,
    )

    highlight_class = (
        "equipment-highlight" if item.get("wearable", False) else "item-highlight"
    )

    return f"<em><span class='{highlight_class}'>" f"{item_name}" "</span></em>"


def get_formatted_item_list(item_ids):
    item_names = [
        get_item_display_name(
            itemRegistry[item_id],
        )
        for item_id in item_ids
    ]

    return format_item_names(
        item_names,
    )


def append_narrator_response(
    response,
    narrator_text,
):
    messages = normalize_response_messages(
        response,
    )

    messages.append(
        {
            "speaker": "narrator",
            "text": narrator_text,
        }
    )

    return messages


def get_item_quantity_description(
    item,
    item_state,
):
    quantity_display = item.get(
        "quantityDisplay",
    )

    if not quantity_display:
        return None

    if not state_matches(
        item_state,
        quantity_display.get(
            "requiresState",
            {},
        ),
    ):
        return None

    state_key = quantity_display["stateKey"]
    quantity = item_state.get(
        state_key,
    )

    if type(quantity) is not int or quantity < 0:
        return None

    label = (
        quantity_display["singular"]
        if quantity == 1
        else quantity_display["plural"]
    )

    return f"It contains {quantity} {label}."


def append_item_quantity_description(
    response,
    item,
    item_state,
):
    quantity_description = get_item_quantity_description(
        item,
        item_state,
    )

    if not quantity_description:
        return response

    if isinstance(response, str):
        return f"{response} {quantity_description}"

    return append_narrator_response(
        response,
        quantity_description,
    )


def format_item_names(item_names):
    if len(item_names) == 1:
        return f"a {item_names[0]}"

    if len(item_names) == 2:
        return f"a {item_names[0]} and a {item_names[1]}"

    first_items = ", ".join(item_names[:-1])

    return f"a {first_items}, " f"and a {item_names[-1]}"
