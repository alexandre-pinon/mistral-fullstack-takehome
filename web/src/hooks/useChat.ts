import { useCallback, useEffect, useState } from "react";
import type { ChatMessage } from "../entities/ChatMessage";
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

			setIsStreaming(true);
			chatStream(
				userMessage.id,
				(message) => {
					setChatMessages((prev) => {
						const assistantMessage = prev.at(-1);
						if (assistantMessage?.id === message.id) {
							return [...prev.slice(0, -1), message];
						}

						return [...prev, message];
					});
				},
				() => {
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
