import { Mail, MessageCircle, Clock, Shield } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"

export default function HelpPage() {
  const supportEmail = "support@xyz.com"

  return (
    <div className="flex justify-center items-center min-h-screen">
    <div className="text-center"></div>
    <div className="min-h-screen bg-gradient-to-b from-primary/10 to-background">
      <div className="container max-w-4xl py-16 px-4 md:py-24">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold tracking-tight mb-4">Need Help?</h1>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
            We're here to assist you with any questions or issues you might have.
          </p>
        </div>

        <Card className="w-full bg-card/80 backdrop-blur-sm border-primary/20 shadow-lg">
          <CardContent className="p-8 flex flex-col items-center">
            <div className="h-16 w-16 rounded-full bg-primary/20 flex items-center justify-center mb-6">
              <Mail className="h-8 w-8 text-primary" />
            </div>

            <h2 className="text-2xl font-semibold mb-2">Contact Support</h2>
            <p className="text-muted-foreground mb-6 text-center">
              Send us an email and we'll get back to you as soon as possible.
            </p>

            <div className="bg-primary/10 rounded-lg p-4 w-full text-center mb-6">
              <a
                // href={`mailto:${supportEmail}`}
                className="text-xl md:text-2xl font-medium text-primary hover:underline"
              >
                {supportEmail}
              </a>
            </div>

            <Button asChild size="lg" className="gap-2">
              <a href={`mailto:${supportEmail}`}>
                <Mail className="h-4 w-4" />
                Send Email
              </a>
            </Button>
          </CardContent>
        </Card>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-12">
          <div className="bg-card p-6 rounded-lg border shadow-sm">
            <MessageCircle className="h-8 w-8 text-primary mb-4" />
            <h3 className="text-lg font-medium mb-2">What to Include</h3>
            <p className="text-muted-foreground">
              Please include your account details, a clear description of the issue, and any relevant screenshots.
            </p>
          </div>

          <div className="bg-card p-6 rounded-lg border shadow-sm">
            <Clock className="h-8 w-8 text-primary mb-4" />
            <h3 className="text-lg font-medium mb-2">Response Time</h3>
            <p className="text-muted-foreground">
              We typically respond to all inquiries within 24 hours during business days.
            </p>
          </div>

          <div className="bg-card p-6 rounded-lg border shadow-sm">
            <Shield className="h-8 w-8 text-primary mb-4" />
            <h3 className="text-lg font-medium mb-2">Privacy & Security</h3>
            <p className="text-muted-foreground">
              Your information is secure. We never share your details with third parties.
            </p>
          </div>
        </div>
      </div>
    </div>
    </div>
  )
}

