import { useState } from 'react';
import { useDispatch } from 'react-redux';

export const STARTUP_MESSAGE = [
  'Project ID10T: A MEMORY NOT FOUND',
  'A Text-Based Adventure',
  'Version 0.1',
  'Developed by AJ Wells at Wellscrypted',
  'Type "help" or "h" for available commands.',
];

const startupClasses = [
  'startup-title',
  'startup-subtitle',
  'startup-version',
  'startup-development',
  'startup-help',
];

export const START_PROMPT_MESSAGE = [
  {
    speaker: 'system',
    text: 'Type <span class="command-highlight">load save</span> to resume, or type <span class="command-highlight">new game</span>.',
  },
];

export const QUIT_MESSAGE = [
  {
    speaker: 'system',
    text: 'Game Ended',
  },
  ...START_PROMPT_MESSAGE,
];

export function StartupMessage({ messages }) {
  return (
    <div className="startup-block">
      {messages.map((message, index) => (
        <div key={message} className={startupClasses[index]}>
          {message}
        </div>
      ))}
    </div>
  );
}

export function useStartup() {
  const dispatch = useDispatch();
  const [waitingForStartChoice, setWaitingForStartChoice] = useState(true);

  const startNewGame = () => {
    dispatch({
      type: 'NEW_GAME_REQUEST',
    });

    setWaitingForStartChoice(false);
  };

  const loadGame = () => {
    dispatch({
      type: 'LOAD_GAME_REQUEST',
    });

    setWaitingForStartChoice(false);
  };

  const endGame = () => {
    dispatch({
      type: 'QUIT_GAME_REQUEST',
    });

    setWaitingForStartChoice(true);
  };

  return {
    waitingForStartChoice,
    startNewGame,
    loadGame,
    endGame,
  };
}
