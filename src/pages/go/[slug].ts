import type { APIRoute } from 'astro';
import affiliateLinks from '../../../affiliates.json';

export const GET: APIRoute = ({ params, redirect }) => {
  const slug = params.slug || 'default';
  
  // پیدا کردن لینک افیلیت متناسب با اسلاگ یا استفاده از لینک پیش‌فرض
  const key = Object.keys(affiliateLinks).find(k => slug.includes(k)) || 'default';
  const targetUrl = (affiliateLinks as Record<string, string>)[key] || affiliateLinks.default;

  // هدایت کاربر با کد 302 (موقت) برای حفظ سئو
  return redirect(targetUrl, 302);
};
