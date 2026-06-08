import { SignIn } from "@clerk/nextjs"
import { Zap } from "lucide-react"
import Link from "next/link"

export const metadata = {
  title: "Sign In",
}

export default function SignInPage() {
  return (
    <div className="min-h-screen flex">
      {/* Left Panel */}
      <div className="hidden lg:flex lg:w-1/2 gradient-blue items-center justify-center p-12 text-white">
        <div className="max-w-md">
          <div className="flex items-center gap-3 mb-8">
            <div className="h-10 w-10 rounded-xl bg-white/20 flex items-center justify-center">
              <Zap className="h-5 w-5" />
            </div>
            <span className="text-2xl font-bold">FinSight AI</span>
          </div>
          <h1 className="text-4xl font-bold mb-4 leading-tight">
            Your AI-Powered Financial Intelligence Platform
          </h1>
          <p className="text-blue-100 text-lg mb-8">
            Track expenses, manage invoices, forecast cash flow, and get AI-driven insights — all in one secure platform.
          </p>
          <div className="space-y-3">
            {[
              "Real-time financial dashboard",
              "AI Assistant with RAG architecture",
              "Deterministic cash flow forecasting",
              "Bank-grade security & compliance",
            ].map((item) => (
              <div key={item} className="flex items-center gap-2 text-sm">
                <div className="h-1.5 w-1.5 rounded-full bg-white" />
                {item}
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
          <SignIn
            appearance={{
              elements: {
                rootBox: "w-full",
                card: "shadow-none border rounded-2xl",
                headerTitle: "text-2xl font-bold",
                headerSubtitle: "text-muted-foreground",
                socialButtonsBlockButton: "border hover:bg-accent",
                formButtonPrimary: "gradient-blue",
                footerActionLink: "text-primary hover:text-primary/80",
              },
            }}
          />
        </div>
      </div>
    </div>
  )
}
