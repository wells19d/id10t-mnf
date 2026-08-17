const initialState = {
  health: 'medium',
  status: 'normal',
  location: null,
  inventory: [],

  equipment: {
    head: null,
    chest: null,
    hands: null,
    legs: null,
    feet: null,
    outerwear: null,
    back: null,
    accessories: null,
  },
};

const playerReducer = (state = initialState, action) => {
  switch (action.type) {
    case 'SET_PLAYER':
      return {
        ...state,
        ...action.payload,
      };

    default:
      return state;
  }
};

export default playerReducer;
