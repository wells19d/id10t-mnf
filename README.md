# Project ID10T: A Memory Not Found

Project ID10T: A Memory Not Found — A browser-based, text adventure built with Python and Flask.

This project serves as a self-directed final project for learning and applying the fundamentals of Python through a larger, complete application.

---

## Project Goal

The goal of this project is to strengthen my understanding of Python by building a playable application instead of working only through isolated lessons and exercises.

The project currently focuses on:

- Python functions and modules
- Dictionaries, lists, and application state
- Flask routes and JSON responses
- Parsing text commands
- Reusable action handlers
- Movement between connected locations
- Inventory and item management
- Interactive scenery and containers
- Connecting a Python backend to an HTML, CSS, and JavaScript interface

The game is intentionally text-based so the primary focus remains on Python, application structure, and game logic.

---

## Concept

The player wakes with no memory of who they are or how they arrived.

Through exploration, environmental interaction, and puzzle solving, the player begins uncovering information about the world and their own past.

The game is inspired by classic text adventures such as Zork, but runs through a browser-based terminal interface.

---

## Presentation

The interface is designed to resemble a simple terminal.

Game output is divided between:

- **Player** — commands entered by the person playing
- **Narrator** — descriptions of the world and results of actions
- **Inner Voice** — occasional thoughts, reactions, hints, or commentary from the character

Most actions only require a Narrator response. The Inner Voice is used only when it adds something meaningful to the moment.

---

## Command System

The player interacts with the game by entering text commands.

Current command types include:

    look
    look at <target>

    search
    search <target>

    open <target>
    close <target>

    take <item>
    take <item> from <target>

    throw <item>
    throw <item> at <target>

    use <item>
    use <item> on <target>

    wear <item>

    inventory

Movement supports full directions and short aliases:

    north
    south
    east
    west

    n
    s
    e
    w

Several command aliases are also supported:

    grab
    get
    pick up
    inspect
    examine
    equip

The parser separates each command into its verb, object, target, and additional values before sending it to the appropriate handler.

---

## World and Location System

The game world is divided into connected locations.

Each location can define:

- A first-visit introduction
- A normal location description
- Available exits
- Visible scenery
- Items
- Searchable objects
- Openable and closeable containers
- Location-specific state
- Optional Narrator and Inner Voice responses

Indoor and outdoor locations use the same general system.

Interior sections can be connected like any other location while still containing their own scenery, items, interactions, containers, and exits.

---

## Items

Items are stored in a central registry and use unique internal IDs.

This allows the game to distinguish between multiple objects that may share similar names or aliases.

For example, the player may enter:

    take axe

If only one matching item is available, the action continues normally.

If multiple matching items are available, the game asks the player to be more specific:

    Which axe do you mean?

The player can then enter a more precise command:

    take rusty axe

The game stores the internal item ID while displaying the readable item name to the player.

---

## Scenery and Containers

Scenery represents visible parts of a location that may be examined or interacted with but are not necessarily inventory items.

Scenery can support:

- Aliases
- Descriptions
- Failed interaction responses
- Attached items
- Search behavior
- Open and closed states
- Optional Narrator and Inner Voice responses

Containers can hold items that remain hidden until the container is opened and searched.

Changing state is stored separately from the location definition so objects can remain open, closed, searched, emptied, or otherwise changed after the player interacts with them.

---

## Look and Search

The `look` and `search` commands serve different purposes.

`look` returns the main description of the current location.

`look at <target>` examines a specific visible item or scenery object.

`search` returns visible scenery and discoverable items within the current location.

`search <target>` searches a specific object or container.

Search results respond to the current game state. Items that have been taken no longer appear, closed containers hide their contents, and scenery can be removed from search results when it no longer contains anything relevant.

---

## Response System

Handlers can return either a standard Narrator response or a sequence containing both Narrator and Inner Voice messages.

Most actions use a single Narrator response.

The usual response flow is:

    Narrator
    Inner Voice

A second Narrator response is reserved for a separate event or result rather than continuing the same action unnecessarily.

---

## Current Backend Structure

    game/
    ├── commandParser.py
    ├── failedActions.py
    ├── itemRegistry.py
    ├── movement.py
    ├── parserUtils.py
    └── handlers/
        ├── __init__.py
        ├── common.py
        ├── inventory.py
        ├── look.py
        ├── open_close.py
        ├── search.py
        ├── take.py
        ├── throw.py
        ├── use.py
        └── wear.py

Shared helper functions are kept in `handlers/common.py`, while each action handler is stored in its own file.

This keeps the command system easier to update as new mechanics are added.

---

## Current Progress

Completed or currently working:

- Flask application setup
- Browser-based terminal interface
- Player, Narrator, and Inner Voice display
- Command parsing and aliases
- Directional movement
- First-visit and repeat-visit location behavior
- Central game state
- Central item registry
- Unique internal item IDs
- Inventory display
- Ambiguous item handling
- Interactive scenery
- Searchable objects and containers
- Open and close states
- Taking items from locations and containers
- Throw, use, and wear handlers
- Optional custom Narrator and Inner Voice responses
- Handler files separated by action

---

## Next Steps

The next stage is focused on writing and connecting the actual world content.

This includes:

- Finalizing location descriptions
- Defining scenery and items for each location
- Building interior locations
- Expanding interaction responses
- Adding environmental puzzles
- Connecting progression between areas
- Refining command behavior and failed-action responses
- Continuing to clean up and simplify the game structure as it grows

---

## Running the Project

From the project folder, run:

    python start.py

On systems that use `python3`:

    python3 start.py

If Flask is not installed, the launcher installs it automatically and then starts the game.

## Screenshots

## Screenshots

![Screenshot 1](ss/ss1.png)

![Screenshot 2](ss/ss2.png)
