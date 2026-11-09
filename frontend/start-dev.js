import { createServer } from "vite";

async function start() {
  const server = await createServer({
    configFile: "./vite.config.js",
    server: {
      host: "0.0.0.0",
      port: 5173,
      strictPort: true,
    },
  });
  await server.listen();
  server.printUrls();
  // Keep the dev server alive indefinitely even if stdin is closed
  setInterval(() => {}, 3600000);
}

start().catch((err) => {
  console.error("Failed to start Vite server:", err);
  process.exit(1);
});

