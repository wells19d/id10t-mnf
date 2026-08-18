import { use } from 'react';
import CommandInput from './CommandInput';
import { usePlayerState, useWorldState, useItemState } from './hooks/useHooks';
import StartupMessage from '../startMsg';

function App() {
  const handleCommand = (command) => {
    console.log(command);
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
        <div id="game-output" className="terminal-top">
          <StartupMessage />
        </div>

        <div className="terminal-bottom">
          <CommandInput onCommand={handleCommand} />
        </div>
      </div>
    </main>
  );
}

export default App;
