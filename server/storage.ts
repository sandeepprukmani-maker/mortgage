import { db } from "./db";
import { quoteRequests, type QuoteInput } from "@shared/schema";

export interface IStorage {
  logQuoteRequest(request: QuoteInput): Promise<void>;
}

export class DatabaseStorage implements IStorage {
  async logQuoteRequest(request: QuoteInput): Promise<void> {
    try {
      await db.insert(quoteRequests).values({
        payload: request,
      });
    } catch (error) {
      console.error("Failed to log quote request:", error);
      // Don't fail the request just because logging failed
    }
  }
}

export const storage = new DatabaseStorage();
