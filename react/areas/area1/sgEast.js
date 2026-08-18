const sgEast = {
  id: 'sgEast',
  name: 'Security Gate (East Side)',
  intro: [],
  description: 'A security card reader controls access to the guard station.',
  responses: {},
  exits: {
    north: 'outerCompound',
    south: 'sgSouth',
    east: false,
    west: false,
  },
};

export default sgEast;
