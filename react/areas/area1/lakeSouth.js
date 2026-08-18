const lakeSouth = {
  id: 'lakeSouth',
  name: 'Lake (South)',
  intro: [
    {
      speaker: 'narrator',
      text: "The trees thin along the southern shore of the same secluded <em><span class='area-highlight'>Lake (South)</span></em>. From here, the water opens northward between forested banks, reflecting the sky and the distant mountain ridge. Stones gathered into an old fire circle and a worn patch beneath the trees suggest another small campsite once occupied this end of the lake. The water along the shore is bitterly cold; swimming any distance in it would be unsafe. Paths lead south and east.",
    },
  ],
  description:
    "The southern shore looks north across the <em><span class='area-highlight'>Lake (South)</span></em>, with dense forest wrapping around both banks. Signs of an abandoned campsite remain among the rocks. The water is clear but intensely cold, making swimming too dangerous to attempt. Paths lead south and east.",
  responses: {},
  exits: {
    north: false,
    south: 'fallenNursery',
    east: 'lakeEast',
    west: false,
  },
};

export default lakeSouth;
