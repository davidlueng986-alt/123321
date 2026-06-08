import Link from "next/link"
import {
  BarChart3, Bot, FileText, Shield, TrendingUp,
  Zap, ArrowRight, CheckCircle, Star, Globe, Lock
} from "lucide-react"

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-background">
      {/* Navigation */}
      <nav className="sticky top-0 z-50 border-b bg-background/95 backdrop-blur">
        <div className="container mx-auto max-w-7xl px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="flex h-8 w-8 items-center justify-center rounded-lg gradient-blue">
              <Zap className="h-4 w-4 text-white" />
            </div>
            <span className="font-bold text-lg">FinSight AI</span>
          </div>
          <div className="hidden md:flex items-center gap-6 text-sm">
            <a href="#features" className="text-muted-foreground hover:text-foreground transition-colors">Features</a>
            <a href="#security" className="text-muted-foreground hover:text-foreground transition-colors">Security</a>
            <a href="#pricing" className="text-muted-foreground hover:text-foreground transition-colors">Pricing</a>
          </div>
          <div className="flex items-center gap-3">
            <Link
              href="/sign-in"
              className="text-sm font-medium hover:text-primary transition-colors"
            >
              Sign In
            </Link>
            <Link
              href="/sign-up"
              className="inline-flex items-center gap-1.5 rounded-lg bg-primary px-4 py-2 text-sm font-medium text-primary-foreground hover:bg-primary/90 transition-colors"
            >
              Get Started Free
              <ArrowRight className="h-3.5 w-3.5" />
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero */}
      <section className="relative py-24 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-blue-50 via-background to-purple-50 dark:from-blue-950/20 dark:to-purple-950/20" />
        <div className="relative container mx-auto max-w-7xl px-6 text-center">
          <div className="inline-flex items-center gap-2 rounded-full border bg-background px-4 py-1.5 text-sm text-muted-foreground mb-8">
            <Bot className="h-3.5 w-3.5 text-primary" />
            Powered by GPT-4o with RAG Architecture
          </div>
          <h1 className="text-5xl md:text-7xl font-extrabold tracking-tight mb-6">
            AI Financial Intelligence
            <br />
            <span className="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
              for Your Business
            </span>
          </h1>
          <p className="text-xl text-muted-foreground max-w-3xl mx-auto mb-10">
            FinSight AI is a production-grade financial platform for SMEs. Track expenses,
            manage invoices, analyze cash flow, and get real-time AI insights — all with
            bank-grade security.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              href="/sign-up"
              className="inline-flex items-center gap-2 rounded-xl bg-primary px-8 py-4 text-base font-semibold text-primary-foreground hover:bg-primary/90 transition-colors shadow-lg"
            >
              Start for Free
              <ArrowRight className="h-4 w-4" />
            </Link>
            <Link
              href="/dashboard"
              className="inline-flex items-center gap-2 rounded-xl border bg-background px-8 py-4 text-base font-semibold hover:bg-accent transition-colors"
            >
              View Demo Dashboard
            </Link>
          </div>

          {/* Social proof */}
          <div className="flex items-center justify-center gap-6 mt-12 text-sm text-muted-foreground">
            <div className="flex items-center gap-1.5">
              <Shield className="h-4 w-4 text-emerald-500" />
              OWASP Compliant
            </div>
            <div className="flex items-center gap-1.5">
              <Lock className="h-4 w-4 text-blue-500" />
              SOC 2 Ready
            </div>
            <div className="flex items-center gap-1.5">
              <Globe className="h-4 w-4 text-purple-500" />
              Multi-currency Support
            </div>
          </div>
        </div>
      </section>

      {/* Features Grid */}
      <section id="features" className="py-24">
        <div className="container mx-auto max-w-7xl px-6">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold mb-4">Everything Your Business Needs</h2>
            <p className="text-muted-foreground text-lg max-w-2xl mx-auto">
              A complete financial intelligence platform built for production use
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {[
              {
                icon: Bot,
                title: "AI Financial Assistant",
                description: "Ask any question about your finances. AI uses RAG to retrieve real data and generate accurate responses — never invents numbers.",
                color: "from-blue-500 to-cyan-500",
              },
              {
                icon: BarChart3,
                title: "Real-time Dashboard",
                description: "Live financial metrics including revenue, expenses, profit margins, and cash flow with beautiful interactive charts.",
                color: "from-purple-500 to-pink-500",
              },
              {
                icon: FileText,
                title: "Invoice Management",
                description: "Create, send, and track invoices. Automatic overdue detection, payment recording, and client management.",
                color: "from-emerald-500 to-teal-500",
              },
              {
                icon: TrendingUp,
                title: "Cash Flow Forecasting",
                description: "Deterministic 3-month cash flow forecasts based on linear trend analysis of your historical data.",
                color: "from-orange-500 to-amber-500",
              },
              {
                icon: Shield,
                title: "Bank-Grade Security",
                description: "OWASP Top 10 compliant. CSRF protection, SQL injection prevention, rate limiting, audit logs, and MFA support.",
                color: "from-red-500 to-rose-500",
              },
              {
                icon: Zap,
                title: "AI Insights Engine",
                description: "Automated detection of expense spikes, revenue concentration, cash flow warnings, and unusual transactions.",
                color: "from-violet-500 to-purple-500",
              },
            ].map((feature) => (
              <div
                key={feature.title}
                className="group rounded-2xl border bg-card p-6 hover:shadow-lg transition-all duration-300 hover:-translate-y-1"
              >
                <div className={`inline-flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-br ${feature.color} mb-4`}>
                  <feature.icon className="h-6 w-6 text-white" />
                </div>
                <h3 className="text-lg font-semibold mb-2">{feature.title}</h3>
                <p className="text-muted-foreground text-sm leading-relaxed">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Security Section */}
      <section id="security" className="py-24 bg-muted/50">
        <div className="container mx-auto max-w-7xl px-6">
          <div className="grid md:grid-cols-2 gap-12 items-center">
            <div>
              <h2 className="text-4xl font-bold mb-4">
                Security You Can Trust
              </h2>
              <p className="text-muted-foreground text-lg mb-6">
                Built with enterprise-grade security standards. Your financial data is protected at every layer.
              </p>
              <div className="space-y-3">
                {[
                  "OWASP Top 10 compliance",
                  "CSRF & XSS protection",
                  "SQL Injection prevention via Prisma ORM",
                  "Rate limiting on all API endpoints",
                  "Complete audit logs",
                  "Role-based access control (Admin, Accountant, Employee)",
                  "Multi-factor authentication via Clerk",
                  "Encrypted sensitive data",
                ].map((item) => (
                  <div key={item} className="flex items-center gap-3">
                    <CheckCircle className="h-5 w-5 text-emerald-500 shrink-0" />
                    <span className="text-sm">{item}</span>
                  </div>
                ))}
              </div>
            </div>
            <div className="rounded-2xl border bg-card p-8">
              <h3 className="font-semibold text-xl mb-4">Tech Stack</h3>
              {[
                { category: "Frontend", items: ["Next.js 15 App Router", "TypeScript", "Tailwind CSS", "ShadCN UI", "React Query", "Zustand"] },
                { category: "Backend", items: ["Next.js API Routes", "Prisma ORM", "PostgreSQL", "Zod Validation"] },
                { category: "AI", items: ["OpenAI GPT-4o", "RAG Architecture", "OpenAI Embeddings", "Qdrant Vector DB"] },
                { category: "Auth", items: ["Clerk Authentication", "MFA", "RBAC", "Session Management"] },
              ].map((stack) => (
                <div key={stack.category} className="mb-4">
                  <p className="text-sm font-semibold text-primary mb-1">{stack.category}</p>
                  <div className="flex flex-wrap gap-1.5">
                    {stack.items.map((item) => (
                      <span key={item} className="text-xs rounded-full bg-muted px-2 py-1">{item}</span>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-24">
        <div className="container mx-auto max-w-3xl px-6 text-center">
          <div className="rounded-3xl bg-gradient-to-br from-blue-600 to-purple-700 p-12 text-white">
            <h2 className="text-4xl font-bold mb-4">
              Ready to Transform Your Financial Intelligence?
            </h2>
            <p className="text-blue-100 text-lg mb-8">
              Join businesses already using FinSight AI to make smarter financial decisions.
            </p>
            <Link
              href="/sign-up"
              className="inline-flex items-center gap-2 rounded-xl bg-white px-8 py-4 text-base font-semibold text-blue-700 hover:bg-blue-50 transition-colors shadow-lg"
            >
              Get Started Free
              <ArrowRight className="h-4 w-4" />
            </Link>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t py-8">
        <div className="container mx-auto max-w-7xl px-6">
          <div className="flex items-center justify-between text-sm text-muted-foreground">
            <div className="flex items-center gap-2">
              <div className="h-6 w-6 rounded-md gradient-blue flex items-center justify-center">
                <Zap className="h-3 w-3 text-white" />
              </div>
              <span>FinSight AI © 2024</span>
            </div>
            <div className="flex gap-6">
              <a href="#" className="hover:text-foreground transition-colors">Privacy</a>
              <a href="#" className="hover:text-foreground transition-colors">Terms</a>
              <a href="#" className="hover:text-foreground transition-colors">Security</a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}
