# Item Definition Reference

This document describes the item-definition fields supported by the current
Python game engine. It is a reference for creating content, not a proposal for
item factories or a replacement for the existing Area 1 item files.

The main systems involved are:

- `items/registry.py` — builds the global item registry.
- `game/validators/items.py` — validates registered item definitions.
- `game/itemAccess.py` — resolves names, ambiguity, and container access.
- `game/itemDisplay.py` — formats item names and quantity descriptions.
- `game/handlers/` — executes item commands.
- `game/useActions.py` — executes item-to-item and item-to-scenery USE actions.
- `states/model.py` and `states/validator.py` — create and validate runtime item
  state and ownership.

## Basic definition shape

Every registered item is an ordered `(item ID, definition)` pair:

```python
a1_example_item = (
    "a1_example_item",
    {
        "name": "Example Item",
        "aliases": [
            "example item",
            "item",
        ],
        "description": "A short description of the item.",
        "takeable": True,
        "wearable": False,
    },
)
```

The item ID is the physical identity used by placement, inventory, equipment,
runtime state, interactions, and saves. Two physical copies must have different
IDs even when their definitions are otherwise identical.

Item IDs must be globally unique. Area item IDs use their originating area as a
namespace, such as `a1_house_key_1`. Moving an item to another area does not
change its ID.

## Response shapes

Unless a field is specifically documented as plain text, an item response can
use any standard response shape:

```python
"A narrator response string."
```

```python
{
    "speaker": "narrator",
    "text": "A single response message.",
}
```

```python
[
    {
        "speaker": "narrator",
        "text": "The action occurs.",
    },
    {
        "speaker": "voice",
        "text": "An internal thought.",
    },
]
```

Currently valid item-response speakers are:

- `narrator`
- `voice`
- `system`

Response strings, message text, and response lists must not be empty.

## Identity and description fields

| Field | Value | Required | Used by |
| --- | --- | --- | --- |
| `name` | Non-empty string | Yes | Display formatting, item resolution, inventory, equipment, and responses |
| `aliases` | Non-empty list of unique lowercase strings | Yes | Command item resolution |
| `description` | Non-empty string | No | LOOK/INSPECT outside inventory and fallback inspection text |
| `inspect` | Standard response shape | No | LOOK AT/INSPECT when the item is carried; falls back to `description` |
| `worldDescription` | Non-empty string | No | SEARCH when an item remains in its original world placement |
| `looseDescription` | Non-empty string | No | SEARCH after an item has been dropped or thrown loose |
| `stateDescriptions` | Ordered state-description list | No | LOOK for world or equipped items with matching state |

`description`, `worldDescription`, `looseDescription`, and each
`stateDescriptions[].description` are plain strings rather than response
objects or response lists.

The first matching state description is used:

```python
"stateDescriptions": [
    {
        "requiresState": {
            "isBroken": True,
        },
        "description": "The item has broken into several pieces.",
    },
],
```

Carried items use `inspect` before `description`; they currently do not use
`stateDescriptions`. SEARCH continues to use `worldDescription` and
`looseDescription` independently of LOOK/INSPECT.

## Basic behavior fields

| Field | Value | Default | Used by |
| --- | --- | --- | --- |
| `takeable` | Boolean | `False` | TAKE |
| `wearable` | Boolean | `False` | WEAR and display highlight selection |
| `flammable` | Boolean | Unset/false | Generic USE definition requirements, currently ignition |
| `slot` | Equipment-slot string | None | WEAR, REMOVE, equipment display, and capacity checks |
| `carryCapacity` | Positive integer | None | Adds capacity when a back-slot item is equipped |

Valid equipment slots are:

- `head`
- `chest`
- `outerwear`
- `hands`
- `legs`
- `feet`
- `back`
- `accessory`

`slot` is required when `wearable` is true. `carryCapacity` is valid only on a
wearable back-slot item. Equipped items do not consume normal inventory slots.

`flammable` does nothing by itself. A USE source can require it through
`targetDefinitionRequires`, which prevents resource consumption when the target
does not qualify.

## TAKE, DROP, WEAR, and REMOVE responses

All fields in this section accept a standard response shape.

| Field | Used when |
| --- | --- |
| `takeFail` | TAKE resolves the item, but `takeable` is false |
| `takeResponse` | A normal TAKE succeeds, including confirmed container-bundle acquisition |
| `takeWearResponse` | The exact combined TAKE then WEAR command fully succeeds |
| `mergeResponse` | `mergeOnTake` successfully combines the incoming item into a carried item |
| `takeBlockedResponse` | The player cannot access contents of this item when using TAKE FROM |
| `dropResponse` | DROP succeeds, including confirmed equipped/capacity-changing drops |
| `wearFailResponse` | WEAR resolves the item, but `wearable` is false |
| `wearResponse` | WEAR succeeds, including confirmed capacity-changing swaps |
| `removeResponse` | REMOVE succeeds, including confirmed capacity changes |

