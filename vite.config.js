import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import ViteYaml from '@modyfi/vite-plugin-yaml'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react(), ViteYaml()],
  resolve: {
    alias: {
      '@': '/src',
    },
  },
  // If deploying to a custom domain (mirasquran.com), use '/'
  // If deploying to github.io/repo-name, use '/repo-name/'
  base: '/miras-quran/',
})
