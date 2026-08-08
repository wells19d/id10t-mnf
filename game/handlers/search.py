from game.handlers.common import (
    WORLD_ITEM_PLACEMENT,
    can_access_scenery_contents,
    find_scenery,
    format_item_names,
    get_current_location_state,
    get_item_display_name,
    get_items_in_scenery,
    get_scenery_state,
)
from game.itemRegistry import itemRegistry


def format_search_results(search_results):
    # Clean ending punctuation from each fragment so
    # SEARCH can build one properly formatted sentence.
    cleaned_results = []

    for result in search_results:
        cleaned_result = result.strip().rstrip(".!?")

        if cleaned_result:
            cleaned_results.append(
                cleaned_result,
            )

    if not cleaned_results:
        return ""

    # One result:
    # A rusty axe lying on the ground.
    if len(cleaned_results) == 1:
        return cleaned_results[0]

    # Two results:
    # A rusty axe lying on the ground and
    # a fallen branch lying on the ground.
    if len(cleaned_results) == 2:
        return f"{cleaned_results[0]} " f"and {cleaned_results[1]}"

    # Three or more results:
    # A rusty axe lying on the ground,
    # a branch near the tree,
    # and a cupboard nailed to the trunk.
    return ", ".join(cleaned_results[:-1]) + f", and {cleaned_results[-1]}"


def handle_search(command, current_area, game_state):
    target = command["target"] or command["object"]

    location_state = get_current_location_state(
        game_state,
    )

    # SEARCH <target>
    if target:
        scenery_id, scenery_data = find_scenery(
            target,
            current_area,
        )

        if not scenery_data:
            return f"I don't see a {target} here."

        if not scenery_data.get(
            "searchable",
            False,
        ):
            return scenery_data.get(
                "searchResponse",
                f"You don't find anything useful in the {scenery_id}.",
            )

        scenery_state = get_scenery_state(
            location_state,
            scenery_id,
        )

        # Closed containers must be opened first.
        if scenery_data.get("openable") and not scenery_state.get(
            "isOpen",
            False,
        ):
            return scenery_data.get(
                "searchClosedResponse",
                f"The {scenery_id} is closed.",
            )

        # Other scenery conditions may also block
        # access to its contents.
        if not can_access_scenery_contents(
            scenery_data,
            scenery_state,
        ):
            return scenery_data.get(
                "searchBlockedResponse",
                f"You can't search the {scenery_id} right now.",
            )

        item_ids = get_items_in_scenery(
            location_state,
            scenery_id,
        )

        scenery_state["isSearched"] = True

        if not item_ids:
            return scenery_data.get(
                "searchEmptyResponse",
                f"You search the {scenery_id} but find nothing useful.",
            )

        item_names = []

        for item_id in item_ids:
            item = itemRegistry.get(
                item_id,
            )

            if item:
                item_names.append(
                    get_item_display_name(
                        item,
                    )
                )

        if not item_names:
            return scenery_data.get(
                "searchEmptyResponse",
                f"You search the {scenery_id} but find nothing useful.",
            )

        item_list = format_item_names(
            item_names,
        )

        custom_response = scenery_data.get(
            "searchResponse",
        )

        if custom_response:
            if isinstance(
                custom_response,
                list,
            ):
                responses = list(
                    custom_response,
                )

                responses.append(
                    {
                        "speaker": "narrator",
                        "text": (f"You find {item_list}."),
                    }
                )

                return responses

            return custom_response

        return f"You search inside the {scenery_id} " f"and find {item_list}."

    # SEARCH
    #
    # Search only for visible/discoverable items in
    # the current area. General scenery descriptions
    # are not returned here.
    search_results = []

    for item_id, placement in location_state["items"].items():
        item = itemRegistry.get(
            item_id,
        )

        if not item:
            continue

        # Item is still in its original world placement.
        if placement == WORLD_ITEM_PLACEMENT:
            description = item.get(
                "worldDescription",
                item.get(
                    "description",
                    get_item_display_name(
                        item,
                    ),
                ),
            )

            search_results.append(
                description,
            )

            continue

        # Item was dropped or thrown loose.
        if placement is None:
            description = item.get(
                "looseDescription",
                item.get(
                    "worldDescription",
                    item.get(
                        "description",
                        get_item_display_name(
                            item,
                        ),
                    ),
                ),
            )

            search_results.append(
                description,
            )

            continue

        # Item is attached to / associated with scenery.
        scenery_data = current_area.get(
            "scenery",
            {},
        ).get(
            placement,
        )

        if not scenery_data:
            continue

        scenery_state = get_scenery_state(
            location_state,
            placement,
        )

        # Items inside containers should not appear in
        # a general area search. The player must search
        # the container directly.
        if scenery_data.get(
            "openable",
            False,
        ):
            continue

        # Other state requirements may also hide or
        # block access to an attached item.
        if not can_access_scenery_contents(
            scenery_data,
            scenery_state,
        ):
            continue

        # Scenery can optionally provide a special
        # description for an item attached to it.
        item_description = scenery_data.get(
            "itemDescriptions",
            {},
        ).get(
            item_id,
        )

        # Otherwise use the item's normal world description.
        if not item_description:
            item_description = item.get(
                "worldDescription",
                item.get(
                    "description",
                    get_item_display_name(
                        item,
                    ),
                ),
            )

        search_results.append(
            item_description,
        )

    if not search_results:
        return "You don't find anything useful here."

    formatted_results = format_search_results(
        search_results,
    )

    narrator_text = "You search the area and find " f"{formatted_results}."

    search_voice = current_area.get(
        "searchVoice",
    )

    if not search_voice:
        return narrator_text

    if isinstance(
        search_voice,
        str,
    ):
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
