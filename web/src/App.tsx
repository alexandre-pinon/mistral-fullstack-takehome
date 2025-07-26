import { useState } from "react";
import { v4 as uuidv4 } from "uuid";
import { Alert } from "./components/Alert";
import { Chat } from "./components/Chat";
import { ChatInput } from "./components/ChatInput";
import { type ChatMessage, createChatMessage } from "./entities/ChatMessage";
import { chat as sendMessageToAssistant } from "./services/api-client";

const chatHistory: ChatMessage[] = [
  {
    id: uuidv4(),
    role: "user",
    content: "Coucou la tortue !",
    createdAt: new Date(),
  },
  {
    id: uuidv4(),
    role: "assistant",
    content: "COUCOU !",
    createdAt: new Date(),
  },
];

const App = () => {
  const [chatMessages, setChatMessages] = useState<ChatMessage[]>(chatHistory);
  const [error, setError] = useState<string | null>(null);

  const handleSend = async (message: string) => {
    const userMessage = createChatMessage("user", message);
    setChatMessages((prev) => [...prev, userMessage]);

    try {
      const assistantMessage = await sendMessageToAssistant(userMessage);
      console.log(assistantMessage);
      setChatMessages((prev) => [...prev, assistantMessage]);
    } catch (error: unknown) {
      handleError(error instanceof Error ? error : new Error("Something went wrong"));
    }
  };

  const handleError = (error: Error) => {
    setError(error.message);
    setTimeout(() => {
      setError(null);
    }, 5000);
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
