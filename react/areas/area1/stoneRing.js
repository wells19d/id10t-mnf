const stoneRing = {
  id: 'stoneRing',
  name: 'Stone Ring',
  intro: [
    {
      speaker: 'narrator',
      text: "A narrow path opens into a small forest clearing centered around a low, moss-covered <em><span class='area-highlight'>Stone Ring</span></em>. The fire inside has burned down recently, leaving a bed of hot coals that still radiates heat into the damp air. Among the blackened wood are warped scraps of something deliberately burned, as though someone tried to destroy a handful of personal belongings. Paths lead south and west.",
    },
    {
      speaker: 'voice',
      text: 'There might still be something worth saving in there... if only I had something that could hold enough water to cool it down.',
    },
  ],
  description:
    "A bed of hot coals smolders inside the moss-covered <em><span class='area-highlight'>Stone Ring</span></em>. Blackened scraps among the coals suggest someone tried to burn several personal belongings. Paths lead south and west.",
  description: ({ worldState }) => {
    const coalsCooled = worldState.area1.stoneRing.coalsCooled;

    if (coalsCooled) {
      return "Cold gray ash fills the moss-covered <em><span class='area-highlight'>Stone Ring</span></em>. The remains of several burned personal belongings lie exposed within it. Paths lead south and west.";
    }

    return "A bed of hot coals smolders inside the moss-covered <em><span class='area-highlight'>Stone Ring</span></em>. Blackened scraps among the coals suggest someone tried to burn several personal belongings. Paths lead south and west.";
  },

  responses: {
    handleCoals: ({ worldState, itemState }) => {
      const coalsCooled = worldState.area1.stoneRing.coalsCooled;
      const wateringCan = itemState.a1_watering_can;

      if (coalsCooled) {
        return [
          {
            speaker: 'system',
            text: 'The coals are already cold.',
          },
        ];
      }

      if (wateringCan.liquidType !== 'water') {
        return [
          {
            speaker: 'narrator',
            text: 'The Watering Can is empty.',
          },
        ];
      }

      return [
        {
          speaker: 'narrator',
          text: 'You pour the water over the coals. Steam rises as they cool.',
        },
      ];
    },
  },
  exits: {
    north: false,
    south: 'house2',
    east: false,
    west: 'lakeEast',
  },
};

export default stoneRing;
