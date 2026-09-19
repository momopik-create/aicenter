import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://momopik.com', // آدرس سایت شما
  integrations: [
    sitemap(),
  ],
});
