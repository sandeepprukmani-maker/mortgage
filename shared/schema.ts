import { pgTable, text, serial, integer, boolean, timestamp, jsonb } from "drizzle-orm/pg-core";
import { createInsertSchema } from "drizzle-zod";
import { z } from "zod";

// We don't necessarily need a database for this specific proxy task as it's stateless,
// but we'll keep the structure standard.
// We can store query history if needed later.

export const quoteRequests = pgTable("quote_requests", {
  id: serial("id").primaryKey(),
  payload: jsonb("payload").notNull(),
  createdAt: timestamp("created_at").defaultNow(),
});

export const insertQuoteRequestSchema = createInsertSchema(quoteRequests).omit({ id: true, createdAt: true });

// === API CONTRACT TYPES ===

// Input for the Quote API (matches Python script payload)
// We use z.any() for some deep nested fields to stay flexible, but type key fields for the form.
export const quoteInputSchema = z.object({
  loanAmount: z.number().default(800000),
  creditScore: z.number().default(780),
  borrowerName: z.string().default("Luca"),
  propertyZipCode: z.string().default("27606"),
  propertyCounty: z.string().default("WAKE"),
  propertyState: z.string().default("NC"),
  salesPrice: z.number().default(0),
  appraisedValue: z.number().default(1157600),
  // Allow other fields to be passed dynamically
}).catchall(z.any());

export type QuoteInput = z.infer<typeof quoteInputSchema>;

// Response structure
export interface QuoteMatch {
  mortgageProductId: number;
  mortgageProductName: string;
  mortgageProductAlias?: string;
  match?: {
    interestRate: number;
    finalPrice: number;
    finalPriceAfterOriginationFee: number;
    originationFee: number;
    principalAndInterest: number;
    monthlyPayment: number;
  };
  diff?: number;
  amount?: number;
  note?: string;
}

export interface QuoteSummary {
  loanAmount: number;
  borrowerName: string;
  validQuoteItemsCount: number;
  errorMessages?: any[];
  matches: QuoteMatch[];
  rawJson: any;
}
