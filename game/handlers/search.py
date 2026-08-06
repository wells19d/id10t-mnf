from game.handlers.common import (
    find_scenery,
    format_item_names,
    get_current_location_state,
    get_item_name,
    get_scenery_state,
)
from game.itemRegistry import itemRegistry


def handle_search(command, current_area, game_state):
    target = command["target"] or command["object"]
    location_state = get_current_location_state(game_state)

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

        visible_names = []

        for item_id in scenery_data.get("items", []):
            if item_id not in location_state["itemsAvailable"]:
                continue

            item = itemRegistry.get(item_id)

            if item:
                visible_names.append(get_item_name(item))

        scenery_state["isSearched"] = True

        if not visible_names:
            return scenery_data.get(
                "searchEmptyResponse",
                f"The {scenery_id} is empty.",
            )

        custom_response = scenery_data.get("searchResponse")

        if custom_response:
            if isinstance(custom_response, list):
                item_list = format_item_names(visible_names)

                responses = list(custom_response)
                responses.append(
                    {
                        "speaker": "narrator",
                        "text": (f"Inside the {scenery_id}, " f"you find {item_list}."),
                    }
                )

                return responses

            return custom_response

        item_list = format_item_names(visible_names)

        return f"Inside the {scenery_id}, you find {item_list}."

    search_results = []

    for scenery_id, scenery_data in current_area.get(
        "scenery",
        {},
    ).items():
        description = scenery_data["description"]
        scenery_items = scenery_data.get("items", [])

        scenery_state = get_scenery_state(
            location_state,
            scenery_id,
        )

        items_are_visible = not (
            scenery_data.get("openable") and not scenery_state.get("isOpen", False)
        )

        remaining_items = [
            item_id
            for item_id in scenery_items
            if item_id in location_state["itemsAvailable"]
        ]

        if (
            scenery_data.get("hideOnEmpty", False)
            and scenery_items
            and not remaining_items
        ):
            continue

        visible_names = []

        if items_are_visible:
            for item_id in remaining_items:
                item = itemRegistry.get(item_id)

                if item:
                    visible_names.append(get_item_name(item))

        if visible_names:
            item_prefix = scenery_data.get("itemPrefix")

            if item_prefix:
                item_list = format_item_names(visible_names)

                description = f"{description} {item_prefix} {item_list}."

        search_results.append(description)

    if not search_results:
        return "You don't find anything useful here."

    narrator_text = "You search the area and find: " + " ".join(search_results)

    search_voice = current_area.get("searchVoice")

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
