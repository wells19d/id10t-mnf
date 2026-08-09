const commandForm = document.getElementById('command-form');
const commandInput = document.getElementById('command-input');
const gameOutput = document.getElementById('game-output');

const SAVE_KEY = 'id10t_save';

const commandHistory = [];
let historyIndex = 0;

let waitingForStartChoice = false;
let currentGameState = null;

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

      <div class="tr ${speaker}-response">
        ${text}
      </div>
    </div>
  `;

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

window.addEventListener('resize', () => {
  requestAnimationFrame(scrollToBottom);
});

window.addEventListener('load', initializeGame);

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

  const command = commandInput.value.trim();

  if (!command) {
    return;
  }

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

  const data = await response.json();

  if (Array.isArray(data.response)) {
    data.response.forEach((message) => {
      displayMessage(message.speaker, message.text);
    });
  } else {
    displayMessage('narrator', data.response);
  }

  saveGameState(data.state);

  scrollToBottom();
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

setInterval(checkServerVersion, 1000);
