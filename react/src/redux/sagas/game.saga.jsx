import { call, put, select, takeLatest } from 'redux-saga/effects';

const SAVE_KEY = 'id10t_react_save';

function* newGame() {
  yield call([localStorage, localStorage.removeItem], SAVE_KEY);
  yield put({ type: 'RESET_ALL_STATE' });
}

function* loadGame() {
  try {
    const savedGame = yield call([localStorage, localStorage.getItem], SAVE_KEY);

    if (!savedGame) {
      yield put({ type: 'RESET_ALL_STATE' });
      return;
    }

    const savedState = JSON.parse(savedGame);

    if (
      !savedState?.playerState ||
      !savedState?.worldState ||
      !savedState?.itemState
    ) {
      yield put({ type: 'RESET_ALL_STATE' });
      return;
    }

    yield put({ type: 'SET_PLAYER', payload: savedState.playerState });
    yield put({ type: 'SET_WORLD', payload: savedState.worldState });
    yield put({ type: 'SET_ITEMS', payload: savedState.itemState });
  } catch (error) {
    console.error('Unable to load saved game:', error);
    yield put({ type: 'RESET_ALL_STATE' });
  }
}

function* quitGame() {
  try {
    const gameState = yield select((state) => ({
      playerState: state.playerState,
      worldState: state.worldState,
      itemState: state.itemState,
    }));

    yield call(
      [localStorage, localStorage.setItem],
      SAVE_KEY,
      JSON.stringify(gameState),
    );

    yield put({ type: 'RESET_ALL_STATE' });
  } catch (error) {
    console.error('Unable to save game before quitting:', error);
  }
}

export default function* gameSaga() {
  yield takeLatest('NEW_GAME_REQUEST', newGame);
  yield takeLatest('LOAD_GAME_REQUEST', loadGame);
  yield takeLatest('QUIT_GAME_REQUEST', quitGame);
}
