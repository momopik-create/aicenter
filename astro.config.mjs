import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://aicenter.pages.dev', // بعداً با دامنه اصلی جایگزین می‌شود
  integrations: [sitemap()],
});
