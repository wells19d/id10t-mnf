const house3 = {
  id: 'house3',
  name: 'Green House',
  intro: [
    {
      speaker: 'narrator',
      text: 'A weathered green house leans beneath the surrounding trees.',
    },
  ],
  description:
    "The green house's front door is locked. Paths lead north and east.",
  responses: {},
  exits: {
    north: 'fallenNursery',
    south: false,
    east: 'silentGrove',
    west: false,
  },

  rooms: {
    house3_livingRoom: {
      name: 'Green House - Living Room',
      intro: [
        {
          speaker: 'narrator',
          text: "You enter the green house's dim living room.",
        },
      ],
      description:
        'A dim living room connects to a kitchen, bathroom, and two bedrooms. A drawer rests beneath a boarded window, and the front door leads outside.',
      responses: {},
      exits: {
        north: false,
        south: false,
        east: false,
        west: false,
      },
    },

    house3_kitchen: {
      name: 'Green House - Kitchen',
      intro: [],
      description:
        'A stripped kitchen with empty cabinets and a single drawer. The living room is nearby.',
      responses: {},
      exits: {
        north: false,
        south: false,
        east: false,
        west: false,
      },
    },

    house3_bedroom1: {
      name: 'Green House - Bedroom 1',
      intro: [],
      description:
        'A calendar lies open on the floor of the first bedroom beside an empty drawer and closet. The living room is nearby.',
      responses: {},
      exits: {
        north: false,
        south: false,
        east: false,
        west: false,
      },
    },

    house3_bedroom2: {
      name: 'Green House - Bedroom 2',
      intro: [],
      description:
        'A pair of security pants has been left on the bed. A combination safe sits on the floor of the closet beside a note from Charles.',
      responses: {},
      exits: {
        north: false,
        south: false,
        east: false,
        west: false,
      },
    },

    house3_bathroom: {
      name: 'Green House - Bathroom',
      intro: [],
      description:
        'A damp bathroom with a rust-spotted medicine cabinet. The living room is nearby.',
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

export default house3;
