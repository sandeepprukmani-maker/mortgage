import axios, { type AxiosInstance } from "axios";
import { SocksProxyAgent } from "socks-proxy-agent";
import { type QuoteInput, type QuoteSummary, type QuoteMatch } from "@shared/schema";

// Environment variables should be set in Replit Secrets
// UWM_USERNAME, UWM_PASSWORD, UWM_CLIENT_ID, UWM_CLIENT_SECRET, UWM_SCOPE

export class UwmClient {
  private session: AxiosInstance;
  private tokenUrl = "https://sso.uwm.com/adfs/oauth2/token";
  private priceQuoteUrl = "https://stg.api.uwm.com/public/instantpricequote/v2/pricequote";
  private proxyUrl = "socks5://127.0.0.1:1080";

  constructor() {
    const httpsAgent = new SocksProxyAgent(this.proxyUrl);
    
    this.session = axios.create({
      httpsAgent,
      httpAgent: httpsAgent,
      headers: {
        "User-Agent": "uwm-ipq-python/1.0", // Mimic the python script
        "Accept": "application/json",
      },
      timeout: 60000 // 60s
    });
  }

  private async getAccessToken(): Promise<string> {
    const { UWM_USERNAME, UWM_PASSWORD, UWM_CLIENT_ID, UWM_CLIENT_SECRET, UWM_SCOPE } = process.env;

    if (!UWM_USERNAME || !UWM_PASSWORD || !UWM_CLIENT_ID || !UWM_CLIENT_SECRET) {
      throw new Error("Missing UWM environment variables (UWM_USERNAME, UWM_PASSWORD, etc.)");
    }

    const params = new URLSearchParams();
    params.append("grant_type", "password");
    params.append("username", UWM_USERNAME);
    params.append("password", UWM_PASSWORD);
    params.append("client_id", UWM_CLIENT_ID);
    params.append("client_secret", UWM_CLIENT_SECRET);
    if (UWM_SCOPE) params.append("scope", UWM_SCOPE);

    try {
      const response = await this.session.post(this.tokenUrl, params, {
        headers: { "Content-Type": "application/x-www-form-urlencoded" }
      });

      if (response.data && response.data.access_token) {
        return response.data.access_token;
      } else {
        throw new Error("No access_token in response: " + JSON.stringify(response.data));
      }
    } catch (error: any) {
       console.error("Token Error:", error.response?.data || error.message);
       throw new Error(`Failed to get access token: ${error.message}`);
    }
  }

  async getQuote(input: QuoteInput): Promise<QuoteSummary> {
    const token = await this.getAccessToken();

    // Construct full payload filling in defaults for missing fields if necessary
    // The input already has some defaults from Zod, but we need the full structure the API expects
    const payload = {
        brokerAlias: "TEST",
        loanOfficer: "lofficer@email.com",
        purposeTypeID: "3",
        loanTypeIds: ["0"],
        refinancePurposeId: "Rate And Term Reduction-CONV",
        occupancyTypeId: "1",
        propertyTypeId: "22",
        commitmentPeriodId: "13",
        isCorrespondent: false,
        isDTIOver45Percent: false,
        monthlyDebt: 0,
        annualTaxes: 0,
        annualHomeownersInsurance: 0,
        annualPercentageRateFees: 0,
        selfEmployed: false,
        monthsOfBankStatementsId: "0",
        monthsOfReservesId: "0",
        numberOfBorrowers: 1,
        compensationPayerTypeID: "1",
        escrowWaiverTypeId: "1",
        includeFlexTerms: false,
        tracTypeId: "0",
        waivableFeeTypeIds: ["0"],
        loanShieldTypeId: "0",
        paPlusTypeId: "0",
        exactRateTypeId: "2",
        targetPriceValue: 0,
        targetCashValue: 0,
        waiveUnderwritingFee: false,
        monthlyIncome: 20000,
        buyDownAliasID: "2-1 LLPA",
        firstTimeHomeBuyer: false,
        loanTermIds: ["4", "3", "1", "2", "0"],
        // Overrides from input
        ...input
    };

    try {
      const response = await this.session.post(this.priceQuoteUrl, payload, {
        headers: {
          "Authorization": `Bearer ${token}`,
          "Content-Type": "application/json"
        }
      });

      const body = this.normalizeJson(response.data);
      return this.processResponse(body);

    } catch (error: any) {
      console.error("Quote API Error:", error.response?.data || error.message);
      throw new Error(`Failed to get price quote: ${error.message}`);
    }
  }

  private normalizeJson(obj: any): any {
    if (Array.isArray(obj)) {
      return obj.map(v => this.normalizeJson(v));
    } else if (typeof obj === 'object' && obj !== null) {
      const newObj: any = {};
      for (const key in obj) {
        newObj[key] = this.normalizeJson(obj[key]);
      }
      return newObj;
    } else if (typeof obj === 'string') {
      return obj.replace(/\u00a0/g, " ").replace(/\s+/g, " ").trim();
    }
    return obj;
  }

  private safeFloat(x: any): number | null {
      if (x === null || x === undefined) return null;
      const parsed = parseFloat(x);
      return isNaN(parsed) ? null : parsed;
  }

  private processResponse(body: any): QuoteSummary {
    const targetAmount = -2000.0;
    const matches: QuoteMatch[] = [];

    const validQuoteItems = body.validQuoteItems || [];

    for (const item of validQuoteItems) {
        let bestPp = null;
        let bestDiff = null;

        const quotePricePoints = item.quotePricePoints || [];
        for (const pp of quotePricePoints) {
            const fpa = pp.finalPriceAfterOriginationFee || {};
            const amt = this.safeFloat(fpa.amount);
            if (amt === null) continue;

            const diff = Math.abs(amt - targetAmount);
            if (bestPp === null || (bestDiff !== null && diff < bestDiff)) {
                bestPp = pp;
                bestDiff = diff;
            }
        }

        if (bestPp) {
             matches.push({
                 mortgageProductId: item.mortgageProductId,
                 mortgageProductName: item.mortgageProductName,
                 mortgageProductAlias: item.mortgageProductAlias,
                 match: {
                     interestRate: bestPp.interestRate?.value,
                     finalPrice: bestPp.finalPrice?.percent,
                     finalPriceAfterOriginationFee: bestPp.finalPriceAfterOriginationFee?.percent,
                     originationFee: bestPp.originationFee?.percent,
                     principalAndInterest: bestPp.principalAndInterest?.value,
                     monthlyPayment: bestPp.monthlyPayment?.value,
                 },
                 diff: bestDiff || 0,
                 amount: this.safeFloat(bestPp.finalPriceAfterOriginationFee?.amount) || 0
             });
        } else {
            matches.push({
                 mortgageProductId: item.mortgageProductId,
                 mortgageProductName: item.mortgageProductName,
                 note: "No matching price points found"
            });
        }
    }

    return {
        loanAmount: body.loanAmount,
        borrowerName: body.borrowerName,
        validQuoteItemsCount: validQuoteItems.length,
        errorMessages: body.errorMessages,
        matches,
        rawJson: body
    };
  }
}
