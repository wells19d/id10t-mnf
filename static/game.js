const commandForm = document.getElementById('command-form');
const commandInput = document.getElementById('command-input');
const gameOutput = document.getElementById('game-output');
const terminal = document.querySelector('.terminal');

const SAVE_KEY = 'id10t_save';
const GAME_TAB_LOCK = 'id10t_game_tab';
const VALID_RESPONSE_SPEAKERS = new Set([
  'narrator',
  'voice',
  'system',
]);

const commandHistory = [];
let historyIndex = 0;

let waitingForStartChoice = false;
let currentGameState = null;
let commandInProgress = false;
let gameTabActive = false;

function focusCommandInput() {
  if (!gameTabActive || document.visibilityState !== 'visible') {
    return;
  }

  commandInput.focus({ preventScroll: true });
}

function displayMessage(speaker, text) {
  if (speaker === 'system') {
    const systemText = document.createElement('div');
    systemText.classList.add('system-response');
    systemText.innerHTML = text;

    gameOutput.appendChild(systemText);
    return;
  }

  const responseText = document.createElement('div');

  let speakerLabel = 'Narrator:';

  if (speaker === 'voice') {
    speakerLabel = 'Inner Voice:';
  }

  if (speaker === 'user') {
    speakerLabel = 'Player:';
  }

  responseText.innerHTML = `
    <div class="tb-row">
      <div class="tl ${speaker}-title">
        ${speakerLabel}
      </div>

      <div class="tr ${speaker}-response"></div>
    </div>
  `;

  const responseContent = responseText.querySelector('.tr');

  if (speaker === 'user') {
    responseContent.textContent = text;
  } else {
    responseContent.innerHTML = text;
  }

  gameOutput.appendChild(responseText);
}

function displayMessages(messages) {
  if (!messages) {
    return;
  }

  messages.forEach((message) => {
    displayMessage(message.speaker, message.text);
  });
}

function isValidCommandMessage(message) {
  return (
    message &&
    typeof message === 'object' &&
    VALID_RESPONSE_SPEAKERS.has(message.speaker) &&
    typeof message.text === 'string'
  );
}

function isValidMessageList(messages) {
  return (
    Array.isArray(messages) && messages.every(isValidCommandMessage)
  );
}

function isValidGameState(state) {
  return (
    state &&
    typeof state === 'object' &&
    !Array.isArray(state) &&
    Number.isInteger(state.saveVersion) &&
    state.player &&
    typeof state.player === 'object' &&
    !Array.isArray(state.player) &&
    Array.isArray(state.player.inventory) &&
    Array.isArray(state.player.equipped) &&
    state.itemStates &&
    typeof state.itemStates === 'object' &&
    !Array.isArray(state.itemStates) &&
    state.flags &&
    typeof state.flags === 'object' &&
    !Array.isArray(state.flags) &&
    state.locations &&
    typeof state.locations === 'object' &&
    !Array.isArray(state.locations)
  );
}

function isValidCommandResult(data) {
  if (!data || typeof data !== 'object') {
    return false;
  }

  const responseIsValid =
    typeof data.response === 'string' ||
    isValidCommandMessage(data.response) ||
    isValidMessageList(data.response);

  return responseIsValid && isValidGameState(data.state);
}

function isValidStartResult(data) {
  return (
    data &&
    typeof data === 'object' &&
    isValidMessageList(data.messages) &&
    isValidGameState(data.state)
  );
}

function displayCommandResponse(response) {
  if (Array.isArray(response)) {
    displayMessages(response);
    return;
  }

  if (isValidCommandMessage(response)) {
    displayMessage(response.speaker, response.text);
    return;
  }

  displayMessage('narrator', response);
}

function scrollToBottom() {
  gameOutput.scrollTop = gameOutput.scrollHeight;
}

function saveGameState(state) {
  if (!isValidGameState(state)) {
    return false;
  }

  try {
    localStorage.setItem(SAVE_KEY, JSON.stringify(state));

    currentGameState = state;

    return true;
  } catch (error) {
    console.error('Unable to save game state.', error);

    return false;
  }
}

function getSavedGameState() {
  let savedGame;

  try {
    savedGame = localStorage.getItem(SAVE_KEY);
  } catch (error) {
    console.error('Unable to read the saved game.', error);

    return {
      status: 'unavailable',
      state: null,
    };
  }

  if (!savedGame) {
    return {
      status: 'missing',
      state: null,
    };
  }

  try {
    const state = JSON.parse(savedGame);

    if (!isValidGameState(state)) {
      return {
        status: 'invalid',
        state: null,
      };
    }

    return {
      status: 'available',
      state: state,
    };
  } catch (error) {
    console.error('Unable to parse the saved game.', error);

    return {
      status: 'invalid',
      state: null,
    };
  }
}

function discardInvalidSavedGame() {
  currentGameState = null;

  try {
    localStorage.removeItem(SAVE_KEY);
    return true;
  } catch (error) {
    console.error('Unable to remove the invalid saved game.', error);
    return false;
  }
}

