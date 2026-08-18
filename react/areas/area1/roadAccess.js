const roadAccess = {
  id: 'roadAccess',
  name: 'Road Access',
  intro: [
    {
      speaker: 'narrator',
      text: 'The forest opens onto a cracked access road choked by weeds and fallen branches. A security gate stands farther north.',
    },
  ],
  description:
    'A narrow, deteriorating road cuts through the forest toward the Security Gate to the north. The red house lies to the west.',
  responses: {},
  exits: {
    north: 'sgSouth',
    south: false,
    east: false,
    west: 'house1',
  },
};

export default roadAccess;
