const outerCompound = {
  id: 'outerCompound',
  name: 'Beyond the Security Gate',
  intro: [
    {
      speaker: 'narrator',
      text: 'As you cross the threshold, a memory flashes through your mind: bright lights, hurried voices, and a door sealing shut.',
    },
    {
      speaker: 'narrator',
      text: 'Behind you, the Guard Station electrical system shorts with a violent crack. The gate slams closed and its mechanism grinds into a permanent jam, cutting off the way back to Area 1.',
    },
  ],
  description:
    'The jammed Security Gate blocks the route back into the forest. The unknown path ahead marks the beginning of Area 2.',
  responses: {},
  exits: {
    north: false,
    south: false,
    east: false,
    west: false,
  },
};

export default outerCompound;
