import { getAuth } from "@/lib/server-auth"
import { NextRequest } from "next/server"
import { prisma } from "@/lib/prisma"
import { apiSuccess, apiError } from "@/lib/rate-limit"
import { getFinancialInsightsData } from "@/lib/financial-calculations"
import { generateResponse } from "@/lib/openai"

async function getOrg(userId: string, orgId: string | null) {
  return orgId
    ? await prisma.organization.findUnique({ where: { clerkOrgId: orgId } })
    : await prisma.organization.findFirst({ where: { clerkOrgId: `personal_${userId}` } })
}

export async function GET(request: NextRequest) {
  try {
    const { userId, orgId } = await getAuth()
    if (!userId) return apiError("Unauthorized", 401)

    const org = await getOrg(userId, orgId ?? null)
    if (!org) return apiSuccess([])

    // Get pre-computed insights
    const storedInsights = await prisma.insight.findMany({
      where: { organizationId: org.id, isDismissed: false },
      orderBy: { createdAt: "desc" },
      take: 10,
    })

    // Always recalculate fresh insights
    const { insights, trends, categories, invoiceStats, topClients } =
      await getFinancialInsightsData(org.id)

    // Generate AI narratives for each insight (using actual calculated data)
    const enrichedInsights = await Promise.all(
      insights.slice(0, 5).map(async (insight) => {
        let aiNarrative = ""
        try {
          const context = `Insight type: ${insight.type}\nMetric: ${insight.metric}\nValue: ${insight.value}\nSeverity: ${insight.severity}`
          const result = await generateResponse(
            [{ role: "user", content: `Generate a brief 2-sentence business insight about: ${insight.metric} with value ${insight.value}. The insight type is ${insight.type}. Be specific with the number.` }],
            context
          )
          aiNarrative = result.content
        } catch {
          aiNarrative = `${insight.metric}: ${insight.value.toFixed(1)}`
        }

        return { ...insight, aiNarrative }
      })
    )

    return apiSuccess({
      insights: enrichedInsights,
      storedInsights,
      trends,
      categories,
      invoiceStats,
      topClients,
    })
  } catch (error) {
    console.error("Insights error:", error)
    return apiError("Failed to generate insights", 500)
  }
}
