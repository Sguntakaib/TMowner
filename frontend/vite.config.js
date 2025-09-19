import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    host: true,
    strictPort: false,
    allowedHosts: [
      'localhost',
      '127.0.0.1',
      '10.219.0.148',
      'threat-pulse-5.preview.emergentagent.com',
      '.preview.emergentagent.com',
      '.emergent.host',
      '.emergentagent.com'
    ],
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