import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      // Forward API calls to the backend during local dev
      '/api': 'http://localhost:3001',
    },
  },
});
