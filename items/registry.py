from items.area1 import area1Items

itemDefinitionsByArea = {
    "area1": area1Items,
}


def buildItemRegistry(definitions_by_area):
    if not isinstance(definitions_by_area, dict):
        raise ValueError(
            "Item definitions must be grouped in a dictionary."
        )

    registry = {}
    sources = {}
    duplicate_errors = []

    for area_id, area_items in definitions_by_area.items():
        if not isinstance(area_id, str) or not area_id:
            raise ValueError(
                "Item definition groups must use non-empty string IDs."
            )

        if not isinstance(area_items, (list, tuple)):
            raise ValueError(
                f"Item definitions for {area_id!r} must be an ordered list."
            )

        for index, entry in enumerate(area_items):
            entry_path = f"itemDefinitionsByArea[{area_id!r}][{index}]"

            if not isinstance(entry, (list, tuple)) or len(entry) != 2:
                raise ValueError(
                    f"{entry_path} must contain an item ID and definition."
                )

            item_id, item_definition = entry

            if not isinstance(item_id, str) or not item_id:
                raise ValueError(
                    f"{entry_path} must use a non-empty string item ID."
                )

            if item_id in sources:
                duplicate_errors.append(
                    f"Item ID {item_id!r} is defined in both "
                    f"{sources[item_id]!r} and {area_id!r}."
                )
                continue

            sources[item_id] = area_id
            registry[item_id] = item_definition

    if duplicate_errors:
        raise ValueError(
            "Duplicate item definitions:\n"
            + "\n".join(
                f"- {error}"
                for error in duplicate_errors
            )
        )

    return registry


itemRegistry = buildItemRegistry(
    itemDefinitionsByArea,
)
