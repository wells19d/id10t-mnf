# Project ID10T: Memory Not Found

A browser-based, Zork-inspired text adventure built with Python, Flask, HTML, CSS, and JavaScript.

This is a self-directed final project focused on learning Python through a complete application rather than isolated exercises.

---

## Concept

The player wakes in a forest clearing with no memory of who they are or how they arrived.

Through exploration, environmental interaction, puzzles, and recovered memories, the player begins to uncover what happened and why they are there.

The interface is styled like a simple terminal and separates responses into:

- **Player** — commands entered by the player
- **Narrator** — descriptions of the world and results of actions
- **Inner Voice** — occasional thoughts, reactions, hints, or commentary

---

## Current Commands

```text
look
look at <target>

search
search <target>

open <target>
close <target>

take <item>
take <item> from <target>
drop <item>

throw <item>
throw <item> at <target>

use <item> on <target>

wear <item>

inventory

north / south / east / west
n / s / e / w
```

Aliases currently include:

```text
grab
get
pick up
inspect
examine
equip
```

The browser also supports terminal-style command history:

- **Up Arrow** — previous command
- **Down Arrow** — newer command
- Keeps the last **10 commands**

---

## World Structure

Each location is stored in its own file under `areas/`.

An area can define:

- First-visit narration
- Normal description
- LOOK response
- Loose pickup items
- Permanent/interactable scenery
- Searchable objects
- Openable/closeable containers
- Items stored inside scenery
- Exits to other locations
- Optional Narrator and Inner Voice responses

### Items vs. Scenery

Pickup items are defined once in `game/itemRegistry.py`.

The area file only decides where that item starts:

```python
"items": [
    "a1_fallen_branch",
]
```

Items inside a container are placed on the scenery object:

```python
"scenery": {
    "cupboard": {
        "openable": True,
        "closeable": True,
        "searchable": True,
        "items": [
            "a1_house_key",
        ],
    },
}
```

Permanent objects such as trees, doors, safes, cupboards, calendars, or objects that cannot be taken exist only as scenery in the area file.

Runtime state is created automatically as the player interacts with the world, so new items and scenery no longer need to be manually added to `gameState.py`.

---

## Item Behavior

Items can support:

- Taking
- Dropping
- Looking/examining
- Wearing
- Throwing
- Throwing at scenery
- Using on scenery
- Being destroyed after an action
- Setting game flags after successful interactions

Example:

```python
"a1_fallen_branch": {
    "name": "Fallen Branch",
    "aliases": ["fallen branch", "branch", "stick"],
    "description": "A fallen branch from a nearby tree.",
    "worldDescription": "A fallen branch lies on the ground.",
    "takeable": True,
    "wearable": False,
    "onThrow": {
        "default": {
            "response": (
                "You throw the branch. It spins through the air "
                "and drops into the grass."
            ),
            "destroyItem": False,
        },
    },
},
```

If an item survives being thrown or dropped, it becomes a loose item in the current location and can be picked up again.

---

## Look and Search

`LOOK` describes the current location.

`LOOK AT <target>` examines a specific item or scenery object.

`SEARCH` looks for loose items and scenery in the current location.

`SEARCH <target>` searches a specific object or container.

Search results react to the current game state. Taken items disappear, dropped items appear in their new location, and closed containers hide their contents.

---

## Backend Structure

```text
game/
├── commandParser.py
├── failedActions.py
├── itemRegistry.py
├── movement.py
├── parserUtils.py
└── handlers/
    ├── common.py
    ├── drop.py
    ├── inventory.py
    ├── look.py
    ├── open_close.py
    ├── search.py
    ├── take.py
    ├── throw.py
    ├── use.py
    └── wear.py
```

Action logic is separated into handlers while shared lookup/state helpers live in `handlers/common.py`.

---

## Development Workflow

Run the project with:

```bash
python start.py
```

or:

```bash
python3 start.py
```

The launcher:

- Installs Flask if needed
- Starts Flask in debug mode
- Opens the game in the browser
- Automatically reloads Python changes during development
- Refreshes the browser after the Flask server reloads
- Shuts down cleanly with `Ctrl+C`

This makes editing area narration and game data much closer to a live-development workflow.

---

## Current Progress

The project currently supports:

- Flask backend and browser terminal UI
- Area-to-area movement
- First-visit and repeat-visit behavior
- Command parsing and aliases
- Central item registry
- Runtime world state
- Inventory
- Taking and dropping items
- Throwing items
- Using items on scenery
- Wearable items
- Searchable scenery
- Openable/closeable containers
- Items stored inside containers
- Custom success and failure responses
- Optional Inner Voice responses
- Terminal-style command history
- Development hot reload

Current work is focused on building the actual narrative, scenery, items, and puzzles for **Area 1: The Forest**.

---

## Screenshots

![Screenshot 1](ss/ss1.png)

![Screenshot 2](ss/ss2.png)
