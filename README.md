# Project ID10T: Memory Not Found

A browser-based, Zork-inspired text adventure built with Python, Flask, HTML, CSS, and JavaScript.

~~This is a self-directed final project focused on learning Python through a complete application rather than isolated exercises.~~

This project began as a self-directed way to practice Python fundamentals through a complete application rather than isolated exercises.

After learning and practicing the basics of Python, I decided to expand the original idea into a much larger game. As the project grew, the code moved beyond the concepts I had originally studied and began incorporating more advanced Python, Flask, JavaScript, state management, and application architecture.

At that point, I began relying more heavily on documentation, researched code examples, and adapted implementation patterns while continuing to use the project as a way to understand how those pieces work together in a real application.

---

## Concept

The player wakes in a forest clearing with no memory of who they are or how they arrived.

Through exploration, environmental interaction, puzzles, and recovered memories, the player begins to uncover what happened and why they are there.

The interface is styled like a simple terminal and separates responses into:

- **Player** — commands entered by the player
- **Narrator** — descriptions of the world and results of actions
- **Inner Voice** — occasional thoughts, reactions, hints, or commentary
- **System** — startup, loading, and other game-control messages

---

## Current Gameplay

The game currently supports movement, exploration, inventory management, item interactions, equipment, containers, environmental state, compound commands, and browser-based save recovery.

Example commands include:

```text
look
look at <target>
search
search <target>

take <item>
take <item> from <target>
drop <item>

open <target>
close <target>

use <item> on <target>
throw <item>
throw <item> at <target>

wear <item>
remove <item>
inventory

north / south / east / west
n / s / e / w
```

Common aliases include `grab`, `get`, `pick up`, `inspect`, `examine`, `equip`, and `unequip`.

The parser also supports some compound commands:

```text
take axe and branch
take axe and throw at tree
take hat and wear it
```

Commands are processed from left to right, and a failed action stops the remaining command chain.

The browser also keeps the last 10 commands for Up/Down Arrow history.

---

## World and Content Structure

Locations are stored as data-driven definitions under `areas/`, while pickup items are grouped under `items/`.

Location and item IDs use an area prefix for global uniqueness:

```text
a1_clearing
a1_massive_tree
a1_rusty_axe
a1_watering_can

a2_admin_key
a2_flashlight
```

The prefix is an internal organization convention, not player-visible area state.

Locations can define things such as:

- First-visit narration
- Normal and state-dependent descriptions
- Items and scenery
- Searchable or openable objects
- Persistent scenery state
- Item interactions and effects
- Target-specific throw interactions
- Conditional exits
- Narrator and Inner Voice responses

The goal is for most future game content to be created through location and item definitions instead of adding one-off engine logic.

---

## Runtime State

The game tracks persistent runtime state for:

- Current location
- Visited locations
- Inventory and equipped items
- Item state
- Scenery state
- Item placement
- World and event flags

For example, an item can track whether it has changed:

```python
"state": {
    "filled": False,
}
```

Scenery can track conditions such as:

```python
"state": {
    "isOpen": False,
    "isLocked": True,
    "isBroken": False,
}
```

This allows the world to react to what the player has already done without hardcoding every puzzle directly into the command handlers.

---

## Save and Recovery

The game automatically stores the current game state in browser `localStorage`.

There is currently one save per browser profile rather than manual save slots.

When the game opens:

- A new game begins if no valid save exists
- An existing save can be resumed
- Invalid or incompatible development saves are rejected safely
- Temporary server or network failures do not erase a valid save
- Failed browser-storage writes are reported instead of silently pretending progress was saved

Game-control commands include:

```text
load
load save
new
new game
quit
```

---

## Project Structure

```text
areas/
├── a1_clearing.py
├── a1_fallen_nursery.py
├── a1_house_1.py
├── ...
└── locationRegistry.py

game/
├── commandParser.py
├── definitionValidator.py
├── failedActions.py
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

items/
├── area1.py
└── itemRegistry.py

states/
└── gameState.py

static/
├── game.js
└── style.css
```

The engine separates command parsing, movement, validation, action handlers, content definitions, and runtime state so new areas can reuse the same underlying systems.

---

## Development

Run the project with:

```bash
python start.py
```

or:

```bash
python3 start.py
```

The launcher starts Flask in debug mode, opens the browser, and supports development reloads.

Definition validation runs at startup so malformed location or item data can fail early during development instead of causing errors later during gameplay.

---

## Current Progress

The underlying game engine and state systems are largely in place.

Current development is focused on **Area 1: The Forest**, including its narrative, locations, scenery, items, puzzles, and progression into Area 2.

Implemented systems currently include:

- Terminal-style browser UI
- Flask backend
- Location movement and conditional exits
- Command parsing, aliases, and compound commands
- Inventory and equipment
- Item/scenery interactions
- Persistent item and scenery state
- Searchable and openable scenery
- State-dependent descriptions
- Automatic browser saving and recovery
- Definition validation
- Development hot reload

---

## Screenshots

![Screenshot 1](ss/ss1.png)

![Screenshot 2](ss/ss2.png)
