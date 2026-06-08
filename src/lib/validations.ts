import { z } from "zod"

// ─── Common Schemas ──────────────────────────────────────────
export const paginationSchema = z.object({
  page: z.coerce.number().int().min(1).default(1),
  limit: z.coerce.number().int().min(1).max(100).default(20),
  sortBy: z.string().optional(),
  sortOrder: z.enum(["asc", "desc"]).default("desc"),
})

export const dateRangeSchema = z.object({
  from: z.string().datetime().optional(),
  to: z.string().datetime().optional(),
})

// ─── Invoice Schemas ─────────────────────────────────────────
export const invoiceItemSchema = z.object({
  description: z.string().min(1).max(500),
  quantity: z.number().positive().max(99999),
  unitPrice: z.number().min(0).max(9999999),
  taxRate: z.number().min(0).max(100).default(0),
})

export const createInvoiceSchema = z.object({
  clientId: z.string().cuid().optional(),
  invoiceNumber: z.string().min(1).max(50),
  issueDate: z.string(),
  dueDate: z.string(),
  taxRate: z.number().min(0).max(100).default(0),
  discountAmount: z.number().min(0).default(0),
  currency: z.string().length(3).default("USD"),
  notes: z.string().max(2000).optional(),
  terms: z.string().max(2000).optional(),
  items: z.array(invoiceItemSchema).min(1).max(100),
})

export const updateInvoiceSchema = createInvoiceSchema.partial()

// ─── Expense Schemas ─────────────────────────────────────────
export const createExpenseSchema = z.object({
  categoryId: z.string().cuid().optional(),
  vendorId: z.string().cuid().optional(),
  amount: z.number().positive().max(9999999),
  currency: z.string().length(3).default("USD"),
  description: z.string().min(1).max(500),
  date: z.string(),
  notes: z.string().max(2000).optional(),
  tags: z.array(z.string()).max(10).optional(),
  isReimbursable: z.boolean().default(false),
})

export const updateExpenseSchema = createExpenseSchema.partial()

// ─── Transaction Schemas ─────────────────────────────────────
export const createTransactionSchema = z.object({
  type: z.enum(["INCOME", "EXPENSE", "TRANSFER"]),
  amount: z.number().positive(),
  currency: z.string().length(3).default("USD"),
  description: z.string().min(1).max(500),
  reference: z.string().max(100).optional(),
  date: z.string(),
  categoryId: z.string().cuid().optional(),
  tags: z.array(z.string()).max(10).optional(),
})

// ─── Category Schemas ────────────────────────────────────────
export const createCategorySchema = z.object({
  name: z.string().min(1).max(100),
  type: z.enum(["INCOME", "EXPENSE", "BOTH"]),
  color: z.string().regex(/^#[0-9A-Fa-f]{6}$/).optional(),
  icon: z.string().max(50).optional(),
  description: z.string().max(500).optional(),
  parentId: z.string().cuid().optional(),
})

// ─── AI Chat Schemas ─────────────────────────────────────────
export const chatMessageSchema = z.object({
  chatId: z.string().cuid().optional(),
  message: z.string().min(1).max(4000),
  context: z.object({
    dateRange: dateRangeSchema.optional(),
    module: z.string().optional(),
  }).optional(),
})

// ─── Report Schemas ──────────────────────────────────────────
export const generateReportSchema = z.object({
  type: z.enum(["PROFIT_LOSS", "CASH_FLOW", "EXPENSE_SUMMARY", "REVENUE_TRENDS", "BALANCE_SHEET"]),
  name: z.string().min(1).max(200),
  from: z.string(),
  to: z.string(),
  format: z.enum(["PDF", "EXCEL", "CSV"]).optional(),
})

// ─── Client Schemas ──────────────────────────────────────────
export const createClientSchema = z.object({
  name: z.string().min(1).max(200),
  email: z.string().email().optional().or(z.literal("")),
  phone: z.string().max(20).optional(),
  company: z.string().max(200).optional(),
  address: z.object({
    street: z.string().optional(),
    city: z.string().optional(),
    state: z.string().optional(),
    zip: z.string().optional(),
    country: z.string().optional(),
  }).optional(),
  taxId: z.string().max(50).optional(),
  notes: z.string().max(1000).optional(),
})

// ─── Payment Schema ──────────────────────────────────────────
export const recordPaymentSchema = z.object({
  amount: z.number().positive(),
  currency: z.string().length(3).default("USD"),
  method: z.enum(["bank_transfer", "card", "cash", "check", "other"]),
  reference: z.string().max(100).optional(),
  notes: z.string().max(500).optional(),
  paidAt: z.string(),
})

// ─── Organization Schema ─────────────────────────────────────
export const updateOrganizationSchema = z.object({
  name: z.string().min(1).max(200).optional(),
  description: z.string().max(1000).optional(),
  industry: z.string().max(100).optional(),
  currency: z.string().length(3).optional(),
  fiscalYearStart: z.number().int().min(1).max(12).optional(),
  timezone: z.string().optional(),
  website: z.string().url().optional().or(z.literal("")),
  taxId: z.string().max(50).optional(),
})
