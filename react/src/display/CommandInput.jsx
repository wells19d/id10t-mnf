import { useEffect, useRef, useState } from 'react';

function CommandInput({ onCommand }) {
  const inputRef = useRef(null);
  const [command, setCommand] = useState('');

  useEffect(() => {
    const focusInput = () => {
      if (!document.hidden) {
        inputRef.current?.focus();
      }
    };

    const handleVisibilityChange = () => {
      if (!document.hidden) {
        focusInput();
      }
    };

    const handlePagePointerDown = () => {
      setTimeout(focusInput, 0);
    };

    focusInput();

    window.addEventListener('focus', focusInput);
    document.addEventListener('visibilitychange', handleVisibilityChange);
    document.addEventListener('pointerdown', handlePagePointerDown);

    return () => {
      window.removeEventListener('focus', focusInput);
      document.removeEventListener('visibilitychange', handleVisibilityChange);
      document.removeEventListener('pointerdown', handlePagePointerDown);
    };
  }, []);

  const handleBlur = () => {
    setTimeout(() => {
      if (!document.hidden) {
        inputRef.current?.focus();
      }
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
