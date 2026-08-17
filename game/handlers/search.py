from game.handlers.common import (
    WORLD_ITEM_PLACEMENT,
    addQuantityText,
    canAccessSceneryContents,
    findScenery,
    formatNames,
    currentLocation,
    displayName,
    getItemStateSnapshot,
    containerItems,
    sceneryItems,
    getSceneryState,
    visibleItemIds,
    normalizeResponseMessages,
    resolveItem,
    stateMatches,
)
from game.itemDisplay import getStateDescription
from items.registry import itemRegistry


def formatSearchResults(search_results):
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


def _searchItem(
    target,
    item_id,
    item,
    location_state,
    game_state,
):
    item_state = getItemStateSnapshot(
        game_state,
        item_id,
    )

    if not item.get(
        "searchable",
        False,
    ):
        inspect_state_response = getStateDescription(
            item,
            item_state,
            "inspectState",
        )

        if inspect_state_response:
            return addQuantityText(
                inspect_state_response,
                item,
                item_state,
            )

        return item.get(
            "searchResponse",
            f"You don't find anything useful in the {target}.",
        )

    if item.get("openable") and not item_state.get(
        "isOpen",
        False,
    ):
        return item.get(
            "searchClosedResponse",
            f"The {target} is closed.",
        )

    if not stateMatches(
        item_state,
        item.get(
            "contentsRequiresState",
            {},
        ),
    ):
        return item.get(
            "searchBlockedResponse",
            f"You can't search the {target} right now.",
        )

    item_state["isSearched"] = True
    game_state["itemStates"][item_id] = item_state
    contained_item_ids = containerItems(
        location_state,
        item_id,
    )

    if contained_item_ids:
        contained_item_names = [
            displayName(
                itemRegistry[contained_item_id],
            )
            for contained_item_id in contained_item_ids
        ]
        response = (
            f"You search the {target} and find "
            f"{formatNames(contained_item_names)}."
        )
    else:
        response = item.get(
            "searchEmptyResponse",
            f"You search the {target} but find nothing useful.",
        )

    return addQuantityText(
        response,
        item,
        item_state,
    )


def _searchScenery(
    scenery_id,
    scenery_data,
    location_state,
):
    if not scenery_data.get(
        "searchable",
        False,
    ):
        return scenery_data.get(
            "searchResponse",
            f"You don't find anything useful in the {scenery_id}.",
        )

    scenery_state = getSceneryState(
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
    if not canAccessSceneryContents(
        scenery_data,
        scenery_state,
    ):
        return scenery_data.get(
            "searchBlockedResponse",
            f"You can't search the {scenery_id} right now.",
        )

    item_ids = sceneryItems(
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
                displayName(
                    item,
                )
            )

    if not item_names:
        return scenery_data.get(
            "searchEmptyResponse",
            f"You search the {scenery_id} but find nothing useful.",
        )

    item_list = formatNames(
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


def _searchTarget(
    target,
    location_definition,
    location_state,
    game_state,
):
    scenery_id, scenery_data = findScenery(
        target,
        location_definition,
    )

    if scenery_data:
        return _searchScenery(
            scenery_id,
            scenery_data,
            location_state,
        )

    accessible_items = (
        visibleItemIds(
            location_definition,
            game_state,
        )
        + game_state["player"]["inventory"]
        + game_state["player"]["equipped"]
    )
    item_id, clarification = resolveItem(
        target,
        accessible_items,
    )

    if clarification:
        return clarification

    item = itemRegistry.get(
        item_id,
    )

    if not item:
        return f"I don't see a {target} here."

    return _searchItem(
        target,
        item_id,
        item,
        location_state,
        game_state,
    )


def _searchArea(
    location_definition,
    location_state,
):
    # Search only for visible/discoverable items in
    # the current location. General scenery descriptions
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
                    displayName(
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
                        displayName(
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
        scenery_data = location_definition.get(
            "scenery",
            {},
        ).get(
            placement,
        )

        if not scenery_data:
            continue

        scenery_state = getSceneryState(
            location_state,
            placement,
        )

        # Items inside containers should not appear in
        # a general location search. The player must search
        # the container directly.
        if scenery_data.get(
            "openable",
            False,
        ):
            continue

        # Other state requirements may also hide or
        # block access to an attached item.
        if not canAccessSceneryContents(
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
                    displayName(
                        item,
                    ),
                ),
            )

        search_results.append(
            item_description,
        )

    if not search_results:
        return "You don't find anything useful here."

    formatted_results = formatSearchResults(
        search_results,
    )

    narrator_text = "You search the area and find " f"{formatted_results}."

    search_voice = location_definition.get(
        "searchVoice",
    )

    if not search_voice:
        return narrator_text

    search_voice_messages = normalizeResponseMessages(
        search_voice,
        default_speaker="voice",
    )

    return [
        {
            "speaker": "narrator",
            "text": narrator_text,
        },
        *search_voice_messages,
    ]


def handleSearch(command, location_definition, game_state):
    target = command["target"] or command["object"]

    location_state = currentLocation(
        game_state,
    )

    if target:
        return _searchTarget(
            target,
            location_definition,
            location_state,
            game_state,
        )

    return _searchArea(
        location_definition,
        location_state,
    )
