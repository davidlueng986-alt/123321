import { clerkMiddleware, createRouteMatcher } from "@clerk/nextjs/server"
import { NextResponse } from "next/server"
import type { NextRequest } from "next/server"

// Define public routes that don't require authentication
const isPublicRoute = createRouteMatcher([
  "/",
  "/sign-in(.*)",
  "/sign-up(.*)",
  "/api/webhooks(.*)",
  "/api/health",
])

// Define API routes that require auth but no org
const isApiRoute = createRouteMatcher(["/api(.*)"])

export default clerkMiddleware(async (auth, request: NextRequest) => {
  const { userId, orgId } = await auth()

  // Allow public routes without auth
  if (isPublicRoute(request)) {
    return NextResponse.next()
  }

  // Require auth for all other routes
  if (!userId) {
    const signInUrl = new URL("/sign-in", request.url)
    signInUrl.searchParams.set("redirect_url", request.url)
    return NextResponse.redirect(signInUrl)
  }

  // Security headers
  const response = NextResponse.next()
  response.headers.set("X-Content-Type-Options", "nosniff")
  response.headers.set("X-Frame-Options", "DENY")
  response.headers.set("X-XSS-Protection", "1; mode=block")
  response.headers.set("Referrer-Policy", "strict-origin-when-cross-origin")

  // CSRF protection for mutations
  if (
    isApiRoute(request) &&
    ["POST", "PUT", "PATCH", "DELETE"].includes(request.method)
  ) {
    const origin = request.headers.get("origin")
    const host = request.headers.get("host")

    if (origin && host) {
      const originHost = new URL(origin).host
      if (originHost !== host) {
        // Allow from same host only (CSRF protection)
        // In production, also check against allowed origins list
        const allowedOrigins = [
          process.env.NEXT_PUBLIC_APP_URL ?? "",
          "http://localhost:3000",
        ]
        if (!allowedOrigins.some((o) => origin.startsWith(o))) {
          return NextResponse.json(
            { error: "CSRF validation failed" },
            { status: 403 }
          )
        }
      }
    }
  }

  return response
})

export const config = {
  matcher: [
    // Skip Next.js internals and all static files
    "/((?!_next|[^?]*\\.(?:html?|css|js(?!on)|jpe?g|webp|png|gif|svg|ttf|woff2?|ico|csv|docx?|xlsx?|zip|webmanifest)).*)",
    // Always run for API routes
    "/(api|trpc)(.*)",
  ],
}
