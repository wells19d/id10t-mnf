import MsgDisplay from '../MsgDisplay';

export default function QuitMessage({ visible }) {
  if (!visible) {
    return null;
  }

  return <MsgDisplay speaker="system" text="Game Ended" />;
}
