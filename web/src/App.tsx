import { Alert } from "./components/Alert";
import { Chat } from "./components/Chat";
import { ChatInput } from "./components/ChatInput";
import { useChat } from "./hooks/useChat";

const App = () => {
  const { chatMessages, error, isStreaming, sendMessage } = useChat();

  return (
    <div className="flex flex-col items-center h-screen pb-6 relative">
      <div className="overflow-y-auto h-full w-full flex flex-col items-center">
        <h1 className="text-3xl font-semibold py-6">Chat</h1>
        <Chat messages={chatMessages} />
      </div>
      <div className="w-full max-w-2xl">
        <ChatInput onSend={sendMessage} disabled={isStreaming} />
      </div>
      <Alert className="absolute top-5" errorMessage={error} />
    </div>
  );
};

export default App;
