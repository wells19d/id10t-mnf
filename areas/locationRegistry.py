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

area1Locations = {
    "a1_clearing": a1_clearing,
    "a1_fallen_nursery": a1_fallen_nursery,
    "a1_house_1": a1_house_1,
    "a1_house_2": a1_house_2,
    "a1_house_3": a1_house_3,
    "a1_lake_east": a1_lake_east,
    "a1_lake_south": a1_lake_south,
    "a1_massive_tree": a1_massive_tree,
    "a1_road_access": a1_road_access,
    "a1_security_gate": a1_security_gate,
    "a1_silent_grove": a1_silent_grove,
    "a1_stone_ring": a1_stone_ring,
}

locationDefinitionsByArea = {
    "area1": area1Locations,
}

locationRegistry = {}

for area_locations in locationDefinitionsByArea.values():
    for location_id, location_definition in area_locations.items():
        locationRegistry.setdefault(
            location_id,
            location_definition,
        )
