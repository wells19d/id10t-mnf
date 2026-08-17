import { useEffect, useRef, useState } from 'react';

function CommandInput({ onCommand }) {
  const inputRef = useRef(null);
  const [command, setCommand] = useState('');

  useEffect(() => {
    const focusInput = () => {
      inputRef.current?.focus();
    };

    const handleVisibilityChange = () => {
      if (!document.hidden) {
        focusInput();
      }
    };

    focusInput();

    window.addEventListener('focus', focusInput);
    document.addEventListener('visibilitychange', handleVisibilityChange);

    return () => {
      window.removeEventListener('focus', focusInput);
      document.removeEventListener('visibilitychange', handleVisibilityChange);
    };
  }, []);

  const handleBlur = () => {
    setTimeout(() => {
      inputRef.current?.focus();
    }, 0);
  };

  const handleSubmit = (event) => {
    event.preventDefault();

    const trimmedCommand = command.trim();

    if (!trimmedCommand) {
      return;
    }

    onCommand(trimmedCommand);
    setCommand('');
  };

  return (
    <form className="terminal-form" onSubmit={handleSubmit}>
      <span className="terminal-prompt">Ready:</span>

      <input
        ref={inputRef}
        type="text"
        autoComplete="off"
        className="terminal-input"
        value={command}
        onChange={(event) => setCommand(event.target.value)}
        onBlur={handleBlur}
      />

      <button type="submit" className="terminal-button">
        Enter
      </button>
    </form>
  );
}

export default CommandInput;
