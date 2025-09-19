import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    host: '0.0.0.0',
    allowedHosts: [
      'localhost',
      '127.0.0.1',
      '0.0.0.0',
      '.emergentagent.com',
      'threat-analysis-1.preview.emergentagent.com',
      '.preview.emergentagent.com'
    ],
    strictPort: false,
    hmr: {
      host: 'localhost'
    }
  },
  build: {
    outDir: 'build'
  },
  define: {
    'process.env': {}
  }
})