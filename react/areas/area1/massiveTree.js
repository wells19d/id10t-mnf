const massiveTree = {
  id: 'massiveTree',
  name: 'Massive Tree',
  intro: [
    {
      speaker: 'narrator',
      text: "You stand in a clearing beside a <em><span class='area-highlight'>Massive Tree</span></em>, its thick trunk and branches spreading high overhead. The bark is rough, deeply grooved, and weathered gray with age. There's no direction to go except back the way you came.",
    },
  ],
  description:
    "You stand in a clearing beside a <em><span class='area-highlight'>Massive Tree</span></em> There's no direction to go except back the way you came.",
  responses: {},
  exits: {
    north: false,
    south: 'clearing',
    east: false,
    west: false,
  },
};

export default massiveTree;
