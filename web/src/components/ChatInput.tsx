import { useState } from "react";

type ChatInputProps = {
  onSend: (message: string) => void;
};

export const ChatInput = ({ onSend }: ChatInputProps) => {
  const [message, setMessage] = useState<string>("");

  return (
    <div className="card bg-base-100 w-full shadow-[0_0_15px_rgba(0,0,0,0.05)]">
      <div className="card-body">
        <textarea
          className="textarea field-sizing-content resize-none border-none focus:outline-none shadow-none focus:shadow-none w-full max-h-40 text-base"
          placeholder="Chat..."
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter" && !e.shiftKey) {
              e.preventDefault();
              onSend(message);
              setMessage("");
            }
          }}
        ></textarea>
        <div className="card-actions justify-end">
          <button
            type="button"
            className="btn btn-outline btn-primary"
            onClick={() => onSend(message)}
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
};
