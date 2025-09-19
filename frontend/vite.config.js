import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    host: true,
    strictPort: false,
    hmr: {
      port: 3000
    },
    middlewareMode: false,
    cors: {
      origin: true,
      credentials: true
    },
    proxy: {},
    fs: {
      strict: false
    }
  },
  preview: {
    host: true,
    port: 3000,
    strictPort: false,
    cors: true
  },
  build: {
    outDir: 'build'
  }
})