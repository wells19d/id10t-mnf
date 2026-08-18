const silentGrove = {
  id: 'silentGrove',
  name: 'Silent Grove',
  intro: [
    {
      speaker: 'narrator',
      text: "You enter a <em><span class='area-highlight'>Silent Grove</span></em>, the air still and filled with the scent of damp earth and moss. The trees here are tall and ancient, their branches forming a dense canopy overhead. Sunlight filters through the leaves, casting dappled shadows across the forest floor. It's peaceful here, but the silence is almost eerie. A worn path leads north, while other paths continue east and west.",
    },
  ],
  description:
    "You are standing in a quiet and secluded <em><span class='area-highlight'>Silent Grove</span></em>. Worn paths lead north, east, and west.",
  responses: {},
  exits: {
    north: 'clearing',
    south: false,
    east: 'house1',
    west: 'house3',
  },
};

export default silentGrove;
