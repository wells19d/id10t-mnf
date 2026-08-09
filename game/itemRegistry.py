itemRegistry = {
    "a1_fallen_branch": {
        "name": "Fallen Branch",
        "aliases": [
            "fallen branch",
            "branch",
            "stick",
        ],
        "description": "A fallen branch from a nearby tree.",
        "worldDescription": (
            "a <em><span class='item-highlight'>fallen branch</span></em> "
            "lying on the ground."
        ),
        "looseDescription": (
            "a <em><span class='item-highlight'>fallen branch</span></em> "
            "lying on the ground."
        ),
        "takeable": True,
        "wearable": False,
        "onThrow": {
            "default": {
                "response": (
                    "You throw the branch. It spins through the air and drops into the grass."
                ),
                "destroyItem": False,
            },
        },
    },
    "a1_rusty_axe": {
        "name": "Rusty Axe",
        "aliases": [
            "rusty axe",
            "axe",
            "hatchet",
        ],
        "description": "A rusty axe with a worn wooden handle.",
        "worldDescription": (
            "a <em><span class='item-highlight'>rusty axe</span></em> "
            "embedded into the base of the massive tree, its blade dulled and handle worn from years of use."
        ),
        "looseDescription": (
            "a <em><span class='item-highlight'>rusty axe</span></em> "
            "lying on the ground."
        ),
        "takeable": True,
        "wearable": False,
        "onThrow": {
            "default": {
                "response": (
                    "You throw the axe. It spins through the air and drops to the ground."
                ),
                "destroyItem": False,
            },
        },
    },
    "a1_wornout_work_gloves": {
        "name": "Work Gloves",
        "aliases": [
            "work gloves",
            "gloves",
        ],
        "description": "A pair of worn out work gloves.",
        "worldDescription": (
            "a pair of worn out <em><span class='item-highlight'>work gloves</span></em> "
            "lying next to the tree base."
        ),
        "looseDescription": (
            "a pair of worn out <em><span class='item-highlight'>work gloves</span></em> "
            "lying on the ground."
        ),
        "takeable": True,
        "wearable": False,
        "wearFailResponse": [
            {
                "speaker": "narrator",
                "text": (
                    "You can't wear the "
                    "<em><span class='item-highlight'>Work Gloves</span></em>."
                ),
            },
            {
                "speaker": "voice",
                "text": "Right... Because massive holes and rips are exactly what protective gloves need.",
            },
        ],
        "onThrow": {
            "default": {
                "response": ("You toss the gloves onto the ground."),
                "destroyItem": False,
            },
        },
    },
}


def get_item_definition_errors():
    errors = []

    for item_id, item_data in itemRegistry.items():
        item_path = f"itemRegistry[{item_id!r}]"

        if not isinstance(item_id, str) or not item_id:
            errors.append(
                f"{item_path} must use a non-empty string ID."
            )

        if not isinstance(item_data, dict):
            errors.append(
                f"{item_path} must be a dictionary."
            )
            continue

        name = item_data.get(
            "name",
        )

        if not isinstance(name, str) or not name.strip():
            errors.append(
                f"{item_path}.name must be a non-empty string."
            )

        aliases = item_data.get(
            "aliases",
        )

        if not isinstance(aliases, list) or not aliases:
            errors.append(
                f"{item_path}.aliases must be a non-empty list."
            )
        else:
            for alias in aliases:
                if not isinstance(alias, str) or not alias.strip():
                    errors.append(
                        f"{item_path}.aliases contains an invalid alias."
                    )
                elif alias != alias.lower():
                    errors.append(
                        f"{item_path}.aliases must use lowercase text: {alias!r}."
                    )

            if (
                all(
                    isinstance(alias, str)
                    for alias in aliases
                )
                and len(aliases) != len(set(aliases))
            ):
                errors.append(
                    f"{item_path}.aliases contains duplicate aliases."
                )

        for boolean_key in [
            "takeable",
            "wearable",
        ]:
            if boolean_key in item_data and not isinstance(
                item_data[boolean_key],
                bool,
            ):
                errors.append(
                    f"{item_path}.{boolean_key} must be a boolean."
                )

        if item_data.get(
            "wearable",
            False,
        ):
            slot = item_data.get(
                "slot",
            )

            if not isinstance(slot, str) or not slot.strip():
                errors.append(
                    f"{item_path}.slot is required for wearable items."
                )

        if "state" in item_data and not isinstance(
            item_data["state"],
            dict,
        ):
            errors.append(
                f"{item_path}.state must be a dictionary."
            )

        if "onThrow" in item_data and not isinstance(
            item_data["onThrow"],
            dict,
        ):
            errors.append(
                f"{item_path}.onThrow must be a dictionary."
            )

    return errors
