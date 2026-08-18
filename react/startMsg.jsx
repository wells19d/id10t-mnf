function StartupMessage() {
  return (
    <div className="startup-block">
      <div className="startup-title">Project ID10T: A MEMORY NOT FOUND</div>

      <div className="startup-subtitle">A Text-Based Adventure</div>

      <div className="startup-version">Version 0.1</div>

      <div className="startup-development">
        Developed by AJ Wells at Wellscrypted
      </div>

      <div className="startup-help">
        Type <span className="command-highlight">"help"</span> or{' '}
        <span className="command-highlight">"h"</span> for available commands.
      </div>
    </div>
  );
}

export default StartupMessage;
