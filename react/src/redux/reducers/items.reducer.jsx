const initialState = {};

const itemsReducer = (state = initialState, action) => {
  switch (action.type) {
    case 'SET_ITEMS':
      return {
        ...state,
        ...action.payload,
      };

    default:
      return state;
  }
};

export default itemsReducer;
