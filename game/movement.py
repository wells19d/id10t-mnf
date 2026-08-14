from dataclasses import dataclass

from game.handlers.common import (
    currentLocation,
    getSceneryState,
    stateMatches,
)


@dataclass(frozen=True)
class MovementResult:
    destination: str | None = None
    response: object = None

    def __post_init__(self):
        has_destination = self.destination is not None
        has_response = self.response is not None

        if has_destination == has_response:
            raise ValueError(
                "A movement result must contain either a destination or a response."
            )

    @classmethod
    def moved(cls, destination):
        return cls(
            destination=destination,
        )

    @classmethod
    def blocked(cls, response):
        return cls(
            response=response,
        )


directionAliases = {
    "n": "north",
    "north": "north",
    "s": "south",
    "south": "south",
    "e": "east",
    "east": "east",
    "w": "west",
    "west": "west",
}

fullDirections = {
    "north",
    "south",
    "east",
    "west",
}


def exitRequirementsMet(
    exit_data,
    game_state,
):
    requirements = exit_data.get(
        "requires",
        {},
    )

    # No requirements means the exit is available.
    if not requirements:
        return True

    player_state = game_state["player"]

    # Required inventory items.
    for item_id in requirements.get(
        "inventory",
        [],
    ):
        if item_id not in player_state["inventory"]:
            return False

    # Required equipped items.
    for item_id in requirements.get(
        "equipped",
        [],
    ):
        if item_id not in player_state["equipped"]:
            return False

    # Required world or event flags.
    required_flags = requirements.get(
        "flags",
        {},
    )

    if required_flags:
        if not stateMatches(
            game_state["flags"],
            required_flags,
        ):
            return False

    # Required scenery states in the current location.
    required_scenery = requirements.get(
        "sceneryState",
        {},
    )

    if required_scenery:
        location_state = currentLocation(
            game_state,
        )

        for scenery_id, required_state in required_scenery.items():
            scenery_state = getSceneryState(
                location_state,
                scenery_id,
            )

            if not stateMatches(
                scenery_state,
                required_state,
            ):
                return False

    return True


def movePlayer(
    direction,
    location_definition,
    player_state,
    game_state=None,
):
    full_direction = directionAliases.get(
        direction,
    )

    if not full_direction:
        return None

    exit_data = location_definition["exits"].get(
        full_direction,
    )

    if not exit_data:
        return MovementResult.blocked(f"I can't go {full_direction} from here.")

    # Standard exit:
    #
    # "north": "a1_clearing"
    if isinstance(
        exit_data,
        str,
    ):
        next_location = exit_data

    # Conditional exit:
    #
    # "north": {
    #     "location": "admin_grounds",
    #     "requires": {...},
    #     "blockedResponse": "...",
    # }
    elif isinstance(
        exit_data,
        dict,
    ):
        next_location = exit_data.get(
            "location",
        )

        if not next_location:
            return MovementResult.blocked(f"I can't go {full_direction} from here.")

        if game_state is not None:
            if not exitRequirementsMet(
                exit_data,
                game_state,
            ):
                return MovementResult.blocked(
                    exit_data.get(
                        "blockedResponse",
                        f"You can't go {full_direction} from here.",
                    )
                )

    else:
        return MovementResult.blocked(f"I can't go {full_direction} from here.")

    player_state["currentLocation"] = next_location
    player_state["lastDirection"] = full_direction
    player_state["lastShortDirection"] = full_direction[0]

    return MovementResult.moved(
        next_location,
    )


def movePlayerToRoom(
    room_name,
    location_definition,
    player_state,
):
    if not room_name:
        return MovementResult.blocked(
            "I don't know where I want to go.",
        )

    normalized_room_name = room_name.strip().lower()

    room_exits = location_definition.get(
        "roomExits",
        {},
    )

    next_location = None

    for exit_name, destination in room_exits.items():
        if exit_name.strip().lower() == normalized_room_name:
            next_location = destination
            break

    if not next_location:
        return MovementResult.blocked(
            f"I can't go to the {room_name} from here.",
        )

    player_state["currentLocation"] = next_location

    return MovementResult.moved(
        next_location,
    )
