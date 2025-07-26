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

export const chat = async (message: ChatMessage): Promise<ChatMessage> => {
	const response = await fetch(`${VITE_API_URL}/chat`, {
		method: "POST",
		body: JSON.stringify(mapChatMessageToApi(message)),
		headers: {
			"Content-Type": "application/json",
		},
	});

	if (!response.ok) {
		throw new Error("Failed to chat");
	}

	const responseData = (await response.json()) as ApiChatMessage;

	return mapApiChatMessageToChatMessage(responseData);
};

type ApiChatMessage = {
	id: string;
	role: Role;
	content: string;
	created_at: string;
};

const mapChatMessageToApi = (message: ChatMessage): ApiChatMessage => {
	return {
		id: message.id,
		role: message.role,
		content: message.content,
		created_at: message.createdAt.toISOString(),
	};
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
