import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import tailwind from '@astrojs/tailwind';

// https://astro.build/config
export default defineConfig({
  site: 'https://aicenter.pages.dev', // افزودن دامنه اصلی جهت رفع خطای sitemap
  integrations: [
    tailwind(),
    sitemap(),
  ],
});
