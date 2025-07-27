import type { ChatMessage, Role } from "../entities/ChatMessage";

const { VITE_API_URL } = import.meta.env;

export const loadChat = async (): Promise<ChatMessage[]> => {
	const response = await fetch(`${VITE_API_URL}/chat`);

	if (!response.ok) {
		throw new Error("Failed to load chat history");
	}

	const responseData = (await response.json()) as ApiChatMessage[];

	return responseData.map(mapApiChatMessageToChatMessage);
};

export const sendUserMessage = async (
	content: string,
): Promise<ChatMessage> => {
	const response = await fetch(`${VITE_API_URL}/chat/messages`, {
		method: "POST",
		body: JSON.stringify({ content }),
		headers: {
			"Content-Type": "application/json",
		},
	});

	if (!response.ok) {
		throw new Error("Failed to send message");
	}

	const responseData = (await response.json()) as ApiChatMessage;

	return mapApiChatMessageToChatMessage(responseData);
};

export const chatStream = (
	messageId: string,
	onChunk: (content: string) => void,
	onComplete: (message: ChatMessage) => void,
	onError: (error: Error) => void,
) => {
	const eventSource = new EventSource(
		`${VITE_API_URL}/chat/messages/${messageId}/stream`,
	);

	eventSource.onmessage = (event) => {
		try {
			const data = JSON.parse(event.data) as StreamChunkResponse;

			if (!data.done) {
				onChunk(data.content);
			} else if (data.assistant_message) {
				onComplete(mapApiChatMessageToChatMessage(data.assistant_message));
				eventSource.close();
			} else if (data.error) {
				onError(new Error(data.error));
				eventSource.close();
			}
		} catch (error) {
			console.error(error);
			onError(new Error("Failed to parse streaming response"));
			eventSource.close();
		}
	};

	eventSource.onerror = () => {
		onError(new Error("Streaming connection failed"));
		eventSource.close();
	};

	return eventSource;
};

type ApiChatMessage = {
	id: string;
	role: Role;
	content: string;
	created_at: string;
};

export type StreamChunkResponse =
	| {
			done: false;
			content: string;
	  }
	| {
			done: true;
			assistant_message?: ApiChatMessage;
			error?: string;
	  };

const mapApiChatMessageToChatMessage = (
	message: ApiChatMessage,
): ChatMessage => {
	return {
		id: message.id,
		role: message.role,
		content: message.content,
		createdAt: new Date(message.created_at),
	};
};
