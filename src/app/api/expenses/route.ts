import { auth } from "@clerk/nextjs/server"
import { NextRequest } from "next/server"
import { prisma } from "@/lib/prisma"
import { apiSuccess, apiError, rateLimit } from "@/lib/rate-limit"
import { createExpenseSchema, paginationSchema } from "@/lib/validations"
import { logAuditEvent } from "@/lib/auth"

const checkRateLimit = rateLimit({ limit: 60, windowMs: 60000 })

async function getOrg(userId: string, orgId: string | null) {
  return orgId
    ? await prisma.organization.findUnique({ where: { clerkOrgId: orgId } })
    : await prisma.organization.findFirst({ where: { clerkOrgId: `personal_${userId}` } })
}

// GET /api/expenses
export async function GET(request: NextRequest) {
  const rateLimitResponse = checkRateLimit(request)
  if (rateLimitResponse) return rateLimitResponse

  try {
    const { userId, orgId } = await auth()
    if (!userId) return apiError("Unauthorized", 401)

    const org = await getOrg(userId, orgId ?? null)
    if (!org) return apiSuccess({ expenses: [], total: 0 })

    const sp = request.nextUrl.searchParams
    const { page, limit } = paginationSchema.parse({ page: sp.get("page"), limit: sp.get("limit") })
    const status = sp.get("status")
    const categoryId = sp.get("categoryId")
    const from = sp.get("from")
    const to = sp.get("to")

    const where = {
      organizationId: org.id,
      ...(status && status !== "ALL" ? { status: status as "PENDING" | "APPROVED" | "REJECTED" } : {}),
      ...(categoryId ? { categoryId } : {}),
      ...(from || to ? {
        date: {
          ...(from ? { gte: new Date(from) } : {}),
          ...(to ? { lte: new Date(to) } : {}),
        },
      } : {}),
    }

    const [expenses, total] = await Promise.all([
      prisma.expense.findMany({
        where,
        include: {
          category: { select: { name: true, color: true } },
          vendor: { select: { name: true } },
          createdBy: { select: { firstName: true, lastName: true } },
        },
        orderBy: { date: "desc" },
        skip: (page - 1) * limit,
        take: limit,
      }),
      prisma.expense.count({ where }),
    ])

    // Calculate totals
    const totals = await prisma.expense.aggregate({
      where: { organizationId: org.id },
      _sum: { amount: true },
      _count: true,
    })

    return apiSuccess({
      expenses,
      total,
      pages: Math.ceil(total / limit),
      totalAmount: Number(totals._sum.amount ?? 0),
    })
  } catch (error) {
    console.error("Expenses GET error:", error)
    return apiError("Failed to fetch expenses", 500)
  }
}

// POST /api/expenses
export async function POST(request: NextRequest) {
  const rateLimitResponse = checkRateLimit(request)
  if (rateLimitResponse) return rateLimitResponse

  try {
    const { userId, orgId } = await auth()
    if (!userId) return apiError("Unauthorized", 401)

    const org = await getOrg(userId, orgId ?? null)
    if (!org) return apiError("Organization not found", 404)

    const user = await prisma.user.findUnique({ where: { clerkId: userId } })
    if (!user) return apiError("User not found", 404)

    const body = await request.json()
    const result = createExpenseSchema.safeParse(body)
    if (!result.success) {
      return apiError("Invalid data", 400, result.error.flatten())
    }

    const data = result.data

    const expense = await prisma.expense.create({
      data: {
        organizationId: org.id,
        createdById: user.id,
        ...data,
        date: new Date(data.date),
        tags: data.tags ?? [],
      },
      include: {
        category: { select: { name: true, color: true } },
      },
    })

    // Create expense transaction
    await prisma.transaction.create({
      data: {
        organizationId: org.id,
        type: "EXPENSE",
        amount: data.amount,
        description: data.description,
        date: new Date(data.date),
        categoryId: data.categoryId,
        expenseId: expense.id,
      },
    })

    await logAuditEvent({
      organizationId: org.id,
      userId: user.id,
      action: "CREATE",
      resource: "expenses",
      resourceId: expense.id,
      newValues: { amount: data.amount, description: data.description },
    })

    return apiSuccess(expense, 201)
  } catch (error) {
    console.error("Expense POST error:", error)
    return apiError("Failed to create expense", 500)
  }
}
