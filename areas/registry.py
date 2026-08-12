from areas.a1_clearing import a1_clearing
from areas.a1_fallen_nursery import a1_fallen_nursery
from areas.a1_house_1 import a1_house_1
from areas.a1_house_2 import a1_house_2
from areas.a1_house_3 import a1_house_3
from areas.a1_lake_east import a1_lake_east
from areas.a1_lake_south import a1_lake_south
from areas.a1_massive_tree import a1_massive_tree
from areas.a1_road_access import a1_road_access
from areas.a1_security_gate import a1_security_gate
from areas.a1_silent_grove import a1_silent_grove
from areas.a1_stone_ring import a1_stone_ring

area1Locations = [
    ("a1_clearing", a1_clearing),
    ("a1_fallen_nursery", a1_fallen_nursery),
    ("a1_house_1", a1_house_1),
    ("a1_house_2", a1_house_2),
    ("a1_house_3", a1_house_3),
    ("a1_lake_east", a1_lake_east),
    ("a1_lake_south", a1_lake_south),
    ("a1_massive_tree", a1_massive_tree),
    ("a1_road_access", a1_road_access),
    ("a1_security_gate", a1_security_gate),
    ("a1_silent_grove", a1_silent_grove),
    ("a1_stone_ring", a1_stone_ring),
]

locationDefinitionsByArea = {
    "area1": area1Locations,
}


def buildLocationRegistry(definitions_by_area):
    if not isinstance(definitions_by_area, dict):
        raise ValueError(
            "Location definitions must be grouped in a dictionary."
        )

    registry = {}
    sources = {}
    duplicate_errors = []

    for area_id, area_locations in definitions_by_area.items():
        if not isinstance(area_id, str) or not area_id:
            raise ValueError(
                "Location definition groups must use non-empty string IDs."
            )

        if not isinstance(area_locations, (list, tuple)):
            raise ValueError(
                f"Location definitions for {area_id!r} must be an ordered list."
            )

        for index, entry in enumerate(area_locations):
            entry_path = f"locationDefinitionsByArea[{area_id!r}][{index}]"

            if not isinstance(entry, (list, tuple)) or len(entry) != 2:
                raise ValueError(
                    f"{entry_path} must contain a location ID and definition."
                )

            location_id, location_definition = entry

            if not isinstance(location_id, str) or not location_id:
                raise ValueError(
                    f"{entry_path} must use a non-empty string location ID."
                )

            if location_id in sources:
                duplicate_errors.append(
                    f"Location ID {location_id!r} is defined in both "
                    f"{sources[location_id]!r} and {area_id!r}."
                )
                continue

            sources[location_id] = area_id
            registry[location_id] = location_definition

    if duplicate_errors:
        raise ValueError(
            "Duplicate location definitions:\n"
            + "\n".join(
                f"- {error}"
                for error in duplicate_errors
            )
        )

    return registry


locationRegistry = buildLocationRegistry(
    locationDefinitionsByArea,
)
