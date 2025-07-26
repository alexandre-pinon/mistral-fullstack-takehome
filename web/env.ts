import { defineConfig, Schema } from "@julr/vite-plugin-validate-env";

export default defineConfig({
	validator: "builtin",
	schema: {
		VITE_API_URL: Schema.string({ format: "url" }),
	},
});
