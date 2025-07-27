import { useState } from "react";

type ChatInputProps = {
  onSend: (message: string) => void;
  disabled?: boolean;
};

export const ChatInput = ({ onSend, disabled = false }: ChatInputProps) => {
  const [message, setMessage] = useState<string>("");

  const handleSend = () => {
    if (message.trim() && !disabled) {
      onSend(message);
      setMessage("");
    }
  };

  return (
    <div className="card bg-base-100 w-full shadow-[0_0_15px_rgba(0,0,0,0.05)]">
      <div className="card-body">
        <textarea
          className="textarea field-sizing-content resize-none border-none focus:outline-none shadow-none focus:shadow-none w-full max-h-40 text-base"
          placeholder={disabled ? "Streaming..." : "Chat..."}
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter" && !e.shiftKey) {
              e.preventDefault();
              handleSend();
            }
          }}
          disabled={disabled}
        ></textarea>
        <div className="card-actions justify-end">
          <button
            type="button"
            className="btn btn-outline btn-primary"
            onClick={handleSend}
            disabled={disabled || !message.trim()}
          >
            {disabled ? "Streaming..." : "Send"}
          </button>
        </div>
      </div>
    </div>
  );
};
