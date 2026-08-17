# Project ID10T: Memory Not Found

A browser-based, Zork-inspired text adventure.

~~This is a self-directed final project focused on learning Python through a complete application rather than isolated exercises.~~

This project began as a self-directed way to practice Python fundamentals through a complete application rather than isolated exercises.

As the project expanded, its state management, interactions, and application architecture grew well beyond the original Python-learning scope. The existing Python/Flask version remains in the repository as a working reference, but active development is now restarting the game in **React and JavaScript using Redux, reducers, and Redux Saga**.

The goal of the shift is to build a stronger, cleaner state-management system that better fits the growing complexity of the game while keeping the same text-based interface, world design, and data-driven gameplay direction.

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

The completed Python reference implementation supports movement, exploration, inventory management, item interactions, equipment, containers, environmental state, compound commands, and browser-based save recovery.

The React/Redux version is now being rebuilt from that gameplay foundation rather than directly translated from the Python architecture.

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

The Python reference implementation tracks persistent runtime state for:

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
python/
├── areas/
├── game/
├── items/
├── states/
├── static/
├── templates/
├── app.py
└── start.py

react/
├── src/
├── public/
├── package.json
└── ...

images/
maps/
ss/
z-sandbox/
```

`python/` contains the previous Flask/Python implementation and is retained primarily as a working gameplay and architecture reference.

`react/` is the active project. It will use React, JavaScript, Redux reducers, and Redux Saga for application and game-state management.

Shared design/reference material remains at the repository root.


## Development

The active React project runs from:

```bash
cd react
yarn start
```

The previous Python implementation can still be run independently for reference:

```bash
cd python
python3 start.py
```

or on Windows:

```bash
cd python
python start.py
```

The two implementations are independent. The React version will use its own browser `localStorage` save data and will not overwrite the Python save.


## Current Progress

**Area 1: The Forest is mechanically complete in the Python reference implementation.**

Active development has shifted to rebuilding the project in React/JavaScript with Redux state management. The Python version is no longer the active development target and will be used mainly to reference established gameplay behavior, content, puzzles, and interaction rules.

The React version is being rebuilt deliberately rather than mechanically ported. State shape, reducers, sagas, actions, selectors, and interaction flow may change where a cleaner Redux-based design better fits the project.

The overall goal remains the same: a reusable, data-driven text-adventure engine where future areas and items can be created primarily through definitions rather than one-off engine logic.


## Screenshots

![Screenshot 1](ss/ss1.png)

![Screenshot 2](ss/ss2.png)
