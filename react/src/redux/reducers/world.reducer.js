import worldInit from '../init/world.init';

const worldReducer = (state = worldInit, action) => {
  switch (action.type) {
    case 'SET_WORLD':
      return {
        ...state,
        ...action.payload,
      };

    default:
      return state;
  }
};

export default worldReducer;
