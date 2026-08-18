const speakerLabels = {
  narrator: 'Narrator:',
  voice: 'Inner Voice:',
};

export default function MsgDisplay({ speaker, text }) {
  if (speaker === 'system') {
    return (
      <div
        className="system-response"
        dangerouslySetInnerHTML={{ __html: text }}
      />
    );
  }

  return (
    <div className="tb-row">
      <div className={`tl ${speaker}-title`}>{speakerLabels[speaker]}</div>

      <div
        className={`tr ${speaker}-response`}
        dangerouslySetInnerHTML={{ __html: text }}
      />
    </div>
  );
}
