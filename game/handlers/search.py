from game.handlers.common import (
    find_scenery,
    format_item_names,
    get_current_location_state,
    get_item_name,
    get_items_in_scenery,
    get_scenery_state,
)
from game.itemRegistry import itemRegistry


def handle_search(command, current_area, game_state):
    target = command["target"] or command["object"]

    location_state = get_current_location_state(
        game_state,
    )

    # SEARCH <something>
    if target:
        scenery_id, scenery_data = find_scenery(
            target,
            current_area,
        )

        if not scenery_data:
            return f"I don't see a {target} here."

        if not scenery_data.get("searchable", False):
            return scenery_data.get(
                "searchResponse",
                scenery_data.get(
                    "lookResponse",
                    scenery_data["description"],
                ),
            )

        scenery_state = get_scenery_state(
            location_state,
            scenery_id,
        )

        if scenery_data.get("openable") and not scenery_state.get("isOpen", False):
            return scenery_data.get(
                "searchClosedResponse",
                f"The {scenery_id} is closed.",
            )

        item_ids = get_items_in_scenery(
            location_state,
            scenery_id,
        )

        scenery_state["isSearched"] = True

        if not item_ids:
            return scenery_data.get(
                "searchEmptyResponse",
                f"The {scenery_id} is empty.",
            )

        item_names = []

        for item_id in item_ids:
            item = itemRegistry.get(item_id)

            if item:
                item_names.append(get_item_name(item))

        item_list = format_item_names(
            item_names,
        )

        custom_response = scenery_data.get(
            "searchResponse",
        )

        if isinstance(custom_response, list):
            responses = list(custom_response)

            responses.append(
                {
                    "speaker": "narrator",
                    "text": (f"Inside the {scenery_id}, " f"you find {item_list}."),
                }
            )

            return responses

        if custom_response:
            return custom_response

        return f"Inside the {scenery_id}, " f"you find {item_list}."

    # SEARCH the whole area.
    search_results = []

    # Loose items.
    for item_id, container_id in location_state["items"].items():
        if container_id is not None:
            continue

        item = itemRegistry.get(item_id)

        if not item:
            continue

        search_results.append(
            item.get(
                "worldDescription",
                item["description"],
            )
        )

    # Scenery.
    for scenery_id, scenery_data in current_area.get(
        "scenery",
        {},
    ).items():

        description = scenery_data["description"]

        scenery_state = get_scenery_state(
            location_state,
            scenery_id,
        )

        item_ids = get_items_in_scenery(
            location_state,
            scenery_id,
        )

        started_with_items = bool(scenery_data.get("items", []))

        if (
            scenery_data.get("hideOnEmpty", False)
            and started_with_items
            and not item_ids
        ):
            continue

        items_are_visible = not (
            scenery_data.get("openable") and not scenery_state.get("isOpen", False)
        )

        if items_are_visible and item_ids:
            item_names = []

            for item_id in item_ids:
                item = itemRegistry.get(item_id)

                if item:
                    item_names.append(get_item_name(item))

            item_prefix = scenery_data.get(
                "itemPrefix",
            )

            if item_prefix and item_names:
                item_list = format_item_names(
                    item_names,
                )

                description = f"{description} " f"{item_prefix} {item_list}."

        search_results.append(description)

    if not search_results:
        return "You don't find anything useful here."

    narrator_text = "You search the area and find: " + " ".join(search_results)

    search_voice = current_area.get(
        "searchVoice",
    )

    if not search_voice:
        return narrator_text

    if isinstance(search_voice, str):
        search_voice = {
            "speaker": "voice",
            "text": search_voice,
        }

    return [
        {
            "speaker": "narrator",
            "text": narrator_text,
        },
        search_voice,
    ]
