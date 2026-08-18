const initialState = {
  health: 'medium',
  status: 'normal',
  location: 'clearing',
  inventory: [],

  equipment: {
    head: null,
    chest: 'st_light_blue_dress_shirt',
    hands: null,
    legs: 'st_loose_fit_blue_jeans',
    feet: 'st_grey_casual_shoes',
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

    case 'RESET_PLAYER_STATE':
      return initialState;

    case 'RESET_ALL_STATE':
      return initialState;

    default:
      return state;
  }
};

export default playerReducer;
