import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  base: '/',
  server: {
    port: 3000,
    host: true
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
    extensions: ['.mjs', '.js', '.ts', '.jsx', '.tsx', '.json']
  },
  assetsInclude: ['**/*.png', '**/*.svg', '**/*.jpg', '**/*.jpeg', '**/*.gif', '**/*.webp'],
  build: {
    outDir: 'dist',
    sourcemap: true,
    assetsDir: 'assets',
    rollupOptions: {
      input: {
        main: path.resolve(__dirname, 'index.html'),
      },
      output: {
        manualChunks: {
          'react-vendor': ['react', 'react-dom'],
          'router': ['react-router-dom'],
          'chakra': ['@chakra-ui/react', '@emotion/react', '@emotion/styled', 'framer-motion'],
          'icons': ['react-icons/fa', '@chakra-ui/icons'],
        },
        assetFileNames: (assetInfo) => {
          if (/\.(png|jpe?g|gif|svg|webp)$/.test(assetInfo.name)) {
            return 'assets/images/[name]-[hash][extname]';
          }
          if (/\.css$/.test(assetInfo.name)) {
            return 'assets/css/[name]-[hash][extname]';
          }
          return 'assets/[name]-[hash][extname]';
        },
        chunkFileNames: 'assets/js/[name]-[hash].js',
        entryFileNames: 'assets/js/[name]-[hash].js',
      },
    },
    chunkSizeWarningLimit: 1000,
  },
  optimizeDeps: {
    include: ['react', 'react-dom', 'react-router-dom'],
    exclude: ['@types/react', '@types/react-dom']
  },
  esbuild: {
    jsxFactory: 'React.createElement',
    jsxFragment: 'React.Fragment',
  },
  // Add TypeScript specific configuration
  typescript: {
    tsconfigPath: './tsconfig.json',
    include: ['src/**/*.ts', 'src/**/*.tsx'],
    exclude: ['src/**/*.test.ts', 'src/**/*.test.tsx', 'src/__tests__/**/*']
  }
}) 