`takeWearResponse` replaces the normal TAKE and WEAR success responses only
after both actions complete successfully. Failure and pending-action responses
remain unchanged.

`alreadyWearingResponse` is accepted by the current item validator but is not
read by the current WEAR handler. Do not use it as active content unless the
handler is intentionally extended later.

## Runtime item state

```python
"state": {
    "isOpen": False,
    "matches": 3,
}
```

`state` is an optional dictionary containing the item's initial runtime state.
Each physical item ID receives its own saved state. Common state keys currently
used by item systems include:

- `isOpen` — OPEN/CLOSE and container access.
- `isLocked` — prevents normal OPEN.
- `isSearched` — used by `contentsRequireSearch`.
- Non-negative resource values such as `matches` or `usesRemaining`.

Custom state keys are allowed. Any field that references a state key must use
the exact same spelling and compatible value type.

## EMPTY and SPILL

`EMPTY <item>` works only on carried items that explicitly define
`emptyActions`. `SPILL` is an alias for `EMPTY`. These commands discard the
item's contents without targeting or affecting anything in the location; use
the normal USE interaction system when the contents should affect a target.

```python
"emptyActions": [
    {
        "requiresState": {
            "isFilled": True,
        },
        "effects": {
            "isFilled": False,
        },
        "response": "You pour out the contents.",
    },
],
"emptyFailResponse": "The container is already empty.",
```

The first action whose `requiresState` values match the item's current state is
used. Its `effects` are applied to that item's state only after a match is
found. Requirement and effect keys must exist in the item's initial `state`,
and their value types must match the initial values.

`emptyFailResponse` is optional and accepts a standard response shape. It is
used when the item supports EMPTY but no action matches its current state.

Different liquid types can use a stable string state value:

```python
"state": {
    "liquidType": "empty",
},
```

Filling interactions can set this to values such as `"water"` or `"oil"`, and
separate ordered `emptyActions` can match each value before restoring
`"liquidType": "empty"`.

## Item containers and SEARCH

| Field | Value | Used by |
| --- | --- | --- |
| `container` | Boolean | Allows real items to be placed inside this item |
| `searchable` | Boolean | Enables item SEARCH behavior |
| `openable` | Boolean | Requires `state.isOpen` before contents are accessible |
| `closeable` | Boolean | Enables CLOSE |
| `contentsRequireSearch` | Boolean | Hides contents until SEARCH sets `state.isSearched` |
| `contentsRequiresState` | State-match dictionary | Adds state requirements for content access/search |
| `transferContentsOnTake` | Boolean | TAKE transfers the container and remaining contents into general inventory |

Relationships enforced by validation:

- `transferContentsOnTake=True` requires `container=True`.
- `contentsRequireSearch=True` requires `searchable=True`.
- `mergeOnTake` cannot be combined with `transferContentsOnTake`.

Container contents are placed by the location definition's `itemContents`
mapping. They do not live in a nested carried-inventory structure.

SEARCH response fields accept standard response shapes:

| Field | Used when |
| --- | --- |
| `searchResponse` | The item is not searchable; overrides the normal failure text |
| `searchClosedResponse` | A searchable/openable item is closed |
| `searchBlockedResponse` | `contentsRequiresState` does not match |
| `searchEmptyResponse` | A valid search finds no contained items |

When a valid search finds real contained items, the engine generates the item
list response automatically.

`contentsRequiresState` is used by the runtime access/search systems, but the
current item validator does not yet validate its shape. Use a dictionary.

## OPEN and CLOSE

OPEN and CLOSE work on accessible world, inventory, or equipped items.

| Field | Value | Used when |
| --- | --- | --- |
| `openable` | Boolean | Enables OPEN |
| `closeable` | Boolean | Enables CLOSE |
| `openRequires` | Requirement dictionary | Additional OPEN requirements |
| `closeRequires` | Requirement dictionary | Additional CLOSE requirements |
| `openEffects` | Item-state update dictionary | Applied after OPEN succeeds |
| `closeEffects` | Item-state update dictionary | Applied after CLOSE succeeds |

Supported `openRequires` and `closeRequires` keys are:

