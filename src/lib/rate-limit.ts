import { NextRequest, NextResponse } from "next/server"

import { getRedis } from "@/lib/redis/client"

const rateLimitMap = new Map<string, { count: number; resetTime: number }>()

const CLEANUP_INTERVAL = 60 * 1000

setInterval(() => {
  const now = Date.now()
  for (const [key, value] of rateLimitMap.entries()) {
    if (now > value.resetTime) {
      rateLimitMap.delete(key)
    }
  }
}, CLEANUP_INTERVAL)

export interface RateLimitConfig {
  limit?: number
  windowMs?: number
}

function checkInMemoryRateLimit(
  key: string,
  limit: number,
  windowMs: number,
): NextResponse | null {
  const now = Date.now()
  const current = rateLimitMap.get(key)

  if (!current || now > current.resetTime) {
    rateLimitMap.set(key, { count: 1, resetTime: now + windowMs })
    return null
  }

  if (current.count >= limit) {
    const retryAfter = Math.ceil((current.resetTime - now) / 1000)
    return NextResponse.json(
      {
        error: "Too many requests",
        message: `Rate limit exceeded. Try again in ${retryAfter} seconds.`,
        retryAfter,
      },
      {
        status: 429,
        headers: {
          "X-RateLimit-Limit": limit.toString(),
          "X-RateLimit-Remaining": "0",
          "X-RateLimit-Reset": current.resetTime.toString(),
          "Retry-After": retryAfter.toString(),
        },
      },
    )
  }

  current.count++
  return null
}

async function checkRedisRateLimit(
  key: string,
  limit: number,
  windowMs: number,
): Promise<NextResponse | null> {
  const redis = getRedis()
  if (!redis) {
    return checkInMemoryRateLimit(key, limit, windowMs)
  }

  const redisKey = `finsight:ratelimit:${key}`
  const windowSec = Math.max(1, Math.ceil(windowMs / 1000))

  try {
    const count = await redis.incr(redisKey)
    if (count === 1) {
      await redis.expire(redisKey, windowSec)
    }

    const ttlMs = await redis.pttl(redisKey)
    const resetTime = ttlMs > 0 ? Date.now() + ttlMs : Date.now() + windowMs

    if (count > limit) {
      const retryAfter = Math.ceil((resetTime - Date.now()) / 1000)
      return NextResponse.json(
        {
          error: "Too many requests",
          message: `Rate limit exceeded. Try again in ${retryAfter} seconds.`,
          retryAfter,
        },
        {
          status: 429,
          headers: {
            "X-RateLimit-Limit": limit.toString(),
            "X-RateLimit-Remaining": "0",
            "X-RateLimit-Reset": resetTime.toString(),
            "Retry-After": retryAfter.toString(),
          },
        },
      )
    }

    return null
  } catch (err) {
    console.error("[finsight][redis] rate limit failed:", err)
    return checkInMemoryRateLimit(key, limit, windowMs)
  }
}

export function rateLimit(config: RateLimitConfig = {}) {
  const limit = config.limit ?? parseInt(process.env.RATE_LIMIT_REQUESTS ?? "100")
  const windowMs = config.windowMs ?? parseInt(process.env.RATE_LIMIT_WINDOW_MS ?? "60000")

  return async function checkRateLimit(request: NextRequest): Promise<NextResponse | null> {
    const ip =
      request.headers.get("x-forwarded-for")?.split(",")[0] ??
      request.headers.get("x-real-ip") ??
      "unknown"

    const key = `${ip}:${request.nextUrl.pathname}`
    return checkRedisRateLimit(key, limit, windowMs)
  }
}

export function apiSuccess<T>(data: T, status = 200) {
  return NextResponse.json({ success: true, data }, { status })
}

export function apiError(message: string, status = 400, details?: unknown) {
  return NextResponse.json(
    {
      success: false,
      error: message,
      details: process.env.NODE_ENV === "development" ? details : undefined,
    },
    { status },
  )
}

export function addSecurityHeaders(response: NextResponse): NextResponse {
  response.headers.set("X-Content-Type-Options", "nosniff")
  response.headers.set("X-Frame-Options", "DENY")
  response.headers.set("X-XSS-Protection", "1; mode=block")
  response.headers.set("Referrer-Policy", "strict-origin-when-cross-origin")
  response.headers.set(
    "Permissions-Policy",
    "camera=(), microphone=(), geolocation=()",
  )
  return response
}
