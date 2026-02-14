import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { motion } from "framer-motion";
import { 
  Building2, 
  Calculator, 
  CheckCircle2, 
  ChevronRight, 
  DollarSign, 
  FileText, 
  Percent, 
  User 
} from "lucide-react";

import { useGetQuote, type QuoteResponse } from "@/hooks/use-quote";
import { quoteInputSchema, type QuoteInput } from "@shared/routes";
import { Header } from "@/components/layout/Header";

import { Button } from "@/components/ui/button";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";
import { Separator } from "@/components/ui/separator";
import { Badge } from "@/components/ui/badge";
import { useToast } from "@/hooks/use-toast";

// Extend the schema for form validation with proper types
const formSchema = quoteInputSchema;

export default function Home() {
  const { toast } = useToast();
  const { mutate: getQuote, isPending, data: quoteData, error } = useGetQuote();
  
  const form = useForm<QuoteInput>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      loanAmount: 800000,
      creditScore: 780,
      borrowerName: "Luca",
      propertyZipCode: "27606",
      propertyCounty: "WAKE",
      propertyState: "NC",
      salesPrice: 0,
      appraisedValue: 1157600,
    },
  });

  function onSubmit(data: QuoteInput) {
    getQuote(data, {
      onError: (err) => {
        toast({
          title: "Error fetching quote",
          description: err.message,
          variant: "destructive",
        });
      },
    });
  }

  const formatCurrency = (val?: number) => {
    if (val === undefined || val === null) return "N/A";
    return new Intl.NumberFormat("en-US", {
      style: "currency",
      currency: "USD",
    }).format(val);
  };

  const formatPercent = (val?: number) => {
    if (val === undefined || val === null) return "N/A";
    return `${(val * 100).toFixed(3)}%`;
  };

  return (
    <div className="min-h-screen bg-slate-50/50">
      <Header />
      
      <main className="container mx-auto px-4 py-8 md:py-12">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          
          {/* Left Column: Form */}
          <div className="lg:col-span-4 space-y-6">
            <Card className="border-none shadow-lg shadow-primary/5 sticky top-24">
              <CardHeader className="bg-gradient-to-br from-white to-slate-50 pb-6 rounded-t-xl border-b">
                <CardTitle className="flex items-center gap-2 text-xl">
                  <Calculator className="w-5 h-5 text-primary" />
                  Request Quote
                </CardTitle>
                <CardDescription>
                  Enter borrower details to get real-time pricing.
                </CardDescription>
              </CardHeader>
              <CardContent className="pt-6">
                <Form {...form}>
                  <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
                    <FormField
                      control={form.control}
                      name="borrowerName"
                      render={({ field }) => (
                        <FormItem>
                          <FormLabel>Borrower Name</FormLabel>
                          <FormControl>
                            <div className="relative">
                              <User className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                              <Input className="pl-9" placeholder="John Doe" {...field} />
                            </div>
                          </FormControl>
                          <FormMessage />
                        </FormItem>
                      )}
                    />

                    <div className="grid grid-cols-2 gap-4">
                      <FormField
                        control={form.control}
                        name="loanAmount"
                        render={({ field }) => (
                          <FormItem>
                            <FormLabel>Loan Amount</FormLabel>
                            <FormControl>
                              <div className="relative">
                                <DollarSign className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                                <Input 
                                  className="pl-9" 
                                  type="number" 
                                  {...field} 
                                  onChange={e => field.onChange(Number(e.target.value))}
                                />
                              </div>
                            </FormControl>
                            <FormMessage />
                          </FormItem>
                        )}
                      />
                      <FormField
                        control={form.control}
                        name="creditScore"
                        render={({ field }) => (
                          <FormItem>
                            <FormLabel>Credit Score</FormLabel>
                            <FormControl>
                              <Input 
                                type="number" 
                                {...field} 
                                onChange={e => field.onChange(Number(e.target.value))}
                              />
                            </FormControl>
                            <FormMessage />
                          </FormItem>
                        )}
                      />
                    </div>

                    <FormField
                      control={form.control}
                      name="appraisedValue"
                      render={({ field }) => (
                        <FormItem>
                          <FormLabel>Appraised Value</FormLabel>
                          <FormControl>
                            <div className="relative">
                              <DollarSign className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                              <Input 
                                className="pl-9" 
                                type="number" 
                                {...field} 
                                onChange={e => field.onChange(Number(e.target.value))}
                              />
                            </div>
                          </FormControl>
                          <FormMessage />
                        </FormItem>
                      )}
                    />

                    <div className="grid grid-cols-2 gap-4">
                      <FormField
                        control={form.control}
                        name="propertyZipCode"
                        render={({ field }) => (
                          <FormItem>
                            <FormLabel>Zip Code</FormLabel>
                            <FormControl>
                              <Input {...field} />
                            </FormControl>
                            <FormMessage />
                          </FormItem>
                        )}
                      />
                      <FormField
                        control={form.control}
                        name="propertyState"
                        render={({ field }) => (
                          <FormItem>
                            <FormLabel>State</FormLabel>
                            <FormControl>
                              <Input {...field} maxLength={2} className="uppercase" />
                            </FormControl>
                            <FormMessage />
                          </FormItem>
                        )}
                      />
                    </div>

                    <FormField
                      control={form.control}
                      name="propertyCounty"
                      render={({ field }) => (
                        <FormItem>
                          <FormLabel>County</FormLabel>
                          <FormControl>
                            <Input {...field} className="uppercase" />
                          </FormControl>
                          <FormMessage />
                        </FormItem>
                      )}
                    />

                    <Button 
                      type="submit" 
                      className="w-full h-12 text-base font-semibold mt-4 shadow-lg shadow-primary/20"
                      disabled={isPending}
                    >
                      {isPending ? (
                        <div className="flex items-center gap-2">
                          <div className="h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent" />
                          Running Quote...
                        </div>
                      ) : (
                        <div className="flex items-center gap-2">
                          Get Live Quote
                          <ChevronRight className="w-4 h-4" />
                        </div>
                      )}
                    </Button>
                  </form>
                </Form>
              </CardContent>
            </Card>
          </div>

          {/* Right Column: Results */}
          <div className="lg:col-span-8 space-y-6">
            {!quoteData && !isPending && !error && (
              <div className="h-full min-h-[400px] flex flex-col items-center justify-center text-center p-8 border-2 border-dashed border-slate-200 rounded-xl bg-slate-50">
                <div className="w-16 h-16 bg-white rounded-full flex items-center justify-center shadow-sm mb-4">
                  <Building2 className="w-8 h-8 text-slate-300" />
                </div>
                <h3 className="text-lg font-semibold text-slate-900">No Quote Generated</h3>
                <p className="text-slate-500 max-w-sm mt-2">
                  Fill out the form on the left to see live mortgage product matches and pricing.
                </p>
              </div>
            )}

            {isPending && (
              <div className="h-full min-h-[400px] flex flex-col items-center justify-center space-y-4">
                <div className="w-16 h-16 border-4 border-primary/20 border-t-primary rounded-full animate-spin" />
                <p className="text-slate-500 animate-pulse">Fetching pricing data...</p>
              </div>
            )}

            {error && (
              <Card className="border-red-100 bg-red-50">
                <CardContent className="pt-6 text-center text-red-600">
                  <p className="font-semibold">Error occurred</p>
                  <p className="text-sm mt-1">{error.message}</p>
                </CardContent>
              </Card>
            )}

            {quoteData && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
                className="space-y-8"
              >
                {/* Summary Cards */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <Card className="bg-white/50 backdrop-blur border-primary/10">
                    <CardHeader className="pb-2">
                      <CardDescription>Borrower</CardDescription>
                      <CardTitle className="text-2xl">{quoteData.borrowerName}</CardTitle>
                    </CardHeader>
                  </Card>
                  <Card className="bg-white/50 backdrop-blur border-primary/10">
                    <CardHeader className="pb-2">
                      <CardDescription>Loan Amount</CardDescription>
                      <CardTitle className="text-2xl text-primary">
                        {formatCurrency(quoteData.loanAmount)}
                      </CardTitle>
                    </CardHeader>
                  </Card>
                  <Card className="bg-white/50 backdrop-blur border-primary/10">
                    <CardHeader className="pb-2">
                      <CardDescription>Valid Matches</CardDescription>
                      <CardTitle className="text-2xl flex items-center gap-2">
                        {quoteData.validQuoteItemsCount}
                        <CheckCircle2 className="w-5 h-5 text-green-500" />
                      </CardTitle>
                    </CardHeader>
                  </Card>
                </div>

                {/* Best Matches */}
                <div>
                  <h3 className="text-xl font-bold mb-4 flex items-center gap-2">
                    <FileText className="w-5 h-5 text-primary" />
                    Best Matches
                  </h3>
                  <div className="space-y-4">
                    {quoteData.matches.length === 0 ? (
                      <div className="p-8 text-center bg-white rounded-xl border">
                        <p className="text-muted-foreground">No valid products found for these criteria.</p>
                      </div>
                    ) : (
                      quoteData.matches.map((match, idx) => (
                        <motion.div
                          key={match.mortgageProductId}
                          initial={{ opacity: 0, x: -20 }}
                          animate={{ opacity: 1, x: 0 }}
                          transition={{ delay: idx * 0.1 }}
                        >
                          <Card className="overflow-hidden hover:shadow-lg transition-shadow duration-300 border-primary/5 group">
                            <div className="absolute top-0 left-0 w-1 h-full bg-primary/0 group-hover:bg-primary transition-all duration-300" />
                            <CardContent className="p-6">
                              <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
                                <div className="space-y-1">
                                  <div className="flex items-center gap-2">
                                    <h4 className="font-bold text-lg text-slate-900">
                                      {match.mortgageProductName}
                                    </h4>
                                    <Badge variant="secondary" className="font-mono text-xs">
                                      ID: {match.mortgageProductId}
                                    </Badge>
                                  </div>
                                  {match.note && (
                                    <p className="text-sm text-muted-foreground">{match.note}</p>
                                  )}
                                  {match.match && (
                                    <div className="flex flex-wrap gap-4 mt-3">
                                      <div className="flex items-center gap-1.5 text-sm font-medium text-slate-600 bg-slate-100 px-2.5 py-1 rounded-md">
                                        <Percent className="w-4 h-4 text-primary" />
                                        Rate: {match.match.interestRate}%
                                      </div>
                                      <div className="flex items-center gap-1.5 text-sm font-medium text-slate-600 bg-slate-100 px-2.5 py-1 rounded-md">
                                        <DollarSign className="w-4 h-4 text-green-600" />
                                        Mo. Payment: {formatCurrency(match.match.monthlyPayment)}
                                      </div>
                                    </div>
                                  )}
                                </div>

                                {match.match && (
                                  <div className="flex flex-col items-end gap-1 min-w-[140px]">
                                    <span className="text-sm text-muted-foreground">Final Price</span>
                                    <span className="text-2xl font-bold tracking-tight text-primary">
                                      {match.match.finalPrice !== undefined ? match.match.finalPrice.toFixed(3) : "N/A"}
                                    </span>
                                    {match.diff !== undefined && (
                                      <span className="text-xs font-mono text-muted-foreground bg-slate-100 px-2 py-0.5 rounded">
                                        Diff: {match.diff.toFixed(2)}
                                      </span>
                                    )}
                                  </div>
                                )}
                              </div>
                            </CardContent>
                          </Card>
                        </motion.div>
                      ))
                    )}
                  </div>
                </div>

                {/* Raw JSON Accordion */}
                <Accordion type="single" collapsible className="bg-white rounded-xl border shadow-sm">
                  <AccordionItem value="item-1" className="border-none">
                    <AccordionTrigger className="px-6 hover:no-underline hover:bg-slate-50 rounded-t-xl">
                      <div className="flex items-center gap-2 text-slate-600">
                        <FileText className="w-4 h-4" />
                        <span>View Raw API Response</span>
                      </div>
                    </AccordionTrigger>
                    <AccordionContent>
                      <div className="bg-slate-950 p-6 m-0 border-t overflow-x-auto max-h-[500px] rounded-b-xl">
                        <pre className="text-xs font-mono text-green-400 leading-relaxed">
                          {JSON.stringify(quoteData.rawJson, null, 2)}
                        </pre>
                      </div>
                    </AccordionContent>
                  </AccordionItem>
                </Accordion>
              </motion.div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}
