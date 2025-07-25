import { v4 as uuidv4 } from "uuid";

export type ChatMessage = {
	id: string;
	role: string;
	content: string;
	createdAt: Date;
};

export const createChatMessage = (role: string, content: string) => {
	return {
		id: uuidv4(),
		role,
		content,
		createdAt: new Date(),
	};
};
