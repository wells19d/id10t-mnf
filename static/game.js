const commandForm = document.getElementById('command-form');
const commandInput = document.getElementById('command-input');
const gameOutput = document.getElementById('game-output');

function displayMessage(speaker, text) {
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

  data.messages.forEach((message) => {
    displayMessage(message.speaker, message.text);
  });

  scrollToBottom();
});

commandForm.addEventListener('submit', async (event) => {
  event.preventDefault();

  const command = commandInput.value.trim();

  if (!command) {
    return;
  }

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
