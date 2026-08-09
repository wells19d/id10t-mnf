const commandForm = document.getElementById('command-form');
const commandInput = document.getElementById('command-input');
const gameOutput = document.getElementById('game-output');

const SAVE_KEY = 'id10t_save';
const GAME_TAB_LOCK = 'id10t_game_tab';

const commandHistory = [];
let historyIndex = 0;

let waitingForStartChoice = false;
let currentGameState = null;
let commandInProgress = false;
let gameTabActive = false;

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
    typeof message.speaker === 'string' &&
    typeof message.text === 'string'
  );
}

function isValidCommandResult(data) {
  if (!data || typeof data !== 'object') {
    return false;
  }

  const responseIsValid =
    typeof data.response === 'string' ||
    (Array.isArray(data.response) &&
      data.response.every(isValidCommandMessage));

  const state = data.state;
  const stateIsValid =
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
    state.areas &&
    typeof state.areas === 'object' &&
    !Array.isArray(state.areas);

  return responseIsValid && stateIsValid;
}

function scrollToBottom() {
  gameOutput.scrollTop = gameOutput.scrollHeight;
}

function saveGameState(state) {
  if (!state) {
    return;
  }

  currentGameState = state;

  try {
    localStorage.setItem(SAVE_KEY, JSON.stringify(state));
  } catch (error) {
    console.error('Unable to save game state.', error);
  }
}

function getSavedGameState() {
  const savedGame = localStorage.getItem(SAVE_KEY);

  if (!savedGame) {
    return null;
  }

  try {
    const state = JSON.parse(savedGame);

    if (
      !state ||
      typeof state !== 'object' ||
      !state.player ||
      typeof state.player !== 'object'
    ) {
      localStorage.removeItem(SAVE_KEY);

      return null;
    }

    return state;
  } catch (error) {
    localStorage.removeItem(SAVE_KEY);

    return null;
  }
}

async function startNewGame() {
  waitingForStartChoice = false;

  localStorage.removeItem(SAVE_KEY);

  const response = await fetch('/new-game', {
    method: 'POST',
  });

  const data = await response.json();

  displayMessages(data.messages);

  saveGameState(data.state);

  scrollToBottom();
}

async function loadSavedGame() {
  const savedState = getSavedGameState();

  if (!savedState) {
    await startNewGame();
    return;
  }

  const response = await fetch('/load-game', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      state: savedState,
    }),
  });

  const data = await response.json();

  if (!response.ok) {
    localStorage.removeItem(SAVE_KEY);

    displayMessage(
      'system',
      'The previous save could not be loaded. Starting a new game.',
    );

    await startNewGame();
    return;
  }

  waitingForStartChoice = false;

  displayMessages(data.messages);

  saveGameState(data.state);

  scrollToBottom();
}

async function initializeGame() {
  const response = await fetch('/start');

  const data = await response.json();

  if (data.startup) {
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

  const savedState = getSavedGameState();

  if (savedState) {
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

      if (!response.ok) {
        console.error(
          `Command request failed with status ${response.status}.`,
        );

        displayMessage(
          'system',
          'The command could not be processed. Please try again.',
        );

        scrollToBottom();

        return;
      }

      const data = await response.json();

      if (!isValidCommandResult(data)) {
        console.error('Command request returned invalid data.');

        displayMessage(
          'system',
          'The command returned an invalid response. Please try again.',
        );

        scrollToBottom();

        return;
      }

      if (Array.isArray(data.response)) {
        data.response.forEach((message) => {
          displayMessage(message.speaker, message.text);
        });
      } else {
        displayMessage('narrator', data.response);
      }

      saveGameState(data.state);

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
