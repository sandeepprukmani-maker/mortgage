import { LineChart } from "lucide-react";

export function Header() {
  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background/80 backdrop-blur-md">
      <div className="container mx-auto px-4 h-16 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="p-2 bg-primary/10 rounded-lg">
            <LineChart className="w-6 h-6 text-primary" />
          </div>
          <span className="font-display font-bold text-xl tracking-tight">
            UWM <span className="text-primary">Quoter</span>
          </span>
        </div>
        <div className="text-sm font-medium text-muted-foreground">
          Mortgage Pricing Engine
        </div>
      </div>
    </header>
  );
}
