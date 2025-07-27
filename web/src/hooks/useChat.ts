import { useCallback, useEffect, useState } from "react";
import { type ChatMessage, createChatMessage } from "../entities/ChatMessage";
import { chatStream, loadChat, sendUserMessage } from "../services/api-client";

export const useChat = () => {
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

	const sendMessage = async (message: string) => {
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
						const lastMessageIndex = newMessages.length - 1;
						const lastMessage = newMessages[lastMessageIndex];

						if (lastMessage?.role === "assistant") {
							newMessages[lastMessageIndex] = {
								...lastMessage,
								content: lastMessage.content + content,
							};
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
				},
			);
		} catch (error) {
			handleError(error);
			setIsStreaming(false);
		}
	};

	return {
		chatMessages,
		error,
		isStreaming,
		sendMessage,
	};
};
