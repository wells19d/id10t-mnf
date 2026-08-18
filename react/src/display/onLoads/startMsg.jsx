export const STARTUP_MESSAGE = [
  'Project ID10T: A MEMORY NOT FOUND',
  'A Text-Based Adventure',
  'Version 0.1',
  'Developed by AJ Wells at Wellscrypted',
  'Type "help" or "h" for available commands.',
];

const startupClasses = [
  'startup-title',
  'startup-subtitle',
  'startup-version',
  'startup-development',
  'startup-help',
];

export default function StartupMessage({ messages }) {
  return (
    <div className="startup-block">
      {messages.map((message, index) => (
        <div key={message} className={startupClasses[index]}>
          {message}
        </div>
      ))}
    </div>
  );
}
