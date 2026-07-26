const commandForm = document.getElementById('command-form');
const commandInput = document.getElementById('command-input');
const gameOutput = document.getElementById('game-output');

commandForm.addEventListener('submit', async (event) => {
  event.preventDefault();

  const command = commandInput.value.trim();

  if (!command) {
    return;
  }

  const commandText = document.createElement('div');

  commandText.innerHTML = `
  <div class="tb-row">
    <div class="tl user-command">User:</div>
    <div class="tr user-command">${command}</div>
  </div>
`;

  gameOutput.appendChild(commandText);
  gameOutput.scrollTop = gameOutput.scrollHeight;

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

  const responseText = document.createElement('div');

  responseText.innerHTML = `
  <div class="tb-row">
    <div class="tl">Narrator:</div>
    <div class="tr narrator-response">${data.response}</div>
  </div>
`;

  gameOutput.appendChild(responseText);

  commandInput.value = '';
});
