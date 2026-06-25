import { getAuth } from "@/lib/server-auth"
import { NextRequest } from "next/server"
import { prisma } from "@/lib/prisma"
import { apiSuccess, apiError, rateLimit } from "@/lib/rate-limit"
import { getDashboardMetrics } from "@/lib/financial-calculations"

const checkRateLimit = rateLimit({ limit: 60, windowMs: 60000 })

export async function GET(request: NextRequest) {
  // Rate limiting
  const rateLimitResponse = checkRateLimit(request)
  if (rateLimitResponse) return rateLimitResponse

  try {
    const { userId, orgId } = await getAuth()
    if (!userId) return apiError("Unauthorized", 401)

    // Get or create organization
    let organization = null
    if (orgId) {
      organization = await prisma.organization.findUnique({
        where: { clerkOrgId: orgId },
      })
    }

    // If no org, use a demo/personal org for the user
    if (!organization) {
      // Create a personal org for solo users
      const user = await prisma.user.upsert({
        where: { clerkId: userId },
        update: {},
        create: {
          clerkId: userId,
          email: "user@example.com",
          firstName: "User",
          lastName: "",
        },
      })

      organization = await prisma.organization.upsert({
        where: { clerkOrgId: `personal_${userId}` },
        update: {},
        create: {
          clerkOrgId: `personal_${userId}`,
          name: "My Business",
          slug: `personal-${userId.slice(0, 8)}`,
          members: {
            create: {
              userId: user.id,
              role: "ADMIN",
              joinedAt: new Date(),
            },
          },
        },
      })

      // Seed demo data if empty
      const txCount = await prisma.transaction.count({
        where: { organizationId: organization.id },
      })

      if (txCount === 0) {
        await seedDemoData(organization.id, user.id)
      }
    }

    const metrics = await getDashboardMetrics(organization.id)

    return apiSuccess(metrics)
  } catch (error) {
    console.error("Dashboard API error:", error)
    return apiError("Failed to fetch dashboard data", 500)
  }
}

// ─── Seed Demo Data ──────────────────────────────────────────
async function seedDemoData(organizationId: string, userId: string) {
  try {
    // Create categories
    const categories = await prisma.$transaction([
      prisma.category.create({
        data: { organizationId, name: "Sales", type: "INCOME", color: "#3b82f6", isDefault: true },
      }),
      prisma.category.create({
        data: { organizationId, name: "Services", type: "INCOME", color: "#06b6d4", isDefault: true },
      }),
      prisma.category.create({
        data: { organizationId, name: "Office Supplies", type: "EXPENSE", color: "#f59e0b", isDefault: true },
      }),
      prisma.category.create({
        data: { organizationId, name: "Marketing", type: "EXPENSE", color: "#ec4899", isDefault: true },
      }),
      prisma.category.create({
        data: { organizationId, name: "Software", type: "EXPENSE", color: "#8b5cf6", isDefault: true },
      }),
      prisma.category.create({
        data: { organizationId, name: "Payroll", type: "EXPENSE", color: "#ef4444", isDefault: true },
      }),
    ])

    // Create clients
    const client1 = await prisma.client.create({
      data: {
        organizationId,
        name: "Acme Corporation",
        email: "billing@acme.com",
        company: "Acme Corp",
        totalRevenue: 45000,
      },
    })

    const client2 = await prisma.client.create({
      data: {
        organizationId,
        name: "TechStart Inc",
        email: "accounts@techstart.io",
        company: "TechStart Inc",
        totalRevenue: 28000,
      },
    })

    // Create invoices
    const inv1 = await prisma.invoice.create({
      data: {
        organizationId,
        clientId: client1.id,
        createdById: userId,
        invoiceNumber: "INV-2024-001",
        status: "PAID",
        issueDate: new Date("2024-10-01"),
        dueDate: new Date("2024-10-31"),
        paidAt: new Date("2024-10-25"),
        subtotal: 15000,
        taxRate: 10,
        taxAmount: 1500,
        total: 16500,
        amountPaid: 16500,
        amountDue: 0,
        items: {
          create: [
            { description: "Web Development Services", quantity: 1, unitPrice: 15000, total: 15000, taxRate: 10 },
          ],
        },
      },
    })

    const inv2 = await prisma.invoice.create({
      data: {
        organizationId,
        clientId: client2.id,
        createdById: userId,
        invoiceNumber: "INV-2024-002",
        status: "OVERDUE",
        issueDate: new Date("2024-10-15"),
        dueDate: new Date("2024-11-14"),
        subtotal: 8500,
        taxRate: 10,
        taxAmount: 850,
        total: 9350,
        amountPaid: 0,
        amountDue: 9350,
        items: {
          create: [
            { description: "Consulting Services", quantity: 10, unitPrice: 850, total: 8500, taxRate: 10 },
          ],
        },
      },
    })

    // Create demo transactions (last 6 months)
    const transactionData = []
    const now = new Date()

    for (let m = 5; m >= 0; m--) {
      const month = new Date(now.getFullYear(), now.getMonth() - m, 1)

      // Income transactions
      transactionData.push(
        {
          organizationId,
          type: "INCOME" as const,
          amount: 15000 + Math.random() * 8000,
          description: "Client Payment - Acme Corporation",
          date: new Date(month.getFullYear(), month.getMonth(), 5),
          categoryId: categories[0].id,
        },
        {
          organizationId,
          type: "INCOME" as const,
          amount: 8000 + Math.random() * 4000,
          description: "Consulting Revenue",
          date: new Date(month.getFullYear(), month.getMonth(), 12),
          categoryId: categories[1].id,
        },
        // Expense transactions
        {
          organizationId,
          type: "EXPENSE" as const,
          amount: 500 + Math.random() * 300,
          description: "Office Supplies",
          date: new Date(month.getFullYear(), month.getMonth(), 8),
          categoryId: categories[2].id,
        },
        {
          organizationId,
          type: "EXPENSE" as const,
          amount: 2000 + Math.random() * 1000,
          description: "Marketing Campaign",
          date: new Date(month.getFullYear(), month.getMonth(), 15),
          categoryId: categories[3].id,
        },
        {
          organizationId,
          type: "EXPENSE" as const,
          amount: 1200 + Math.random() * 400,
          description: "Software Subscriptions",
          date: new Date(month.getFullYear(), month.getMonth(), 1),
          categoryId: categories[4].id,
        },
        {
          organizationId,
          type: "EXPENSE" as const,
          amount: 8000 + Math.random() * 2000,
          description: "Payroll",
          date: new Date(month.getFullYear(), month.getMonth(), 28),
          categoryId: categories[5].id,
        }
      )
    }

    await prisma.transaction.createMany({ data: transactionData })

    // Create some expenses
    await prisma.expense.createMany({
      data: [
        {
          organizationId,
          categoryId: categories[2].id,
          createdById: userId,
          amount: 350,
          description: "Printer cartridges",
          date: new Date(),
          status: "APPROVED",
          approvedById: userId,
        },
        {
          organizationId,
          categoryId: categories[3].id,
          createdById: userId,
          amount: 2500,
          description: "Google Ads Campaign",
          date: new Date(),
          status: "PENDING",
        },
      ],
    })

    console.log("Demo data seeded successfully")
  } catch (error) {
    console.error("Error seeding demo data:", error)
  }
}
