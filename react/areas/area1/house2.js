const house2 = {
  id: 'house2',
  name: 'Blue House',
  intro: [
    {
      speaker: 'narrator',
      text: 'A faded blue house stands between the clearing and the stone ring.',
    },
  ],
  description:
    'The abandoned blue house has a locked front door. Paths lead north and south.',
  responses: {},
  exits: {
    north: 'stoneRing',
    south: 'clearing',
    east: false,
    west: false,
  },

  rooms: {
    house2_livingRoom: {
      name: 'Blue House - Living Room',
      intro: [
        {
          speaker: 'narrator',
          text: "You enter the blue house's quiet living room.",
        },
      ],
      description:
        'A sparse living room connects to the kitchen, bathroom, and bedroom. A drawer sits against one wall, and the front door leads outside.',
      responses: {},
      exits: {
        north: false,
        south: false,
        east: false,
        west: false,
      },
    },

    house2_kitchen: {
      name: 'Blue House - Kitchen',
      intro: [],
      description:
        'A stale kitchen with a row of cabinets and one jammed-looking drawer. The living room is nearby.',
      responses: {},
      exits: {
        north: false,
        south: false,
        east: false,
        west: false,
      },
    },

    house2_bedroom: {
      name: 'Blue House - Bedroom',
      intro: [],
      description:
        "The house's only bedroom contains a drawer and a narrow closet. The living room is nearby.",
      responses: {},
      exits: {
        north: false,
        south: false,
        east: false,
        west: false,
      },
    },

    house2_bathroom: {
      name: 'Blue House - Bathroom',
      intro: [],
      description:
        'A cramped bathroom with a cloudy mirror and medicine cabinet. The living room is nearby.',
      responses: {},
      exits: {
        north: false,
        south: false,
        east: false,
        west: false,
      },
    },
  },
};

export default house2;
