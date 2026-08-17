a1_stone_ring = {
    "name": "Stone Ring",
    "intro": [
        {
            "speaker": "narrator",
            "text": (
                "A narrow path opens into a small forest clearing centered around "
                "a low, moss-covered <em><span class='area-highlight'>Stone Ring</span></em>. "
                "The fire inside has burned down recently, leaving a bed of hot coals "
                "that still radiates heat into the damp air. Among the blackened wood "
                "are warped scraps of something deliberately burned, as though someone "
                "tried to destroy a handful of personal belongings. Paths lead south "
                "and west."
            ),
        },
        {
            "speaker": "voice",
            "text": (
                "There might still be something worth saving in there... if only I had "
                "something that could hold enough water to cool it down."
            ),
        },
    ],
    "description": (
        "A bed of hot coals smolders inside the moss-covered "
        "<em><span class='area-highlight'>Stone Ring</span></em>. Blackened scraps "
        "among the coals suggest someone tried to burn several personal belongings. "
        "Paths lead south and west."
    ),
    "stateDescriptions": [
        {
            "requires": {
                "sceneryState": {
                    "coals": {
                        "isCooled": True,
                    },
                },
            },
            "description": (
                "Cold gray ash fills the moss-covered "
                "<em><span class='area-highlight'>Stone Ring</span></em>. The remains "
                "of several burned personal belongings lie exposed within it. Paths "
                "lead south and west."
            ),
        },
    ],
    "items": [],
    "scenery": {
        "coals": {
            "aliases": [
                "hot coals",
                "coals",
                "fire",
                "fire pit",
                "stone ring",
                "ash",
                "cold ash",
                "ashes",
            ],
            "description": (
                "The fire has collapsed into a dense bed of glowing coals. Heat rolls "
                "off them, and warped fragments buried beneath the charred wood look "
                "like the remains of personal belongings."
            ),
            "stateDescriptions": [
                {
                    "requiresState": {
                        "isCooled": True,
                    },
                    "description": (
                        "The coals have become cold gray ash. Half-burned fragments and "
                        "the outlines of several small objects are now safe to search."
                    ),
                },
            ],
            "searchable": True,
            "state": {
                "isCooled": False,
            },
            "contentsRequiresState": {
                "isCooled": True,
            },
            "searchBlockedResponse": [
                {
                    "speaker": "narrator",
                    "text": (
                        "The heat forces you back before you can search through the "
                        "coals. Anything buried there will have to wait until they are "
                        "cooled."
                    ),
                },
                {
                    "speaker": "voice",
                    "text": (
                        "If only I had something that could carry enough water to put "
                        "these coals out."
                    ),
                },
            ],
            "searchEmptyResponse": (
                "You sift through the cold ash again, but find nothing else worth taking."
            ),
            "items": [
                "a1_house_key_1",
                "a1_silver_locket",
                "a1_wedding_ring",
            ],
            "itemDescriptions": {
                "a1_house_key_1": (
                    "a tarnished <em><span class='item-highlight'>house key</span></em> "
                    "partly buried in the cold ash"
                ),
                "a1_silver_locket": (
                    "a blackened <em><span class='item-highlight'>silver locket</span></em> "
                    "resting among the burned scraps"
                ),
                "a1_wedding_ring": (
                    "a <em><span class='item-highlight'>wedding ring</span></em> "
                    "glinting faintly through the ash"
                ),
            },
            "interactions": {
                "a1_watering_can": {
                    "requires": {
                        "itemState": {
                            "liquidType": "water",
                        },
                        "sceneryState": {
                            "isCooled": False,
                        },
                    },
                    "effects": {
                        "sceneryState": {
                            "isCooled": True,
                        },
                        "destroyItem": True,
                    },
                    "failResponse": (
                        "The <em><span class='item-highlight'>Watering Can</span></em> is empty. You need to fill it before you can "
                        "cool the coals."
                    ),
                    "response": [
                        {
                            "speaker": "narrator",
                            "text": (
                                "You begin to spill the cool water over the hot coals, suddenly the bottom of the "
                                "<em><span class='item-highlight'>Watering Can</span></em> gives way. "
                                "Steam rises as the coals hiss and cool, leaving behind a bed of wet gray ash. "
                                "You drop the damaged watering can on the ground; it's no longer usable. "
                                "The ash looks cool enough to search."
                            ),
                        },
                    ],
                },
            },
        },
    },
    "hints": [
        {
            "requires": {
                "inventory": [
                    "a1_watering_can",
                ],
                "itemStates": {
                    "a1_watering_can": {
                        "liquidType": "water",
                    },
                },
                "sceneryState": {
                    "coals": {
                        "isCooled": False,
                    },
                },
            },
            "response": {
                "speaker": "voice",
                "text": "Maybe I could use the can of water on the coals.",
            },
        },
        {
            "requires": {
                "sceneryState": {
                    "coals": {
                        "isCooled": False,
                    },
                },
            },
            "response": {
                "speaker": "voice",
                "text": "If only I had some nice cool water...",
            },
        },
        {
            "requires": {
                "sceneryState": {
                    "coals": {
                        "isCooled": True,
                    },
                },
                "itemsAt": {
                    "coals": [],
                },
            },
            "response": {
                "speaker": "voice",
                "text": "It might be time to move on.",
            },
        },
        {
            "requires": {
                "sceneryState": {
                    "coals": {
                        "isCooled": True,
                    },
                },
            },
            "response": {
                "speaker": "voice",
                "text": "I should search the ashes...",
            },
        },
    ],
    "exits": {
        "north": False,
        "south": "a1_house_2",
        "east": False,
        "west": "a1_lake_east",
    },
}
