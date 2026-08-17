import { use } from 'react';
import CommandInput from './CommandInput';
import { usePlayerState, useWorldState, useItemState } from './hooks/useHooks';

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

  return (
    <main>
      <h1>Project ID10T: A Memory Not Found</h1>

      <div className="terminal">
        <div id="game-output" className="terminal-top"></div>

        <div className="terminal-bottom">
          <CommandInput onCommand={handleCommand} />
        </div>
      </div>
    </main>
  );
}

export default App;
