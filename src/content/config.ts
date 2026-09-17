import { defineCollection, z } from 'astro:content';

const productsCollection = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    rating: z.number(),
    affiliate_url: z.string().url(),
    date: z.string(),
  }),
});

export const collections = {
  'products': productsCollection,
};
