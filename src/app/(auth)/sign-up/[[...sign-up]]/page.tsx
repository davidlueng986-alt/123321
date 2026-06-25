"use client"

import { Zap, ArrowRight } from "lucide-react"
import Link from "next/link"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"

export default function SignUpPage() {
  const router = useRouter()

  return (
    <div className="min-h-screen flex items-center justify-center p-8">
      <div className="w-full max-w-md">
        <div className="mb-8 text-center">
          <Link href="/" className="inline-flex items-center gap-2 mb-6">
            <div className="h-8 w-8 rounded-lg bg-gradient-to-br from-blue-600 to-purple-700 flex items-center justify-center">
              <Zap className="h-4 w-4 text-white" />
            </div>
            <span className="font-bold text-xl">FinSight AI</span>
          </Link>
          <h2 className="text-2xl font-bold tracking-tight">Create your account</h2>
          <p className="text-muted-foreground mt-1">Get started with FinSight AI</p>
        </div>

        {/* Demo Mode Notice */}
        <div className="mb-6 rounded-xl border border-amber-200 bg-amber-50 p-4">
          <p className="text-sm font-semibold text-amber-800">Demo Mode Active</p>
          <p className="text-xs text-amber-700 mt-0.5">
            No registration required in demo mode. Click below to access the full dashboard.
          </p>
        </div>

        <Button
          className="w-full h-12 text-base bg-gradient-to-r from-blue-600 to-purple-600 text-white font-semibold rounded-xl"
          onClick={() => router.push("/dashboard")}
        >
          Enter Demo Dashboard
          <ArrowRight className="ml-2 h-5 w-5" />
        </Button>

        <p className="text-center text-sm mt-4">
          Already have an account?{" "}
          <Link href="/sign-in" className="text-primary hover:underline">Sign in</Link>
        </p>
      </div>
    </div>
  )
}
