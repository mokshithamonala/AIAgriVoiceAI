import path from "path";
import { fileURLToPath } from "url";
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "lucide-react": path.resolve(__dirname, "./src/icons.jsx"),
    },
  },
  server: {
    host: "0.0.0.0",
    port: 5173,
  },
});
