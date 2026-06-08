import { auth } from "@clerk/nextjs/server"
import { NextRequest } from "next/server"
import { prisma } from "@/lib/prisma"
import { apiSuccess, apiError } from "@/lib/rate-limit"
import { updateInvoiceSchema, recordPaymentSchema } from "@/lib/validations"
import { logAuditEvent } from "@/lib/auth"

type RouteParams = { params: Promise<{ id: string }> }

// GET /api/invoices/[id]
export async function GET(request: NextRequest, { params }: RouteParams) {
  try {
    const { userId, orgId } = await auth()
    if (!userId) return apiError("Unauthorized", 401)
    const { id } = await params

    const org = orgId
      ? await prisma.organization.findUnique({ where: { clerkOrgId: orgId } })
      : await prisma.organization.findFirst({ where: { clerkOrgId: `personal_${userId}` } })
    if (!org) return apiError("Organization not found", 404)

    const invoice = await prisma.invoice.findFirst({
      where: { id, organizationId: org.id },
      include: {
        client: true,
        items: { orderBy: { sortOrder: "asc" } },
        payments: { orderBy: { paidAt: "desc" } },
        createdBy: { select: { firstName: true, lastName: true } },
      },
    })

    if (!invoice) return apiError("Invoice not found", 404)

    return apiSuccess(invoice)
  } catch (error) {
    return apiError("Failed to fetch invoice", 500)
  }
}

// PATCH /api/invoices/[id]
export async function PATCH(request: NextRequest, { params }: RouteParams) {
  try {
    const { userId, orgId } = await auth()
    if (!userId) return apiError("Unauthorized", 401)
    const { id } = await params

    const org = orgId
      ? await prisma.organization.findUnique({ where: { clerkOrgId: orgId } })
      : await prisma.organization.findFirst({ where: { clerkOrgId: `personal_${userId}` } })
    if (!org) return apiError("Organization not found", 404)

    const user = await prisma.user.findUnique({ where: { clerkId: userId } })
    if (!user) return apiError("User not found", 404)

    const existing = await prisma.invoice.findFirst({
      where: { id, organizationId: org.id },
    })
    if (!existing) return apiError("Invoice not found", 404)

    const body = await request.json()

    // Handle payment recording
    if (body._action === "record_payment") {
      const paymentData = recordPaymentSchema.parse(body)
      const newAmountPaid = Number(existing.amountPaid) + paymentData.amount
      const newAmountDue = Math.max(0, Number(existing.total) - newAmountPaid)
      const newStatus = newAmountDue === 0 ? "PAID" : newAmountPaid > 0 ? "PARTIAL" : existing.status

      const [payment, updatedInvoice] = await prisma.$transaction([
        prisma.payment.create({
          data: {
            invoiceId: id,
            amount: paymentData.amount,
            currency: paymentData.currency,
            method: paymentData.method,
            reference: paymentData.reference,
            notes: paymentData.notes,
            paidAt: new Date(paymentData.paidAt),
          },
        }),
        prisma.invoice.update({
          where: { id },
          data: {
            amountPaid: newAmountPaid,
            amountDue: newAmountDue,
            status: newStatus as "PAID" | "PARTIAL",
            paidAt: newStatus === "PAID" ? new Date(paymentData.paidAt) : existing.paidAt,
          },
        }),
      ])

      return apiSuccess({ payment, invoice: updatedInvoice })
    }

    // Handle status update
    if (body._action === "send") {
      const updated = await prisma.invoice.update({
        where: { id },
        data: { status: "SENT", sentAt: new Date() },
      })
      return apiSuccess(updated)
    }

    // Regular update
    const data = updateInvoiceSchema.parse(body)
    const updated = await prisma.invoice.update({
      where: { id },
      data: {
        ...data,
        ...(data.issueDate ? { issueDate: new Date(data.issueDate) } : {}),
        ...(data.dueDate ? { dueDate: new Date(data.dueDate) } : {}),
      },
      include: { items: true },
    })

    await logAuditEvent({
      organizationId: org.id,
      userId: user.id,
      action: "UPDATE",
      resource: "invoices",
      resourceId: id,
    })

    return apiSuccess(updated)
  } catch (error) {
    console.error("Invoice PATCH error:", error)
    return apiError("Failed to update invoice", 500)
  }
}

// DELETE /api/invoices/[id]
export async function DELETE(request: NextRequest, { params }: RouteParams) {
  try {
    const { userId, orgId } = await auth()
    if (!userId) return apiError("Unauthorized", 401)
    const { id } = await params

    const org = orgId
      ? await prisma.organization.findUnique({ where: { clerkOrgId: orgId } })
      : await prisma.organization.findFirst({ where: { clerkOrgId: `personal_${userId}` } })
    if (!org) return apiError("Organization not found", 404)

    const invoice = await prisma.invoice.findFirst({
      where: { id, organizationId: org.id },
    })
    if (!invoice) return apiError("Invoice not found", 404)

    // Can only delete drafts
    if (invoice.status !== "DRAFT") {
      return apiError("Only draft invoices can be deleted", 400)
    }

    await prisma.invoice.delete({ where: { id } })

    return apiSuccess({ deleted: true })
  } catch (error) {
    return apiError("Failed to delete invoice", 500)
  }
}
