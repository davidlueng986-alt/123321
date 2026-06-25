"use client"

import { Zap, Bot, TrendingUp, Shield, BarChart3, ArrowRight } from "lucide-react"
import Link from "next/link"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"

export default function SignInPage() {
  const router = useRouter()

  const handleDemoLogin = () => {
    // In demo mode, just redirect to dashboard directly
    router.push("/dashboard")
  }

  return (
    <div className="min-h-screen flex">
      {/* Left Panel */}
      <div className="hidden lg:flex lg:w-1/2 bg-gradient-to-br from-blue-600 to-purple-700 items-center justify-center p-12 text-white">
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
              { icon: BarChart3, text: "Real-time financial dashboard" },
              { icon: Bot, text: "AI Assistant with RAG architecture" },
              { icon: TrendingUp, text: "Deterministic cash flow forecasting" },
              { icon: Shield, text: "Bank-grade security & compliance" },
            ].map((item) => (
              <div key={item.text} className="flex items-center gap-3 text-sm">
                <item.icon className="h-4 w-4 text-blue-200 shrink-0" />
                <span>{item.text}</span>
              </div>
            ))}
          </div>

          {/* Demo data preview */}
          <div className="mt-10 rounded-2xl bg-white/10 p-4 border border-white/20">
            <p className="text-xs text-blue-200 mb-3 font-medium uppercase tracking-wide">Live Demo Data Preview</p>
            <div className="grid grid-cols-2 gap-3">
              {[
                { label: "Revenue", value: "$124,500" },
                { label: "Expenses", value: "$78,300" },
                { label: "Profit", value: "$46,200" },
                { label: "Invoices", value: "23 active" },
              ].map((stat) => (
                <div key={stat.label} className="rounded-lg bg-white/10 p-2.5">
                  <p className="text-[10px] text-blue-200">{stat.label}</p>
                  <p className="text-sm font-bold">{stat.value}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Right Panel */}
      <div className="flex-1 flex items-center justify-center p-8">
        <div className="w-full max-w-md">
          <div className="mb-8 text-center">
            <Link href="/" className="inline-flex items-center gap-2 mb-6">
              <div className="h-8 w-8 rounded-lg bg-gradient-to-br from-blue-600 to-purple-700 flex items-center justify-center">
                <Zap className="h-4 w-4 text-white" />
              </div>
              <span className="font-bold text-xl">FinSight AI</span>
            </Link>
            <h2 className="text-2xl font-bold tracking-tight">Welcome back</h2>
            <p className="text-muted-foreground mt-1">Sign in to your financial dashboard</p>
          </div>

          {/* Demo Mode Notice */}
          <div className="mb-6 rounded-xl border border-amber-200 bg-amber-50 p-4">
            <div className="flex items-start gap-3">
              <div className="h-6 w-6 rounded-full bg-amber-400 flex items-center justify-center shrink-0 mt-0.5">
                <Zap className="h-3.5 w-3.5 text-white" />
              </div>
              <div>
                <p className="text-sm font-semibold text-amber-800">Demo Mode Active</p>
                <p className="text-xs text-amber-700 mt-0.5">
                  This is a fully functional demo with pre-seeded financial data. No credentials required — click the button below to explore all features.
                </p>
              </div>
            </div>
          </div>

          {/* Demo Sign In Button */}
          <Button
            className="w-full h-12 text-base bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white font-semibold rounded-xl shadow-lg hover:shadow-xl transition-all"
            onClick={handleDemoLogin}
          >
            Enter Demo Dashboard
            <ArrowRight className="ml-2 h-5 w-5" />
          </Button>

          <p className="text-center text-xs text-muted-foreground mt-4">
            By continuing, you agree to FinSight AI's Terms of Service and Privacy Policy
          </p>

          {/* Feature highlights */}
          <div className="mt-8 pt-8 border-t">
            <p className="text-center text-xs text-muted-foreground mb-4">What you'll find inside</p>
            <div className="grid grid-cols-3 gap-3">
              {[
                { icon: BarChart3, label: "Dashboard", color: "text-blue-600" },
                { icon: TrendingUp, label: "Cash Flow", color: "text-emerald-600" },
                { icon: Bot, label: "AI Assistant", color: "text-purple-600" },
              ].map((f) => (
                <div key={f.label} className="flex flex-col items-center gap-1.5 rounded-lg border p-3 text-center">
                  <f.icon className={`h-5 w-5 ${f.color}`} />
                  <span className="text-xs font-medium">{f.label}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
