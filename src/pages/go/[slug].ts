import type { GetStaticPaths, APIRoute } from 'astro';
import fs from 'node:fs';
import path from 'node:path';

// تابع خواندن affiliates.json
function getAffiliateData(): Record<string, string> {
  const filePath = path.resolve(process.cwd(), 'affiliates.json');
  if (fs.existsSync(filePath)) {
    try {
      const content = fs.readFileSync(filePath, 'utf-8');
      return JSON.parse(content);
    } catch {
      return {};
    }
  }
  return {};
}

// ایجاد تمام مسیرهای پویا برای زمان بیلد
export const getStaticPaths: GetStaticPaths = () => {
  const affiliateLinks = getAffiliateData();
  const paths = Object.keys(affiliateLinks).map((slug) => ({
    params: { slug },
  }));

  return paths;
};

// هندل کردن ریدایرکت 302 به لینک افیلیت
export const GET: APIRoute = ({ params, redirect }) => {
  const { slug } = params;
  const affiliateLinks = getAffiliateData();

  if (slug && affiliateLinks[slug]) {
    return redirect(affiliateLinks[slug], 302);
  }

  const defaultLink = affiliateLinks['default'] || 'https://google.com';
  return redirect(defaultLink, 302);
};
