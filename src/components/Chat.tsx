import type { ChatMessage } from "../entities/ChatMessage";
import { ChatMessageBubble } from "./ChatMessageBubble";

type ChatProps = {
  messages: ChatMessage[];
};

export const Chat = ({ messages }: ChatProps) => {
  return (
    <div className="w-full max-w-3xl">
      {messages.map((message) => (
        <ChatMessageBubble key={message.id} {...message} />
      ))}
    </div>
  );
};
