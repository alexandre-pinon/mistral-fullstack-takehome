import Markdown from "marked-react";
import { memo } from "react";
import assistantAvatar from "../assets/assistant_avatar.png";
import type { ChatMessage } from "../entities/ChatMessage";

type ChatMessageBubbleProps = Omit<ChatMessage, "id">;

const ChatMessageBubble = ({ role, content, createdAt }: ChatMessageBubbleProps) => {
  return (
    <div className={`chat gap-y-1 ${role === "user" ? "chat-end" : "chat-start"}`}>
      {role === "assistant" && (
        <div className="chat-image avatar">
          <div className="w-10 rounded-full">
            <img alt="Assistant avatar" src={assistantAvatar} />
          </div>
        </div>
      )}
      <div
        className={`chat-bubble before:hidden peer ${
          role === "user" ? "bg-primary/20" : "bg-secondary/20"
        }`}
      >
        <Markdown value={content} breaks />
      </div>
      <div className="chat-footer opacity-0 peer-hover:opacity-100 transition-opacity duration-200 mt-1">
        {createdAt.toLocaleTimeString([], {
          hour: "numeric",
          minute: "2-digit",
        })}
      </div>
    </div>
  );
};

export const ChatMessageBubbleMemo = memo(ChatMessageBubble);