```python
{
    "sceneryState": {
        # For an item OPEN/CLOSE action, this matches this item's state.
        "customStateKey": True,
    },
    "inventory": ["registered_item_id"],
    "equipped": ["registered_item_id"],
    "flags": {
        "flagName": True,
    },
}
```

OPEN checks `state.isLocked` and `state.isOpen`, then sets `isOpen=True` before
applying `openEffects`. CLOSE checks `state.isOpen`, sets it to false, and then
applies `closeEffects`.

OPEN/CLOSE response fields accept standard response shapes:

| Field | Used when |
| --- | --- |
| `openFailResponse` | `openable` is false |
| `lockedResponse` | `state.isLocked` is true |
| `alreadyOpenResponse` | `state.isOpen` is already true |
| `openBlockedResponse` | `openRequires` fails |
| `openResponse` | OPEN succeeds |
| `closeFailResponse` | `closeable` is false |
| `alreadyClosedResponse` | `state.isOpen` is already false |
| `closeBlockedResponse` | `closeRequires` fails |
| `closeResponse` | CLOSE succeeds |

The runtime supports the item `openRequires`, `closeRequires`, `openEffects`,
`closeEffects`, and `contentsRequiresState` fields, but the current item
validator does not validate them. Keep these dictionaries simple and test them
carefully when used.

## Interchangeable physical items

```python
"interchangeableGroup": "house_key"
```

`interchangeableGroup` is an optional non-empty string. Multiple separately
registered physical items with the same group:

- Remain separate IDs and separate saved objects.
- Each continue to count toward inventory capacity.
- Display once in inventory with a count such as `House Key (x2)`.
- Avoid inventory ambiguity for USE, DROP, THROW, and WEAR.
- Deterministically select the first matching inventory ID for the action.

World-item ambiguity is unchanged. Matching names alone do not make items
interchangeable. Do not assign the same group to items whose meaningful runtime
state can differ.

This field is independent from `mergeOnTake`.

## Merge-on-TAKE resources

```python
"mergeOnTake": {
    "group": "matchbox",
    "stateKey": "matches",
},
"mergeResponse": (
    "You combine the contents and discard the empty container."
),
```

`mergeOnTake` is explicit opt-in and must contain exactly:

| Field | Requirement |
| --- | --- |
| `group` | Non-empty compatibility-group string |
| `stateKey` | A key containing a non-negative integer in `state` |

When TAKE finds a carried item with the same merge group and state key, it:

1. Reads both items' current runtime quantities.
2. Adds the incoming quantity to the retained carried item.
3. Preserves the retained item's other state values.
4. Removes the incoming physical item from the world and runtime item state.
5. Does not add another inventory slot.
6. Returns `mergeResponse`, or the generic merge response when it is absent.

All members of one merge group must use the same `stateKey`. Merge items must
be takeable and cannot use `transferContentsOnTake`.

## Quantity presentation

```python
"quantityDisplay": {
    "stateKey": "matches",
    "singular": "match",
    "plural": "matches",
    "showInInventory": True,
    "requiresState": {
        "isOpen": True,
    },
},
```

| Field | Requirement | Used by |
| --- | --- | --- |
| `stateKey` | References a non-negative integer in initial `state` | All quantity output |
| `singular` | Non-empty string | LOOK/SEARCH prose when quantity is one |
| `plural` | Non-empty string | LOOK/SEARCH prose for other quantities |
| `requiresState` | Optional state-match dictionary | Controls LOOK/SEARCH quantity prose |
| `showInInventory` | Optional boolean | Shows the bare live number, such as `Matchbox (3)` |

The inventory count is read directly from current runtime state, so merge and
resource consumption are immediately reflected. Inventory display currently
does not apply `requiresState`; that requirement controls the descriptive
sentence added by LOOK, OPEN, and SEARCH.

## Virtual provided uses and resources

An inventory item can provide a virtual source without creating another
physical inventory item:

```python
"providedUses": {
    "match": {
        "aliases": [
            "match",
        ],
        "requiresState": {
            "isOpen": True,
        },
        "resource": {
            "stateKey": "matches",
            "minimum": 1,
            "consume": 1,
        },
        "failResponse": "The matchbox cannot provide a usable match.",
        "targetDefinitionRequires": {
            "flammable": True,
        },
    },
},
```

`providedUses` is a dictionary keyed by a non-empty virtual-use ID. Each entry
supports:

| Field | Requirement |
| --- | --- |
| `aliases` | Non-empty list of lowercase strings used to resolve the virtual source |
| `requiresState` | State values the provider must match |
| `resource.stateKey` | Non-negative integer key in the provider's initial `state` |
| `resource.minimum` | Positive integer required before attempting the interaction |
| `resource.consume` | Positive integer deducted only after successful interaction validation |
| `failResponse` | Standard response returned when provider state/resource requirements fail |
| `targetDefinitionRequires` | Optional dictionary matched against the target's item definition |