async function readJsonResponse(response) {
  try {
    return await response.json();
  } catch (error) {
    console.error('Unable to read the server response.', error);
    return null;
  }
}

async function startNewGame() {
  try {
    const response = await fetch('/new-game', {
      method: 'POST',
    });

    const data = await readJsonResponse(response);

    if (!response.ok || !isValidStartResult(data)) {
      console.error('The new-game request returned invalid data.');

      displayMessage(
        'system',
        'A new game could not be started. No saved progress was changed.',
      );

      waitingForStartChoice = true;
      scrollToBottom();
      return false;
    }

    if (!saveGameState(data.state)) {
      displayMessage(
        'system',
        'The new game could not be saved, so it was not started. Check that browser storage is available and try again.',
      );

      waitingForStartChoice = true;
      scrollToBottom();
      return false;
    }

    waitingForStartChoice = false;

    displayMessages(data.messages);
    scrollToBottom();
    return true;
  } catch (error) {
    console.error('Unable to start a new game.', error);

    displayMessage(
      'system',
      'Unable to reach the game server. No saved progress was changed.',
    );

    waitingForStartChoice = true;
    scrollToBottom();
    return false;
  }
}

async function loadSavedGame() {
  const savedGame = getSavedGameState();

  if (savedGame.status === 'unavailable') {
    displayMessage(
      'system',
      'Browser storage is unavailable, so the saved game cannot be loaded safely.',
    );

    scrollToBottom();
    return false;
  }

  if (savedGame.status === 'invalid') {
    discardInvalidSavedGame();

    displayMessage(
      'system',
      'The previous save is invalid or corrupted. Starting a new game.',
    );

    await startNewGame();
    return false;
  }

  if (savedGame.status === 'missing') {
    return startNewGame();
  }

  try {
    const response = await fetch('/load-game', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        state: savedGame.state,
      }),
    });

    const data = await readJsonResponse(response);

    if (
      !response.ok &&
      response.status === 400 &&
      data &&
      data.errorCode === 'invalid-save'
    ) {
      discardInvalidSavedGame();

      displayMessage(
        'system',
        'The previous save is invalid or incompatible. Starting a new game.',
      );

      await startNewGame();
      return false;
    }

    if (!response.ok) {
      console.error(`Load request failed with status ${response.status}.`);

      displayMessage(
        'system',
        'The saved game could not be loaded because of a temporary server error. Your save has been preserved.',
      );

      scrollToBottom();
      return false;
    }

    if (!isValidStartResult(data)) {
      console.error('The load request returned invalid data.');

      displayMessage(
        'system',
        'The server returned an invalid load response. Your save has been preserved.',
      );

      scrollToBottom();
      return false;
    }

    if (!saveGameState(data.state)) {
      displayMessage(
        'system',
        'The loaded game could not be saved safely. Check that browser storage is available and try again.',
      );

      scrollToBottom();
      return false;
    }

    waitingForStartChoice = false;

    displayMessages(data.messages);
    scrollToBottom();
    return true;
  } catch (error) {
    console.error('Unable to load the saved game.', error);

    displayMessage(
      'system',
      'Unable to reach the game server. Your save has been preserved.',
    );

    scrollToBottom();
    return false;
  }
}

async function initializeGame() {
  try {
    const response = await fetch('/start');
    const data = await readJsonResponse(response);

    if (response.ok && data && Array.isArray(data.startup)) {
      const startup = document.createElement('div');

      startup.classList.add('startup-block');

      startup.innerHTML = `
        <div class="startup-title">${data.startup[0]}</div>
        <div class="startup-subtitle">${data.startup[1]}</div>
        <div class="startup-version">${data.startup[2]}</div>
        <div class="startup-development">${data.startup[3]}</div>
        <div class="startup-help">${data.startup[4]}</div>
      `;

      gameOutput.appendChild(startup);
    }
  } catch (error) {
    console.error('Unable to load the startup message.', error);
  }

  const savedGame = getSavedGameState();

  if (savedGame.status === 'unavailable') {
    waitingForStartChoice = true;

    displayMessage(
      'system',
      'Browser storage is unavailable. The game cannot start safely until storage is available.',
    );

    scrollToBottom();
    commandInput.focus();
    return;
  }

  if (savedGame.status === 'invalid') {
    discardInvalidSavedGame();

    displayMessage(
      'system',
      'The previous save is invalid or corrupted. Starting a new game.',
    );

    await startNewGame();
    commandInput.focus();
    return;
  }

  if (savedGame.status === 'available') {
    waitingForStartChoice = true;

    displayMessage(
      'system',
      'Type <span class="command-highlight">load save</span> to resume, or type <span class="command-highlight">new game</span>.',
    );

    scrollToBottom();

    commandInput.focus();

    return;
  }

  await startNewGame();

  commandInput.focus();
}

