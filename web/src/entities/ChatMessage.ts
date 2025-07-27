export type Role = "user" | "assistant";

export type ChatMessage = {
	id: string;
	role: Role;
	content: string;
	createdAt: Date;
};
