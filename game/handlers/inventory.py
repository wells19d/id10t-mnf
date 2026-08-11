from html import escape

from game.handlers.common import (
    get_item_display_name,
    normalize_response_messages,
)
from items.itemRegistry import itemRegistry
from states.gameState import (
    EQUIPMENT_SLOT_ORDER,
    get_total_carry_capacity,
)


def handle_inventory(game_state):
    player_state = game_state["player"]
    inventory = player_state["inventory"]
    total_capacity = get_total_carry_capacity(
        player_state,
    )
    capacity_text = (
        "<div class='inventory-capacity'>"
        f"Item Capacity: {len(inventory)} / {total_capacity}"
        "</div>"
    )

    if not inventory:
        empty_response = game_state.get(
            "inventoryEmptyResponse",
            "You aren't carrying anything.",
        )

        return f"{empty_response}{capacity_text}"

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
        f"{capacity_text}"
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


def handle_player_status(game_state):
    player_state = game_state["player"]
    equipped = player_state["equipped"]

    equipped_by_slot = {}

    for item_id in equipped:
        item = itemRegistry.get(item_id)

        if not item:
            continue

        slot = item.get("slot")

        if slot:
            equipped_by_slot[slot] = item

    equipment_rows = []

    for slot in EQUIPMENT_SLOT_ORDER:
        item = equipped_by_slot.get(slot)

        if item:
            item_name = get_item_display_name(item)

            carry_capacity = item.get(
                "carryCapacity",
                0,
            )

            if slot == "back" and carry_capacity:
                item_name += f" (+{carry_capacity} item capacity)"

        else:
            item_name = "Nothing"

        equipment_rows.append(
            "<div class='player-equipment-row'>"
            f"<span class='player-equipment-slot'>{slot.title()}:</span> "
            f"{item_name}"
            "</div>"
        )

    return (
        "<div class='player-status'>"
        "<div class='player-status-title'>Player Status</div>"
        "<table class='player-health-table'>"
        "<tr>"
        "<td class='player-health-label'>Health:</td>"
        f"<td>{escape(player_state['health'])}</td>"
        "</tr>"
        "<tr>"
        "<td class='player-health-label'>Status:</td>"
        f"<td>{escape(player_state['healthStatus'])}</td>"
        "</tr>"
        "</table>"
        "<div class='player-equipment-label'>Equipped:</div>"
        f"{''.join(equipment_rows)}"
        "</div>"
    )