async function initializeGameTab() {
  if (!navigator.locks) {
    displayMessage(
      'system',
      'This browser cannot start the game with single-tab protection enabled.',
    );

    scrollToBottom();
    return;
  }

  try {
    await navigator.locks.request(
      GAME_TAB_LOCK,
      {
        mode: 'exclusive',
        ifAvailable: true,
      },
      async (lock) => {
        if (!lock) {
          displayMessage(
            'system',
            'The game is already running in another tab. Close that tab and refresh this page to continue.',
          );

          scrollToBottom();
          return;
        }

        gameTabActive = true;

        setInterval(checkServerVersion, 1000);

        await initializeGame();

        await new Promise(() => {});
      },
    );
  } catch (error) {
    gameTabActive = false;

    console.error('Unable to establish the game tab lock.', error);

    displayMessage(
      'system',
      'Unable to start the game safely. Please refresh and try again.',
    );

    scrollToBottom();
  }
}

window.addEventListener('resize', () => {
  requestAnimationFrame(scrollToBottom);
});

window.addEventListener('load', initializeGameTab);

window.addEventListener('focus', () => {
  requestAnimationFrame(focusCommandInput);
});

document.addEventListener('visibilitychange', () => {
  if (document.visibilityState === 'visible') {
    requestAnimationFrame(focusCommandInput);
  }
});

terminal.addEventListener('click', (event) => {
  if (event.target.closest('input, button, a, select, textarea')) {
    return;
  }

  const selection = window.getSelection();

  if (selection && !selection.isCollapsed) {
    return;
  }

  focusCommandInput();
});

commandInput.addEventListener('keydown', (event) => {
  if (event.key === 'ArrowUp') {
    event.preventDefault();

    if (historyIndex > 0) {
      historyIndex -= 1;

      commandInput.value = commandHistory[historyIndex];
    }
  }

  if (event.key === 'ArrowDown') {
    event.preventDefault();

    if (historyIndex < commandHistory.length - 1) {
      historyIndex += 1;

      commandInput.value = commandHistory[historyIndex];
    } else {
      historyIndex = commandHistory.length;

      commandInput.value = '';
    }
  }
});

commandForm.addEventListener('submit', async (event) => {
  event.preventDefault();

  if (!gameTabActive) {
    return;
  }

  const command = commandInput.value.trim();

  if (!command) {
    return;
  }

  if (commandInProgress) {
    return;
  }

  commandInProgress = true;

  try {
    commandHistory.push(command);

    if (commandHistory.length > 10) {
      commandHistory.shift();
    }

    historyIndex = commandHistory.length;

    commandInput.value = '';

    const normalizedCommand = command.toLowerCase();

    if (normalizedCommand === 'quit') {
      waitingForStartChoice = true;

      displayMessage('system', 'Game Ended');

      displayMessage(
        'system',
        'Type <span class="command-highlight">load save</span> to resume, or type <span class="command-highlight">new game</span>.',
      );

      scrollToBottom();

      return;
    }

    if (waitingForStartChoice) {
      if (normalizedCommand === 'load' || normalizedCommand === 'load save') {
        await loadSavedGame();
        return;
      }

      if (normalizedCommand === 'new' || normalizedCommand === 'new game') {
        await startNewGame();
        return;
      }

      displayMessage('user', command);

      displayMessage(
        'system',
        'Type <span class="command-highlight">load save</span> to resume, or type <span class="command-highlight">new game</span>.',
      );

      scrollToBottom();

      return;
    }

    displayMessage('user', command);

    scrollToBottom();

    try {
      const response = await fetch('/command', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          command: command,
          state: currentGameState,
        }),
      });

      const data = await readJsonResponse(response);

      if (!response.ok) {
        console.error(
          `Command request failed with status ${response.status}.`,
        );

        if (
          response.status === 400 &&
          data &&
          data.errorCode === 'invalid-save'
        ) {
          discardInvalidSavedGame();

          waitingForStartChoice = true;

          displayMessage(
            'system',
            'The saved game is invalid or incompatible. Starting a new game.',
          );

          await startNewGame();
          return;
        }

        displayMessage(
          'system',
          'The command could not be processed because of a temporary server error. Your saved progress has been preserved.',
        );

        scrollToBottom();

        return;
      }

      if (!isValidCommandResult(data)) {
        console.error('Command request returned invalid data.');

        displayMessage(
          'system',
          'The command returned an invalid response. Please try again.',
        );

        scrollToBottom();

        return;
      }

      if (!saveGameState(data.state)) {
        displayMessage(
          'system',
          'The command result could not be saved, so the command was not applied. Check that browser storage is available and try again.',
        );

        scrollToBottom();
        return;
      }

      displayCommandResponse(data.response);

      scrollToBottom();
    } catch (error) {
      console.error('Command request failed.', error);

      displayMessage(
        'system',
        'Unable to reach the game server. Please try again.',
      );

      scrollToBottom();
    }
  } finally {
    commandInProgress = false;

    focusCommandInput();
  }
});

let currentServerVersion = null;

async function checkServerVersion() {
  try {
    const response = await fetch('/dev-version');

    const data = await response.json();

    if (currentServerVersion === null) {
      currentServerVersion = data.version;

      return;
    }

    if (data.version !== currentServerVersion) {
      window.location.reload();
    }
  } catch (error) {
    // Flask may be restarting.
  }
}
