import itemsInit from '../init/item.init';

const itemsReducer = (state = itemsInit, action) => {
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
