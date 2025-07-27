import { useCallback, useEffect, useState } from "react";
import { Alert } from "./components/Alert";
import { Chat } from "./components/Chat";
import { ChatInput } from "./components/ChatInput";
import { type ChatMessage, createChatMessage } from "./entities/ChatMessage";
import { chatStream, loadChat, sendUserMessage } from "./services/api-client";

const App = () => {
  const [chatMessages, setChatMessages] = useState<ChatMessage[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [isStreaming, setIsStreaming] = useState(false);

  const handleError = useCallback((error: unknown) => {
    setError(error instanceof Error ? error.message : "Something went wrong");
    setTimeout(() => {
      setError(null);
    }, 5000);
  }, []);

  useEffect(() => {
    loadChat().then(setChatMessages).catch(handleError);
  }, [handleError]);

  const handleSend = async (message: string) => {
    try {
      const userMessage = await sendUserMessage(message);
      setChatMessages((prev) => [...prev, userMessage]);

      const assistantMessage = createChatMessage("assistant", "");
      setChatMessages((prev) => [...prev, assistantMessage]);
      setIsStreaming(true);

      chatStream(
        userMessage.id,
        (content) => {
          setChatMessages((prev) => {
            const newMessages = [...prev];
            const lastMessage = newMessages[newMessages.length - 1];
            if (lastMessage && lastMessage.role === "assistant") {
              lastMessage.content += content;
            }
            return newMessages;
          });
        },
        (completedMessage) => {
          setChatMessages((prev) => {
            const newMessages = [...prev];
            newMessages[newMessages.length - 1] = completedMessage;
            return newMessages;
          });
          setIsStreaming(false);
        },
        (error) => {
          handleError(error);
          setIsStreaming(false);
          setChatMessages((prev) => prev.slice(0, -1));
        }
      );
    } catch (error) {
      handleError(error);
      setIsStreaming(false);
    }
  };

  return (
    <div className="flex flex-col items-center h-screen pb-6 relative">
      <div className="overflow-y-auto h-full w-full flex flex-col items-center">
        <h1 className="text-3xl font-semibold py-6">Chat</h1>
        <Chat messages={chatMessages} />
      </div>
      <div className="w-full max-w-2xl">
        <ChatInput onSend={handleSend} disabled={isStreaming} />
      </div>
      <Alert className="absolute top-5" errorMessage={error} />
    </div>
  );
};

export default App;