The physical provider must be in inventory. If several carried providers match
the same virtual use, the engine asks for clarification instead of silently
choosing one. The resource deduction is committed only when the complete USE
interaction succeeds.

## Physical source definition requirements

A normal physical USE source can define:

```python
"targetDefinitionRequires": {
    "flammable": True,
},
```

This is matched against the target's definition before interaction state or
effects are committed. The field must be a dictionary. A provided virtual use
places the same field inside its `providedUses` entry instead.

## Item-to-item interactions

Interactions are defined on the target item and keyed by either:

- A registered physical source item ID; or
- A virtual-use ID declared by a registered item's `providedUses`.

```python
"interactions": {
    "source_item_or_virtual_use_id": {
        "requires": {
            "sourceItemState": {},
            "sourceItemStateMinimums": {},
            "targetItemState": {},
            "targetItemStateMinimums": {},
            "targetOwnership": "currentLocation",
            "targetPlacement": "loose",
            "player": {},
            "inventory": [],
            "equipped": [],
            "flags": {},
        },
        "effects": {
            "sourceItemState": {},
            "sourceItemStateDeltas": {},
            "targetItemState": {},
            "targetItemStateDeltas": {},
            "player": {},
            "flags": {},
            "destroySource": False,
            "destroyTarget": False,
        },
        "response": "The interaction succeeds.",
        "failResponse": "That will not work right now.",
        "sourceStateFailResponse": "The source is not ready.",
        "targetStateFailResponse": "The target is not ready.",
        "targetLocationFailResponse": "The target must be somewhere else.",
        "targetDefinitionFailResponse": "That kind of item cannot be affected.",
    },
},
```

All interaction response fields accept standard response shapes.

### Interaction requirements

| Field | Meaning |
| --- | --- |
| `sourceItemState` | Exact source-state values |
| `sourceItemStateMinimums` | Positive integer minimums in source state |
| `targetItemState` | Exact target-state values |
| `targetItemStateMinimums` | Positive integer minimums in target state |
| `targetOwnership` | Must be `inventory`, `equipped`, or `currentLocation` |
| `targetPlacement` | Currently supports only `loose` |
| `player` | Required player-state values, such as the current health label |
| `inventory` | Registered item IDs that must be carried |
| `equipped` | Registered item IDs that must be equipped |
| `flags` | Required game-flag values |

`targetPlacement="loose"` means the target must be a loose item in the current
location rather than carried, equipped, or inside/attached to something.

### Interaction effects

| Field | Meaning |
| --- | --- |
| `sourceItemState` | Exact state values applied to the source |
| `sourceItemStateDeltas` | Integer changes applied to numeric source state |
| `targetItemState` | Exact state values applied to the target |
| `targetItemStateDeltas` | Integer changes applied to numeric target state |
| `player` | Player-state values to update after every requirement succeeds |
| `flags` | Game-flag values to update |
| `destroySource` | Removes the selected physical source item |
| `destroyTarget` | Removes only the selected physical target item |

The USE engine previews all requirements, state changes, deltas, and resource
consumption before committing. A failed interaction does not partially mutate
state or consume a provided resource.

An item can support intentional self-use by defining an interaction keyed by
its own physical item ID. For example, `use first aid kit` can apply a player
health update and explicitly set `destroySource=True`. This reuses the normal
item interaction transaction; it does not create a separate self-use engine.

## THROW

```python
"onThrow": {
    "default": {
        "response": "You throw the item onto the ground.",
        "destroyItem": False,
    },
},
```

An item's `onThrow` dictionary currently supports only the `default` action.

| Field | Requirement |
| --- | --- |
| `response` | Required standard response shape |
| `destroyItem` | Optional boolean; false leaves the item loose in the current location |

Target-specific throws are defined by scenery `throwInteractions`, not by the
item's `onThrow` definition.

## Copyable full template

This template shows every active item field. Remove sections the item does not
need. Some combinations are intentionally invalid, so it is a reference rather
than a definition that should be registered unchanged.

