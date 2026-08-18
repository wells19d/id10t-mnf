export function routeCommand(command, commandHandlers) {
  const normalizedCommand = command.trim().toLowerCase();
  const {
    waitingForStartChoice,
    startNewGame,
    loadGame,
    endGame,
    showHelp,
  } = commandHandlers;

  if (waitingForStartChoice) {
    if (normalizedCommand === 'new' || normalizedCommand === 'new game') {
      startNewGame();
      return true;
    }

    if (normalizedCommand === 'load' || normalizedCommand === 'load save') {
      loadGame();
      return true;
    }

    // Only NEW and LOAD commands are accepted while the game is inactive.
    return true;
  }

  if (normalizedCommand === 'help' || normalizedCommand === 'h') {
    showHelp();
    return true;
  }

  if (
    normalizedCommand === 'new' ||
    normalizedCommand === 'new game' ||
    normalizedCommand === 'load' ||
    normalizedCommand === 'load save'
  ) {
    return true;
  }

  if (normalizedCommand === 'quit') {
    endGame();
    return true;
  }

  return false;
}
