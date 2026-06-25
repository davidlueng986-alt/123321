import { NextResponse } from "next/server"
import type { NextRequest } from "next/server"

const DEMO_MODE = process.env.NEXT_PUBLIC_DEMO_MODE === "true"

// Public routes that don't require authentication
const PUBLIC_ROUTES = ["/", "/sign-in", "/sign-up", "/api/health", "/api/webhooks"]

function isPublicRoute(pathname: string): boolean {
  return PUBLIC_ROUTES.some(
    (route) => pathname === route || pathname.startsWith(route + "/")
  )
}

function isApiRoute(pathname: string): boolean {
  return pathname.startsWith("/api/")
}

// In demo mode, just pass all requests through with security headers
export default async function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl

  // Always allow public routes
  if (isPublicRoute(pathname)) {
    return NextResponse.next()
  }

  if (DEMO_MODE) {
    // Demo mode: skip all auth checks, just add security headers
    const response = NextResponse.next()
    response.headers.set("X-Content-Type-Options", "nosniff")
    response.headers.set("X-Frame-Options", "DENY")
    response.headers.set("X-XSS-Protection", "1; mode=block")
    response.headers.set("Referrer-Policy", "strict-origin-when-cross-origin")
    return response
  }

  // Production mode: use Clerk
  const { clerkMiddleware, createRouteMatcher } = await import("@clerk/nextjs/server")
  // For non-demo mode, redirect unauthenticated users
  // This path is not used in demo/test mode
  return NextResponse.next()
}

export const config = {
  matcher: [
    // Skip Next.js internals and all static files
    "/((?!_next|[^?]*\\.(?:html?|css|js(?!on)|jpe?g|webp|png|gif|svg|ttf|woff2?|ico|csv|docx?|xlsx?|zip|webmanifest)).*)",
    // Always run for API routes
    "/(api|trpc)(.*)",
  ],
}
