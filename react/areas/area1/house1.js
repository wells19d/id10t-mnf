const house1 = {
  id: 'house1',
  name: 'Red House',
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
