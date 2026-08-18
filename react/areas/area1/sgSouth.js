const sgSouth = {
  id: 'sgSouth',
  name: 'Security Gate (South Side)',
  intro: [
    {
      speaker: 'narrator',
      text: 'A high security gate blocks the road. A small guard station stands beside it, with a fuse box mounted on its west wall and a card reader beside the station door.',
    },
  ],
  description:
    'The sealed Security Gate spans the road. The powerless guard station has an exterior fuse box and a card reader beside its door. The road returns south.',
  responses: {},
  exits: {
    north: false,
    south: 'roadAccess',
    east: 'sgEast',
    west: 'sgWest',
  },
};

export default sgSouth;
