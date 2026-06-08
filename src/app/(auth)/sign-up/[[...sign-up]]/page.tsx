import { SignUp } from "@clerk/nextjs"
import { Zap, CheckCircle } from "lucide-react"
import Link from "next/link"

export const metadata = {
  title: "Sign Up",
}

export default function SignUpPage() {
  return (
    <div className="min-h-screen flex">
      {/* Left Panel */}
      <div className="hidden lg:flex lg:w-1/2 bg-gradient-to-br from-purple-600 to-blue-700 items-center justify-center p-12 text-white">
        <div className="max-w-md">
          <div className="flex items-center gap-3 mb-8">
            <div className="h-10 w-10 rounded-xl bg-white/20 flex items-center justify-center">
              <Zap className="h-5 w-5" />
            </div>
            <span className="text-2xl font-bold">FinSight AI</span>
          </div>
          <h1 className="text-4xl font-bold mb-4">
            Start Managing Your Finances Intelligently
          </h1>
          <p className="text-purple-100 text-lg mb-8">
            Join thousands of SMEs using AI to make smarter financial decisions.
          </p>
          <div className="space-y-4">
            {[
              { title: "Free to Start", desc: "No credit card required for basic plan" },
              { title: "Instant Setup", desc: "Get your dashboard in under 2 minutes" },
              { title: "Secure & Private", desc: "Your data is encrypted and never shared" },
              { title: "AI Assistant", desc: "Ask questions about your finances anytime" },
            ].map((item) => (
              <div key={item.title} className="flex items-start gap-3">
                <CheckCircle className="h-5 w-5 text-purple-200 mt-0.5 shrink-0" />
                <div>
                  <p className="font-semibold text-sm">{item.title}</p>
                  <p className="text-purple-200 text-xs">{item.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Right Panel */}
      <div className="flex-1 flex items-center justify-center p-8">
        <div className="w-full max-w-md">
          <div className="mb-8 text-center lg:hidden">
            <Link href="/" className="inline-flex items-center gap-2">
              <div className="h-8 w-8 rounded-lg gradient-blue flex items-center justify-center">
                <Zap className="h-4 w-4 text-white" />
              </div>
              <span className="font-bold text-xl">FinSight AI</span>
            </Link>
          </div>
          <SignUp
            appearance={{
              elements: {
                rootBox: "w-full",
                card: "shadow-none border rounded-2xl",
                headerTitle: "text-2xl font-bold",
                headerSubtitle: "text-muted-foreground",
                socialButtonsBlockButton: "border hover:bg-accent",
                formButtonPrimary: "bg-gradient-to-r from-purple-600 to-blue-700",
                footerActionLink: "text-primary hover:text-primary/80",
              },
            }}
          />
        </div>
      </div>
    </div>
  )
}
