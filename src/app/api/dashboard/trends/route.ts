import { getAuth } from "@/lib/server-auth"
import { NextRequest } from "next/server"
import { prisma } from "@/lib/prisma"
import { apiSuccess, apiError } from "@/lib/rate-limit"
import { getMonthlyTrends } from "@/lib/financial-calculations"

export async function GET(request: NextRequest) {
  try {
    const { userId, orgId } = await getAuth()
    if (!userId) return apiError("Unauthorized", 401)

    const org = orgId
      ? await prisma.organization.findUnique({ where: { clerkOrgId: orgId } })
      : await prisma.organization.findFirst({ where: { clerkOrgId: `personal_${userId}` } })

    if (!org) return apiSuccess([])

    const months = parseInt(request.nextUrl.searchParams.get("months") ?? "12")
    const trends = await getMonthlyTrends(org.id, Math.min(months, 24))

    return apiSuccess(trends)
  } catch (error) {
    console.error("Trends API error:", error)
    return apiError("Failed to fetch trends", 500)
  }
}
