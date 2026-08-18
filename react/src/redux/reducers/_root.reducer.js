import { combineReducers } from 'redux';
import playerReducer from './player.reducer';
import worldReducer from './world.reducer';
import itemsReducer from './items.reducer';

const rootReducer = combineReducers({
  playerState: playerReducer,
  worldState: worldReducer,
  itemState: itemsReducer,
});

export default rootReducer;
