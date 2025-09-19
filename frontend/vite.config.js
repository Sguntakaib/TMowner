import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    host: '0.0.0.0',
    allowedHosts: 'all',
    strictPort: false,
    hmr: {
      host: 'localhost',
      clientPort: 3000
    },
    cors: true,
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': '*',
      'Access-Control-Allow-Headers': '*'
    }
  },
  build: {
    outDir: 'build'
  },
  define: {
    'process.env': {}
  }
})