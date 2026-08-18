import itemsInit from '../init/item.init';

const itemsReducer = (state = itemsInit, action) => {
  switch (action.type) {
    case 'SET_ITEMS':
      return {
        ...state,
        ...action.payload,
      };

    case 'UPDATE_ITEM_SUCCESS': {
      const { itemId, updatedData } = action.payload;

      return {
        ...state,
        [itemId]: {
          ...state[itemId],
          ...updatedData,
        },
      };
    }

    case 'RESET_ITEM_STATE':
      return itemsInit;

    case 'RESET_ALL_STATE':
      return itemsInit;

    default:
      return state;
  }
};

export default itemsReducer;
