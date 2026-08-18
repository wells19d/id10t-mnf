import { useEffect, useRef, useState } from 'react';
import CommandInput from './display/CommandInput';
import { usePlayerState, useWorldState, useItemState } from './hooks/useHooks';
import {
  QUIT_MESSAGE,
  START_PROMPT_MESSAGE,
  STARTUP_MESSAGE,
  StartupMessage,
  useStartup,
} from './display/startup';
import MsgDisplay from './display/MsgDisplay';
import { HELP_MESSAGE } from './display/help';
import { routeCommand } from './game/commands';

function App() {
  const terminalOutputRef = useRef(null);
  const [terminalMessages, setTerminalMessages] =
    useState(START_PROMPT_MESSAGE);
  const { waitingForStartChoice, startNewGame, loadGame, endGame } =
    useStartup();

  const appendMessages = (messages) => {
    setTerminalMessages((currentMessages) => [...currentMessages, ...messages]);
  };

  const showHelp = () => {
    appendMessages(HELP_MESSAGE);
  };

  const quitGame = () => {
    endGame();
    appendMessages(QUIT_MESSAGE);
  };

  useEffect(() => {
    const terminalOutput = terminalOutputRef.current;

    if (terminalOutput) {
      terminalOutput.scrollTop = terminalOutput.scrollHeight;
    }
  }, [terminalMessages]);

  const handleCommand = (command) => {
    const commandHandled = routeCommand(command, {
      waitingForStartChoice,
      startNewGame,
      loadGame,
      endGame: quitGame,
      showHelp,
    });

    if (commandHandled) {
      return;
    }

    // Normal gameplay commands will go here later.
    console.log('gameplay command:', command);
  };

  const player = usePlayerState();
  const world = useWorldState();
  const items = useItemState();
  console.log('player', player);
  console.log('world', world);
  console.log('items', items);
  console.log('player', player?.location);

  return (
    <main>
      <h1>Project ID10T: A Memory Not Found</h1>

      <div className="terminal">
        <div ref={terminalOutputRef} id="game-output" className="terminal-top">
          <StartupMessage messages={STARTUP_MESSAGE} />
          {terminalMessages.map((message, index) => (
            <MsgDisplay
              key={index}
              speaker={message.speaker}
              text={message.text}
            />
          ))}
        </div>

        <div className="terminal-bottom">
          <CommandInput onCommand={handleCommand} />
        </div>
      </div>
    </main>
  );
}

export default App;
