import { auth } from "@clerk/nextjs/server"
import { NextRequest } from "next/server"
import { prisma } from "@/lib/prisma"
import { apiSuccess, apiError } from "@/lib/rate-limit"
import { getCashFlowData, generateCashFlowForecast } from "@/lib/financial-calculations"

async function getOrg(userId: string, orgId: string | null) {
  return orgId
    ? await prisma.organization.findUnique({ where: { clerkOrgId: orgId } })
    : await prisma.organization.findFirst({ where: { clerkOrgId: `personal_${userId}` } })
}

export async function GET(request: NextRequest) {
  try {
    const { userId, orgId } = await auth()
    if (!userId) return apiError("Unauthorized", 401)

    const org = await getOrg(userId, orgId ?? null)
    if (!org) return apiSuccess({ historical: [], forecast: [] })

    const months = parseInt(request.nextUrl.searchParams.get("months") ?? "6")
    const forecastMonths = parseInt(request.nextUrl.searchParams.get("forecastMonths") ?? "3")

    // All calculations are deterministic - NO AI calculations
    const [historical, forecast] = await Promise.all([
      getCashFlowData(org.id, months),
      generateCashFlowForecast(org.id, forecastMonths),
    ])

    // Save forecasts to DB for history tracking
    if (forecast.length > 0) {
      await prisma.$transaction(
        forecast.map((f) =>
          prisma.cashFlowForecast.upsert({
            where: {
              id: `${org.id}_${f.forecastDate.toISOString().slice(0, 7)}`,
            },
            update: {
              expectedIncome: f.expectedIncome,
              expectedExpenses: f.expectedExpenses,
              expectedBalance: f.expectedBalance,
              confidence: f.confidence,
            },
            create: {
              id: `${org.id}_${f.forecastDate.toISOString().slice(0, 7)}`,
              organizationId: org.id,
              forecastDate: f.forecastDate,
              period: "monthly",
              expectedIncome: f.expectedIncome,
              expectedExpenses: f.expectedExpenses,
              expectedBalance: f.expectedBalance,
              confidence: f.confidence,
              methodology: f.methodology,
            },
          })
        )
      )
    }

    return apiSuccess({ historical, forecast })
  } catch (error) {
    console.error("Cash flow error:", error)
    return apiError("Failed to calculate cash flow", 500)
  }
}
