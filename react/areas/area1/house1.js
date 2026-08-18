const house1 = {
  id: 'house1',
  name: 'Red House',
  intro: [
    {
      speaker: 'narrator',
      text: 'A small red house stands among the trees, its paint faded and its front door shut tight.',
    },
  ],
  description:
    'A weathered red house sits at the forest edge. Its front door leads inside, while paths run east and west.',
  responses: {},
  exits: {
    north: false,
    south: false,
    east: 'roadAccess',
    west: 'silentGrove',
  },

  rooms: {
    house1_livingRoom: {
      name: 'Red House - Living Room',
      intro: [
        {
          speaker: 'narrator',
          text: "You step into the red house's dusty living room.",
        },
      ],
      description:
        'A dusty living room serves as the center of the red house. A calendar lies on the floor beside an old drawer. The kitchen, bathroom, and two bedrooms open from here, and the front door leads outside.',
      responses: {},
      exits: {
        north: false,
        south: false,
        east: false,
        west: false,
      },
    },

    house1_kitchen: {
      name: 'Red House - Kitchen',
      intro: [],
      description:
        'A cramped kitchen with worn cabinets and a shallow drawer. The living room is nearby.',
      responses: {},
      exits: {
        north: false,
        south: false,
        east: false,
        west: false,
      },
    },

    house1_bedroom1: {
      name: 'Red House - Bedroom 1',
      intro: [],
      description:
        'A neglected bedroom containing a narrow bed, a drawer, and a closet. The living room is nearby.',
      responses: {},
      exits: {
        north: false,
        south: false,
        east: false,
        west: false,
      },
    },

    house1_bedroom2: {
      name: 'Red House - Bedroom 2',
      intro: [],
      description:
        'A second dusty bedroom with an empty drawer and closet. The living room is nearby.',
      responses: {},
      exits: {
        north: false,
        south: false,
        east: false,
        west: false,
      },
    },

    house1_bathroom: {
      name: 'Red House - Bathroom',
      intro: [],
      description:
        'A small bathroom with a cracked mirror and a medicine cabinet. The living room is nearby.',
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

export default house1;
