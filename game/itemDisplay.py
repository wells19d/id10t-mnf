from game.responses import normalizeResponseMessages
from game.worldState import stateMatches
from items.registry import itemRegistry


def itemName(item):
    return item.get(
        "name",
        item["aliases"][0],
    )


def displayName(item):
    item_name = itemName(
        item,
    )

    highlight_class = (
        "equipment-highlight" if item.get("wearable", False) else "item-highlight"
    )

    return f"<em><span class='{highlight_class}'>" f"{item_name}" "</span></em>"


def itemList(item_ids):
    item_names = [
        displayName(
            itemRegistry[item_id],
        )
        for item_id in item_ids
    ]

    return formatNames(
        item_names,
    )


def addNarration(
    response,
    narrator_text,
):
    messages = normalizeResponseMessages(
        response,
    )

    messages.append(
        {
            "speaker": "narrator",
            "text": narrator_text,
        }
    )

    return messages


def quantityText(
    item,
    item_state,
):
    quantity_display = item.get(
        "quantityDisplay",
    )

    if not quantity_display:
        return None

    if not stateMatches(
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


def addQuantityText(
    response,
    item,
    item_state,
):
    quantity_description = quantityText(
        item,
        item_state,
    )

    if not quantity_description:
        return response

    if isinstance(response, str):
        return f"{response} {quantity_description}"

    return addNarration(
        response,
        quantity_description,
    )


def formatNames(item_names):
    if len(item_names) == 1:
        return f"a {item_names[0]}"

    if len(item_names) == 2:
        return f"a {item_names[0]} and a {item_names[1]}"

    first_items = ", ".join(item_names[:-1])

    return f"a {first_items}, " f"and a {item_names[-1]}"
