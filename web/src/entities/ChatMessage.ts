import { v4 as uuidv4 } from "uuid";

export type Role = "user" | "assistant";

export type ChatMessage = {
	id: string;
	role: Role;
	content: string;
	createdAt: Date;
};

export const createChatMessage = (role: Role, content: string) => {
	return {
		id: uuidv4(),
		role,
		content,
		createdAt: new Date(),
	};
};
