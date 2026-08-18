const fallenNursery = {
  id: 'fallenNursery',
  name: 'Fallen Nursery',
  intro: [
    {
      speaker: 'narrator',
      text: "A massive fallen tree dominates the edge of the <em><span class='area-highlight'>Fallen Nursery</span></em>, its trunk covered in moss, ferns, and other new growth. Much of it has begun to sink into the forest floor, while broken limbs and exposed wood disappear beneath the vegetation. The remains of the tree stretch deep into the surrounding forest, making passage around the western side impossible. Worn paths lead north, south, and east.",
    },
  ],
  description:
    "A massive fallen tree stretches along the edge of the <em><span class='area-highlight'>Fallen Nursery</span></em>, blocking passage to the west. Worn paths lead north, south, and east.",
  responses: {},
  exits: {
    north: 'lakeSouth',
    south: 'house3',
    east: 'clearing',
    west: false,
  },
};

export default fallenNursery;
