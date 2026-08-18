const sgWest = {
  id: 'sgWest',
  name: 'Security Gate (West Side)',
  intro: [],
  description:
    'An exterior fuse box on the west wall contains a burned-out fuse socket.',
  responses: {},
  exits: {
    north: false,
    south: 'sgSouth',
    east: false,
    west: false,
  },
};

export default sgWest;
