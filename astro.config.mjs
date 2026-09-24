import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://aicenter-2vm.pages.dev',
  integrations: [
    sitemap(),
  ],
});