const commandForm = document.getElementById('command-form');
const commandInput = document.getElementById('command-input');
const gameOutput = document.getElementById('game-output');

const commandHistory = [];
let historyIndex = 0;

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

function scrollToBottom() {
  gameOutput.scrollTop = gameOutput.scrollHeight;
}

window.addEventListener('resize', () => {
  requestAnimationFrame(scrollToBottom);
});

window.addEventListener('load', async () => {
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

  data.messages.forEach((message) => {
    displayMessage(message.speaker, message.text);
  });

  scrollToBottom();
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

  const command = commandInput.value.trim();

  if (!command) {
    return;
  }

  commandHistory.push(command);

  if (commandHistory.length > 10) {
    commandHistory.shift();
  }

  historyIndex = commandHistory.length;

  displayMessage('user', command);
  scrollToBottom();

  commandInput.value = '';

  const response = await fetch('/command', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      command: command,
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
    // Flask may be restarting
  }
}

setInterval(checkServerVersion, 1000);
