from game.handlers.common import (
    get_item_display_name,
    normalize_response_messages,
)
from items.itemRegistry import itemRegistry


def handle_inventory(game_state):
    inventory = game_state["player"]["inventory"]

    if not inventory:
        return game_state.get(
            "inventoryEmptyResponse",
            "You aren't carrying anything.",
        )

    item_names = []

    for item_id in inventory:
        item = itemRegistry.get(item_id)

        if item:
            item_names.append(get_item_display_name(item))

    inventory_items = "".join(
        f"<div class='inventory-item'>{item_name}</div>" for item_name in item_names
    )

    narrator_text = (
        "<div class='inventory-label'>You are carrying:</div>"
        f"<div class='inventory-grid'>{inventory_items}</div>"
    )

    inventory_voice = game_state.get("inventoryVoice")

    if not inventory_voice:
        return narrator_text

    inventory_voice_messages = normalize_response_messages(
        inventory_voice,
        default_speaker="voice",
    )

    return [
        {
            "speaker": "narrator",
            "text": narrator_text,
        },
        *inventory_voice_messages,
    ]
