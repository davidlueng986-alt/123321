import { auth } from "@clerk/nextjs/server"
import { NextRequest } from "next/server"
import { prisma } from "@/lib/prisma"
import { apiSuccess, apiError } from "@/lib/rate-limit"
import { generateReportSchema } from "@/lib/validations"
import { getProfitLossReport, getExpensesByCategory, getMonthlyTrends } from "@/lib/financial-calculations"

async function getOrg(userId: string, orgId: string | null) {
  return orgId
    ? await prisma.organization.findUnique({ where: { clerkOrgId: orgId } })
    : await prisma.organization.findFirst({ where: { clerkOrgId: `personal_${userId}` } })
}

export async function POST(request: NextRequest) {
  try {
    const { userId, orgId } = await auth()
    if (!userId) return apiError("Unauthorized", 401)

    const org = await getOrg(userId, orgId ?? null)
    if (!org) return apiError("Organization not found", 404)

    const body = await request.json()
    const result = generateReportSchema.safeParse(body)
    if (!result.success) {
      return apiError("Invalid report parameters", 400, result.error.flatten())
    }

    const { type, name, from, to } = result.data
    const fromDate = new Date(from)
    const toDate = new Date(to)

    let reportData: Record<string, unknown> = {}

    switch (type) {
      case "PROFIT_LOSS":
        reportData = await getProfitLossReport(org.id, fromDate, toDate) as unknown as Record<string, unknown>
        break
      case "EXPENSE_SUMMARY":
        const categories = await getExpensesByCategory(org.id, { from: fromDate, to: toDate })
        reportData = {
          categories,
          totalExpenses: categories.reduce((s: number, c: { amount: number }) => s + c.amount, 0),
          period: { from: fromDate, to: toDate },
        }
        break
      case "REVENUE_TRENDS":
        const months = Math.max(1, Math.round((toDate.getTime() - fromDate.getTime()) / (1000 * 60 * 60 * 24 * 30)))
        const trends = await getMonthlyTrends(org.id, months)
        reportData = {
          trends,
          totalRevenue: trends.reduce((s: number, t: { revenue: number }) => s + t.revenue, 0),
          totalExpenses: trends.reduce((s: number, t: { expenses: number }) => s + t.expenses, 0),
          period: { from: fromDate, to: toDate },
        }
        break
      default:
        reportData = await getProfitLossReport(org.id, fromDate, toDate) as unknown as Record<string, unknown>
    }

    // Save report to DB
    const report = await prisma.report.create({
      data: {
        organizationId: org.id,
        type,
        name,
        parameters: { from, to },
        data: reportData as object,
        generatedAt: new Date(),
        expiresAt: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000), // 7 days
      },
    })

    return apiSuccess({ report, data: reportData }, 201)
  } catch (error) {
    console.error("Report generation error:", error)
    return apiError("Failed to generate report", 500)
  }
}

export async function GET(request: NextRequest) {
  try {
    const { userId, orgId } = await auth()
    if (!userId) return apiError("Unauthorized", 401)

    const org = await getOrg(userId, orgId ?? null)
    if (!org) return apiSuccess([])

    const reports = await prisma.report.findMany({
      where: { organizationId: org.id },
      orderBy: { generatedAt: "desc" },
      take: 20,
      select: {
        id: true,
        type: true,
        name: true,
        parameters: true,
        generatedAt: true,
        format: true,
      },
    })

    return apiSuccess(reports)
  } catch (error) {
    return apiError("Failed to fetch reports", 500)
  }
}