```python
a1_example_item = (
    "a1_example_item",
    {
        # Required identity.
        "name": "Example Item",
        "aliases": [
            "example item",
            "item",
        ],

        # LOOK/INSPECT and SEARCH presentation.
        "description": "A short description.",
        "inspect": [
            {
                "speaker": "narrator",
                "text": "A more detailed carried-item inspection.",
            },
        ],
        "worldDescription": "an example item in its original position.",
        "looseDescription": "an example item lying on the ground.",
        "stateDescriptions": [
            {
                "requiresState": {
                    "isBroken": True,
                },
                "description": "The example item is broken.",
            },
        ],

        # Basic physical behavior.
        "takeable": True,
        "wearable": False,
        "flammable": False,

        # Wearable-only fields.
        # "slot": "back",
        # "carryCapacity": 5,

        # Optional container/search behavior.
        "container": False,
        "searchable": False,
        "openable": False,
        "closeable": False,
        "contentsRequireSearch": False,
        "contentsRequiresState": {},
        "transferContentsOnTake": False,

        # Initial per-physical-item state.
        "state": {
            "isOpen": False,
            "isLocked": False,
            "isSearched": False,
            "quantity": 1,
        },

        # Optional carried-item EMPTY/SPILL behavior.
        # "emptyActions": [
        #     {
        #         "requiresState": {"quantity": 1},
        #         "effects": {"quantity": 0},
        #         "response": "You empty the item.",
        #     },
        # ],
        # "emptyFailResponse": "The item is already empty.",

        # Optional OPEN/CLOSE requirements and state updates.
        "openRequires": {},
        "openEffects": {},
        "closeRequires": {},
        "closeEffects": {},

        # Optional inventory ambiguity/display grouping.
        # "interchangeableGroup": "example_group",

        # Optional TAKE resource merging. Do not combine with
        # transferContentsOnTake.
        # "mergeOnTake": {
        #     "group": "example_resource",
        #     "stateKey": "quantity",
        # },

        # Optional quantity text/inventory display.
        # "quantityDisplay": {
        #     "stateKey": "quantity",
        #     "singular": "unit",
        #     "plural": "units",
        #     "showInInventory": True,
        #     "requiresState": {},
        # },

        # Optional virtual source supplied by this carried item.
        # "providedUses": {
        #     "virtual_use_id": {
        #         "aliases": ["virtual use"],
        #         "requiresState": {},
        #         "resource": {
        #             "stateKey": "quantity",
        #             "minimum": 1,
        #             "consume": 1,
        #         },
        #         "failResponse": "The resource is unavailable.",
        #         "targetDefinitionRequires": {},
        #     },
        # },

        # Optional requirements when this physical item is a USE source.
        "targetDefinitionRequires": {},

        # Optional interactions when this item is the USE target.
        "interactions": {
            # "registered_source_or_virtual_use_id": {
            #     "requires": {},
            #     "effects": {},
            #     "response": "The interaction succeeds.",
            #     "failResponse": "That will not work right now.",
            # },
        },

        # Optional action responses. All use standard response shapes.
        "takeFail": "You cannot take it.",
        "takeResponse": "You take the item.",
        "takeWearResponse": "You take and equip the item.",
        # "mergeResponse": "You combine the items.",
        "takeBlockedResponse": "You cannot reach its contents.",
        "dropResponse": "You drop the item.",
        "wearFailResponse": "You cannot wear it.",
        "wearResponse": "You equip the item.",
        "removeResponse": "You remove the item.",
        "searchResponse": "You find nothing useful.",
        "searchClosedResponse": "It is closed.",
        "searchBlockedResponse": "You cannot search it right now.",
        "searchEmptyResponse": "It is empty.",
        "openFailResponse": "You cannot open it.",
        "lockedResponse": "It is locked.",
        "alreadyOpenResponse": "It is already open.",
        "openBlockedResponse": "You cannot open it right now.",
        "openResponse": "You open it.",
        "closeFailResponse": "You cannot close it.",
        "alreadyClosedResponse": "It is already closed.",
        "closeBlockedResponse": "You cannot close it right now.",
        "closeResponse": "You close it.",

        # Optional default THROW behavior.
        "onThrow": {
            "default": {
                "response": "You throw the item onto the ground.",
                "destroyItem": False,
            },
        },
    },
)
```

## Validation checklist

Before registering a new item:

1. Give every physical copy a unique ID.
2. Keep aliases lowercase and unique within the item.
3. Register the item in its area's ordered item list.
4. Place it in exactly one location, container, scenery object, inventory, or
   equipment source as appropriate.
5. Verify every referenced state key exists with the correct initial type.
6. Verify every referenced item/source ID is registered.
7. Use standard response shapes only where the field supports them.
8. Run definition validation, new-game/save validation, and the commands that
   exercise the item.

Do not add a field only because it seems generally useful. New fields require
an engine consumer and validation before they become supported definition data.
