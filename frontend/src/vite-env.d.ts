/// <reference types="vite/client" />

declare module '@fontsource/roboto'

interface ImportMetaEnv {
  readonly VITE_API_URL: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}
