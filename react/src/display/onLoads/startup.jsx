import { useState } from 'react';
import { useDispatch } from 'react-redux';
import MsgDisplay from '../MsgDisplay';

const START_PROMPT =
  'Type <span class="command-highlight">load save</span> to resume, or type <span class="command-highlight">new game</span>.';

export function useStartup() {
  const dispatch = useDispatch();
  const [waitingForStartChoice, setWaitingForStartChoice] = useState(true);
  const [gameEnded, setGameEnded] = useState(false);

  const startNewGame = () => {
    dispatch({
      type: 'NEW_GAME_REQUEST',
    });

    setWaitingForStartChoice(false);
    setGameEnded(false);
  };

  const loadGame = () => {
    dispatch({
      type: 'LOAD_GAME_REQUEST',
    });

    setWaitingForStartChoice(false);
    setGameEnded(false);
  };

  const endGame = () => {
    dispatch({
      type: 'QUIT_GAME_REQUEST',
    });

    setGameEnded(true);
    setWaitingForStartChoice(true);
  };

  return {
    waitingForStartChoice,
    gameEnded,
    startNewGame,
    loadGame,
    endGame,
  };
}

export function StartPrompt({ visible }) {
  if (!visible) {
    return null;
  }

  return <MsgDisplay speaker="system" text={START_PROMPT} />;
}
