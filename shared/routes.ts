import { z } from 'zod';
import { quoteInputSchema } from './schema';

export { quoteInputSchema, type QuoteInput } from './schema';

export const api = {
  quote: {
    get: {
      method: 'POST' as const, // Using POST because we send a payload
      path: '/api/quote' as const,
      input: quoteInputSchema,
      responses: {
        200: z.custom<any>(), // Returns QuoteSummary
        500: z.object({ message: z.string() }),
      },
    },
  },
};
