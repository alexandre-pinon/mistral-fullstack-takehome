import type { ChatMessage } from "../entities/ChatMessage";

const { VITE_API_URL, VITE_API_KEY } = import.meta.env;

export const chat = async (message: string): Promise<ChatMessage> => {
	const response = await fetch(`${VITE_API_URL}/chat`, {
		method: "POST",
		body: JSON.stringify({ message }),
		headers: {
			"Content-Type": "application/json",
			"x-api-key": VITE_API_KEY,
		},
	});

	if (!response.ok) {
		throw new Error("Failed to chat");
	}

	return response.json() as Promise<ChatMessage>;
};
