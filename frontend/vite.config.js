import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5174,
    proxy: {
      '/copilot': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },
      // add more endpoints if needed
    },
  },
});
