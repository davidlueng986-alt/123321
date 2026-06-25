import { getAuth } from "@/lib/server-auth"
import { prisma } from "@/lib/prisma"
import { apiSuccess, apiError } from "@/lib/rate-limit"

export async function GET() {
  try {
    const { userId, orgId } = await getAuth()
    if (!userId) return apiError("Unauthorized", 401)

    const org = orgId
      ? await prisma.organization.findUnique({ where: { clerkOrgId: orgId } })
      : await prisma.organization.findFirst({ where: { clerkOrgId: `personal_${userId}` } })

    if (!org) return apiSuccess({ transactions: [], invoices: [] })

    const [transactions, invoices] = await Promise.all([
      prisma.transaction.findMany({
        where: { organizationId: org.id },
        orderBy: { date: "desc" },
        take: 10,
        include: { category: { select: { name: true, color: true } } },
      }),
      prisma.invoice.findMany({
        where: { organizationId: org.id, status: { in: ["OVERDUE", "SENT", "VIEWED"] } },
        orderBy: { dueDate: "asc" },
        take: 5,
        include: { client: { select: { name: true } } },
      }),
    ])

    return apiSuccess({ transactions, invoices })
  } catch (error) {
    console.error("Activity API error:", error)
    return apiError("Failed to fetch activity", 500)
  }
}
