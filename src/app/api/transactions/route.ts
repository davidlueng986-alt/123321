import { auth } from "@clerk/nextjs/server"
import { NextRequest } from "next/server"
import { prisma } from "@/lib/prisma"
import { apiSuccess, apiError, rateLimit } from "@/lib/rate-limit"
import { createTransactionSchema, paginationSchema } from "@/lib/validations"

const checkRateLimit = rateLimit({ limit: 100, windowMs: 60000 })

async function getOrg(userId: string, orgId: string | null) {
  return orgId
    ? await prisma.organization.findUnique({ where: { clerkOrgId: orgId } })
    : await prisma.organization.findFirst({ where: { clerkOrgId: `personal_${userId}` } })
}

export async function GET(request: NextRequest) {
  const rateLimitResponse = checkRateLimit(request)
  if (rateLimitResponse) return rateLimitResponse

  try {
    const { userId, orgId } = await auth()
    if (!userId) return apiError("Unauthorized", 401)

    const org = await getOrg(userId, orgId ?? null)
    if (!org) return apiSuccess({ transactions: [], total: 0 })

    const sp = request.nextUrl.searchParams
    const { page, limit } = paginationSchema.parse({ page: sp.get("page"), limit: sp.get("limit") })
    const type = sp.get("type")
    const from = sp.get("from")
    const to = sp.get("to")
    const search = sp.get("search")

    const where = {
      organizationId: org.id,
      ...(type && type !== "ALL" ? { type: type as "INCOME" | "EXPENSE" | "TRANSFER" } : {}),
      ...(from || to ? {
        date: {
          ...(from ? { gte: new Date(from) } : {}),
          ...(to ? { lte: new Date(to) } : {}),
        },
      } : {}),
      ...(search ? {
        description: { contains: search, mode: "insensitive" as const },
      } : {}),
    }

    const [transactions, total, summary] = await Promise.all([
      prisma.transaction.findMany({
        where,
        include: {
          category: { select: { name: true, color: true } },
        },
        orderBy: { date: "desc" },
        skip: (page - 1) * limit,
        take: limit,
      }),
      prisma.transaction.count({ where }),
      prisma.transaction.groupBy({
        by: ["type"],
        where: { organizationId: org.id },
        _sum: { amount: true },
      }),
    ])

    const summaryMap: Record<string, number> = {}
    for (const s of summary) {
      summaryMap[s.type] = Number(s._sum.amount ?? 0)
    }

    return apiSuccess({
      transactions,
      total,
      pages: Math.ceil(total / limit),
      summary: {
        income: summaryMap.INCOME ?? 0,
        expenses: summaryMap.EXPENSE ?? 0,
        net: (summaryMap.INCOME ?? 0) - (summaryMap.EXPENSE ?? 0),
      },
    })
  } catch (error) {
    console.error("Transactions GET error:", error)
    return apiError("Failed to fetch transactions", 500)
  }
}

export async function POST(request: NextRequest) {
  const rateLimitResponse = checkRateLimit(request)
  if (rateLimitResponse) return rateLimitResponse

  try {
    const { userId, orgId } = await auth()
    if (!userId) return apiError("Unauthorized", 401)

    const org = await getOrg(userId, orgId ?? null)
    if (!org) return apiError("Organization not found", 404)

    const body = await request.json()
    const result = createTransactionSchema.safeParse(body)
    if (!result.success) {
      return apiError("Invalid data", 400, result.error.flatten())
    }

    const data = result.data
    const transaction = await prisma.transaction.create({
      data: {
        organizationId: org.id,
        ...data,
        date: new Date(data.date),
        tags: data.tags ?? [],
      },
      include: { category: true },
    })

    return apiSuccess(transaction, 201)
  } catch (error) {
    return apiError("Failed to create transaction", 500)
  }
}
