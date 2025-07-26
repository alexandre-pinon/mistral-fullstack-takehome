import { useCallback, useEffect, useState } from "react";
import { Alert } from "./components/Alert";
import { Chat } from "./components/Chat";
import { ChatInput } from "./components/ChatInput";
import { type ChatMessage, createChatMessage } from "./entities/ChatMessage";
import { loadChat, chat as sendMessageToAssistant } from "./services/api-client";

const App = () => {
  const [chatMessages, setChatMessages] = useState<ChatMessage[]>([]);
  const [error, setError] = useState<string | null>(null);

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
    const userMessage = createChatMessage("user", message);
    setChatMessages((prev) => [...prev, userMessage]);

    try {
      const assistantMessage = await sendMessageToAssistant(userMessage);
      setChatMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      handleError(error);
    }
  };

  return (
    <div className="flex flex-col items-center h-screen pb-6 relative">
      <div className="overflow-y-auto h-full w-full flex flex-col items-center">
        <h1 className="text-3xl font-semibold py-6">Chat</h1>
        <Chat messages={chatMessages} />
      </div>
      <div className="w-full max-w-2xl">
        <ChatInput onSend={handleSend} />
      </div>
      <Alert className="absolute top-5" errorMessage={error} />
    </div>
  );
};

export default App;
