const sgSouth = {
  id: 'sgSouth',
  name: 'Security Gate (South Side)',
  responses: {},
  exits: {
    north: false,
    south: 'roadAccess',
    east: 'sgEast',
    west: 'sgWest',
  },
};

export default sgSouth;
