import { useEffect, useRef } from "react";
import type { ChatMessage } from "../entities/ChatMessage";
import { ChatMessageBubble } from "./ChatMessageBubble";

type ChatProps = {
  messages: ChatMessage[];
};

export const Chat = ({ messages }: ChatProps) => {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (messages.length > 0) {
      messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages.length]);

  return (
    <div className="w-full max-w-3xl">
      {messages.map((message) => (
        <ChatMessageBubble key={message.id} {...message} />
      ))}
      <div ref={messagesEndRef} />
    </div>
  );
};
