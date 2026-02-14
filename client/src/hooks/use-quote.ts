import { useMutation } from "@tanstack/react-query";
import { api, type QuoteInput } from "@shared/routes";

export type QuoteResponse = {
  loanAmount: number;
  borrowerName: string;
  validQuoteItemsCount: number;
  matches: Array<{
    mortgageProductId: number;
    mortgageProductName: string;
    mortgageProductAlias?: string;
    match?: {
      interestRate: number;
      finalPrice: number;
      principalAndInterest: number;
      monthlyPayment: number;
      originationFee: number;
    };
    diff?: number;
    amount?: number;
    note?: string;
  }>;
  rawJson: any;
};

export function useGetQuote() {
  return useMutation({
    mutationFn: async (data: QuoteInput) => {
      const res = await fetch(api.quote.get.path, {
        method: api.quote.get.method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });
      
      if (!res.ok) {
        const error = await res.json();
        throw new Error(error.message || "Failed to fetch quote");
      }
      
      return (await res.json()) as QuoteResponse;
    },
  });
}
