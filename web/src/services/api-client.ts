import type { ChatMessage, Role } from "../entities/ChatMessage";

const { VITE_API_URL } = import.meta.env;

export const chat = async (message: ChatMessage): Promise<ChatMessage> => {
	const response = await fetch(`${VITE_API_URL}/chat`, {
		method: "POST",
		body: JSON.stringify({ message: mapChatMessageToRequest(message) }),
		headers: {
			"Content-Type": "application/json",
		},
	});

	if (!response.ok) {
		throw new Error("Failed to chat");
	}

	const responseData = (await response.json()) as ChatMessageResponse;

	return mapChatMessageToResponse(responseData);
};

type ChatMessageRequest = {
	id: string;
	role: Role;
	content: string;
	created_at: string;
};

type ChatMessageResponse = {
	id: string;
	role: Role;
	content: string;
	created_at: string;
};

const mapChatMessageToRequest = (message: ChatMessage): ChatMessageRequest => {
	return {
		id: message.id,
		role: message.role,
		content: message.content,
		created_at: message.createdAt.toISOString(),
	};
};

const mapChatMessageToResponse = (
	message: ChatMessageResponse,
): ChatMessage => {
	return {
		id: message.id,
		role: message.role,
		content: message.content,
		createdAt: new Date(message.created_at),
	};
};
