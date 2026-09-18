import { defineCollection, z } from 'astro:content';

const productsCollection = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    rating: z.number(),
    date: z.string(),
    pricing_tier: z.string().optional(),
  }),
});

export const collections = {
  'products': productsCollection,
};
