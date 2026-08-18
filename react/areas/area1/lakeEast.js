const lakeEast = {
  id: 'lakeEast',
  name: 'Lake (East)',
  intro: [
    {
      speaker: 'narrator',
      text: "The path reaches the eastern shore of a secluded <em><span class='area-highlight'>Lake (East)</span></em>, where clear, dark water stretches west beneath the surrounding pines. Beyond the far shore, a broken mountain ridge rises above the forest. A flattened patch of ground and a rough circle of blackened stones suggest this rocky spot once served as a small campsite. The water gives off a deep cold that numbs your fingers at the slightest touch; trying to swim it would be dangerous. Paths lead south and east.",
    },
  ],
  description:
    "From the eastern shore of the <em><span class='area-highlight'>Lake (East)</span></em>, you can see across its cold, dark water toward the forest and distant mountain ridge. The remains of a small campsite sit among the shoreline rocks. The water is far too cold for safe swimming. Paths lead south and east.",
  responses: {},
  exits: {
    north: false,
    south: 'lakeSouth',
    east: 'stoneRing',
    west: false,
  },
};

export default lakeEast;
