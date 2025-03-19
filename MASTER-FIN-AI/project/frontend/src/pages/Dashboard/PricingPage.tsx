import { useState } from "react";
import { useLocation } from "wouter";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Switch } from "@/components/ui/switch";
import { Check } from "lucide-react";

const PricingPage = () => {
  const [isAnnual, setIsAnnual] = useState(false);
  const [, setLocation] = useLocation();

  const plans = {
    free: {
      name: "Essential",
      price: 0,
      description: "Look first at how all the markets are performing",
      features: [
        "Basic charting",
        "Limited indicators",
        "Real-time data",
        "1 chart layout",
        "Basic alerts"
      ]
    },
    premium: {
      name: "Premium",
      monthly: 49.95,
      annual: 479.40,
      savings: "Save $120/year",
      description: "Full access to all features and capabilities",
      features: [
        "Advanced charting",
        "All indicators",
        "Multiple chart layouts",
        "Advanced alerts",
        "Trading signals",
        "Custom scripts",
        "Volume profile",
        "Priority support"
      ]
    }
  };

  return (
    <div className="min-h-screen bg-background py-20 px-4">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-16">
          <h1 className="text-4xl font-bold mb-4">Plans for every level of ambition</h1>
          <div className="flex items-center justify-center gap-4 mt-8">
            <span className={!isAnnual ? "text-primary" : "text-muted-foreground"}>Monthly</span>
            <Switch 
              checked={isAnnual}
              onCheckedChange={setIsAnnual}
              className="bg-white"
            />
            <span className={isAnnual ? "text-primary" : "text-muted-foreground"}>
              Annually <span className="text-xs text-primary">16% off</span>
            </span>
          </div>
        </div>

        <div className="grid md:grid-cols-2 gap-8 max-w-5xl mx-auto">
          {/* Free Plan */}
          <Card className="relative overflow-hidden border-2 border-muted">
            <CardHeader>
              <CardTitle>{plans.free.name}</CardTitle>
              <CardDescription>{plans.free.description}</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="mb-8">
                <span className="text-4xl font-bold">${plans.free.price}</span>
                <span className="text-muted-foreground">/forever</span>
              </div>
              <ul className="space-y-4">
                {plans.free.features.map((feature, i) => (
                  <li key={i} className="flex items-center gap-2">
                    <Check className="h-5 w-5 text-primary" />
                    <span>{feature}</span>
                  </li>
                ))}
              </ul>
            </CardContent>
            <CardFooter>
              <Button className="w-full" variant="outline">
                Start Free
              </Button>
            </CardFooter>
          </Card>

          {/* Premium Plan */}
          <Card className="relative overflow-hidden border-2 border-primary bg-gradient-to-br from-primary/10 via-background to-background">
            <div className="absolute top-0 right-0 px-3 py-1 bg-primary text-primary-foreground text-sm">
              Most Popular
            </div>
            <CardHeader>
              <CardTitle>{plans.premium.name}</CardTitle>
              <CardDescription>{plans.premium.description}</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="mb-8">
                <span className="text-4xl font-bold">
                  ${isAnnual ? (plans.premium.annual / 12).toFixed(2) : plans.premium.monthly}
                </span>
                <span className="text-muted-foreground">/{isAnnual ? 'mo billed annually' : 'month'}</span>
                {isAnnual && (
                  <div className="text-sm text-primary mt-2">{plans.premium.savings}</div>
                )}
              </div>
              <ul className="space-y-4">
                {plans.premium.features.map((feature, i) => (
                  <li key={i} className="flex items-center gap-2">
                    <Check className="h-5 w-5 text-primary" />
                    <span>{feature}</span>
                  </li>
                ))}
              </ul>
            </CardContent>
            <CardFooter>
              <Button 
                className="w-full" 
                onClick={() => setLocation("/signup")}
              >
                Get Premium
              </Button>
            </CardFooter>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default PricingPage;