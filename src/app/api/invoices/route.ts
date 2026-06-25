import { getAuth } from "@/lib/server-auth"
import { NextRequest } from "next/server"
import { prisma } from "@/lib/prisma"
import { apiSuccess, apiError, rateLimit } from "@/lib/rate-limit"
import { createInvoiceSchema, paginationSchema } from "@/lib/validations"
import { logAuditEvent } from "@/lib/auth"
import { Decimal } from "@prisma/client/runtime/library"

const checkRateLimit = rateLimit({ limit: 60, windowMs: 60000 })

// GET /api/invoices - List invoices
export async function GET(request: NextRequest) {
  const rateLimitResponse = checkRateLimit(request)
  if (rateLimitResponse) return rateLimitResponse

  try {
    const { userId, orgId } = await getAuth()
    if (!userId) return apiError("Unauthorized", 401)

    const org = orgId
      ? await prisma.organization.findUnique({ where: { clerkOrgId: orgId } })
      : await prisma.organization.findFirst({ where: { clerkOrgId: `personal_${userId}` } })
    if (!org) return apiSuccess({ invoices: [], total: 0, pages: 0 })

    const user = await prisma.user.findUnique({ where: { clerkId: userId } })
    if (!user) return apiError("User not found", 404)

    const searchParams = request.nextUrl.searchParams
    const { page, limit } = paginationSchema.parse({
      page: searchParams.get("page"),
      limit: searchParams.get("limit"),
    })
    const status = searchParams.get("status")
    const search = searchParams.get("search")

    const where = {
      organizationId: org.id,
      ...(status && status !== "ALL" ? { status: status as "DRAFT" | "SENT" | "PAID" | "OVERDUE" | "CANCELLED" } : {}),
      ...(search ? {
        OR: [
          { invoiceNumber: { contains: search, mode: "insensitive" as const } },
          { client: { name: { contains: search, mode: "insensitive" as const } } },
        ],
      } : {}),
    }

    const [invoices, total] = await Promise.all([
      prisma.invoice.findMany({
        where,
        include: {
          client: { select: { name: true, company: true } },
          items: true,
          payments: true,
        },
        orderBy: { createdAt: "desc" },
        skip: (page - 1) * limit,
        take: limit,
      }),
      prisma.invoice.count({ where }),
    ])

    // Check and update overdue status deterministically
    const now = new Date()
    const overdueUpdates = invoices
      .filter((inv) => inv.status === "SENT" && new Date(inv.dueDate) < now)
      .map((inv) => inv.id)

    if (overdueUpdates.length > 0) {
      await prisma.invoice.updateMany({
        where: { id: { in: overdueUpdates } },
        data: { status: "OVERDUE" },
      })
    }

    return apiSuccess({
      invoices,
      total,
      pages: Math.ceil(total / limit),
      page,
    })
  } catch (error) {
    console.error("Invoices GET error:", error)
    return apiError("Failed to fetch invoices", 500)
  }
}

// POST /api/invoices - Create invoice
export async function POST(request: NextRequest) {
  const rateLimitResponse = checkRateLimit(request)
  if (rateLimitResponse) return rateLimitResponse

  try {
    const { userId, orgId } = await getAuth()
    if (!userId) return apiError("Unauthorized", 401)

    const org = orgId
      ? await prisma.organization.findUnique({ where: { clerkOrgId: orgId } })
      : await prisma.organization.findFirst({ where: { clerkOrgId: `personal_${userId}` } })
    if (!org) return apiError("Organization not found", 404)

    const user = await prisma.user.findUnique({ where: { clerkId: userId } })
    if (!user) return apiError("User not found", 404)

    const body = await request.json()
    const data = createInvoiceSchema.safeParse(body)
    if (!data.success) {
      return apiError("Invalid data", 400, data.error.flatten())
    }

    const { items, taxRate, discountAmount, ...invoiceData } = data.data

    // Calculate amounts deterministically
    const subtotal = items.reduce((sum, item) => sum + item.quantity * item.unitPrice, 0)
    const discount = discountAmount ?? 0
    const taxAmount = ((subtotal - discount) * (taxRate ?? 0)) / 100
    const total = subtotal - discount + taxAmount
    const amountDue = total

    const invoice = await prisma.invoice.create({
      data: {
        organizationId: org.id,
        createdById: user.id,
        ...invoiceData,
        issueDate: new Date(invoiceData.issueDate),
        dueDate: new Date(invoiceData.dueDate),
        subtotal,
        taxRate: taxRate ?? 0,
        taxAmount,
        discountAmount: discount,
        total,
        amountDue,
        items: {
          create: items.map((item, index) => ({
            description: item.description,
            quantity: item.quantity,
            unitPrice: item.unitPrice,
            total: item.quantity * item.unitPrice,
            taxRate: item.taxRate ?? 0,
            sortOrder: index,
          })),
        },
      },
      include: {
        items: true,
        client: { select: { name: true } },
      },
    })

    // Create income transaction
    await prisma.transaction.create({
      data: {
        organizationId: org.id,
        type: "INCOME",
        amount: total,
        description: `Invoice ${invoice.invoiceNumber}`,
        date: new Date(invoiceData.issueDate),
        invoiceId: invoice.id,
      },
    })

    // Audit log
    await logAuditEvent({
      organizationId: org.id,
      userId: user.id,
      action: "CREATE",
      resource: "invoices",
      resourceId: invoice.id,
      newValues: { invoiceNumber: invoice.invoiceNumber, total },
      ipAddress: request.headers.get("x-forwarded-for") ?? undefined,
    })

    return apiSuccess(invoice, 201)
  } catch (error) {
    console.error("Invoice POST error:", error)
    return apiError("Failed to create invoice", 500)
  }
}
