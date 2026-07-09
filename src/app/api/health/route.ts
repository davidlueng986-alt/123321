import { NextResponse } from "next/server"

import { getRedisStatus } from "@/lib/redis/client"

export async function GET() {
  return NextResponse.json({
    status: "ok",
    service: "FinSight AI",
    version: "1.0.0",
    timestamp: new Date().toISOString(),
    environment: process.env.NODE_ENV,
    redis: getRedisStatus(),
  })
}
