import worldInit from '../init/world.init';

const worldReducer = (state = worldInit, action) => {
  switch (action.type) {
    case 'SET_WORLD':
      return {
        ...state,
        ...action.payload,
      };

    case 'UPDATE_WORLD_SUCCESS': {
      const { area, location, updatedData } = action.payload;

      return {
        ...state,
        [area]: {
          ...state[area],
          [location]: {
            ...state[area][location],
            ...updatedData,
          },
        },
      };
    }

    case 'RESET_WORLD_STATE':
      return worldInit;

    case 'RESET_ALL_STATE':
      return worldInit;

    default:
      return state;
  }
};

export default worldReducer;
