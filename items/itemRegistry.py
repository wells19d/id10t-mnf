from items.area1 import area1Items

itemDefinitionsByArea = {
    "area1": area1Items,
}

itemRegistry = {}

for area_items in itemDefinitionsByArea.values():
    itemRegistry.update(
        area_items,
    )
