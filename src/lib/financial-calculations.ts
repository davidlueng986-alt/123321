/**
 * FinSight AI - Deterministic Financial Calculations
 * 
 * CRITICAL: All financial calculations must be performed here.
 * AI should NEVER calculate financial values - only explain them.
 */

import { prisma } from "./prisma"
import { parseDecimal } from "./utils"

// ─── Dashboard Metrics ───────────────────────────────────────
export async function getDashboardMetrics(
  organizationId: string,
  dateRange?: { from: Date; to: Date }
) {
  const now = new Date()
  const currentPeriodEnd = dateRange?.to ?? now
  const currentPeriodStart = dateRange?.from ?? new Date(now.getFullYear(), now.getMonth(), 1)

  // Previous period (same duration, one period back)
  const periodDuration = currentPeriodEnd.getTime() - currentPeriodStart.getTime()
  const prevPeriodEnd = new Date(currentPeriodStart.getTime() - 1)
  const prevPeriodStart = new Date(prevPeriodEnd.getTime() - periodDuration)

  // Current period aggregates
  const [currentIncome, currentExpenses, prevIncome, prevExpenses] = await Promise.all([
    prisma.transaction.aggregate({
      where: {
        organizationId,
        type: "INCOME",
        date: { gte: currentPeriodStart, lte: currentPeriodEnd },
      },
      _sum: { amount: true },
    }),
    prisma.transaction.aggregate({
      where: {
        organizationId,
        type: "EXPENSE",
        date: { gte: currentPeriodStart, lte: currentPeriodEnd },
      },
      _sum: { amount: true },
    }),
    prisma.transaction.aggregate({
      where: {
        organizationId,
        type: "INCOME",
        date: { gte: prevPeriodStart, lte: prevPeriodEnd },
      },
      _sum: { amount: true },
    }),
    prisma.transaction.aggregate({
      where: {
        organizationId,
        type: "EXPENSE",
        date: { gte: prevPeriodStart, lte: prevPeriodEnd },
      },
      _sum: { amount: true },
    }),
  ])

  const revenue = parseDecimal(currentIncome._sum.amount)
  const expenses = parseDecimal(currentExpenses._sum.amount)
  const profit = revenue - expenses
  const prevRevenue = parseDecimal(prevIncome._sum.amount)
  const prevExpensesAmt = parseDecimal(prevExpenses._sum.amount)
  const prevProfit = prevRevenue - prevExpensesAmt

  // Invoice metrics
  const [pendingInvoices, overdueInvoices, paidThisPeriod] = await Promise.all([
    prisma.invoice.aggregate({
      where: {
        organizationId,
        status: { in: ["SENT", "PARTIAL", "VIEWED"] },
      },
      _sum: { amountDue: true },
      _count: true,
    }),
    prisma.invoice.aggregate({
      where: {
        organizationId,
        status: "OVERDUE",
      },
      _sum: { amountDue: true },
      _count: true,
    }),
    prisma.payment.aggregate({
      where: {
        invoice: { organizationId },
        paidAt: { gte: currentPeriodStart, lte: currentPeriodEnd },
      },
      _sum: { amount: true },
    }),
  ])

  return {
    revenue,
    expenses,
    profit,
    profitMargin: revenue > 0 ? (profit / revenue) * 100 : 0,
    revenueChange: calculatePercentageChange(revenue, prevRevenue),
    expensesChange: calculatePercentageChange(expenses, prevExpensesAmt),
    profitChange: calculatePercentageChange(profit, prevProfit),
    outstandingInvoices: parseDecimal(pendingInvoices._sum.amountDue),
    overdueAmount: parseDecimal(overdueInvoices._sum.amountDue),
    overdueCount: overdueInvoices._count,
    pendingCount: pendingInvoices._count,
    collectedThisPeriod: parseDecimal(paidThisPeriod._sum.amount),
  }
}

// ─── Monthly Revenue & Expense Trends ────────────────────────
export async function getMonthlyTrends(
  organizationId: string,
  months = 12
) {
  const endDate = new Date()
  const startDate = new Date()
  startDate.setMonth(startDate.getMonth() - months + 1)
  startDate.setDate(1)
  startDate.setHours(0, 0, 0, 0)

  const transactions = await prisma.transaction.findMany({
    where: {
      organizationId,
      date: { gte: startDate, lte: endDate },
      type: { in: ["INCOME", "EXPENSE"] },
    },
    select: { type: true, amount: true, date: true },
    orderBy: { date: "asc" },
  })

  // Group by month deterministically
  const monthlyData: Record<string, { month: string; revenue: number; expenses: number; profit: number }> = {}

  for (const tx of transactions) {
    const d = new Date(tx.date)
    const key = `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}`
    const label = d.toLocaleDateString("en-US", { month: "short", year: "numeric" })

    if (!monthlyData[key]) {
      monthlyData[key] = { month: label, revenue: 0, expenses: 0, profit: 0 }
    }

    const amount = parseDecimal(tx.amount)
    if (tx.type === "INCOME") {
      monthlyData[key].revenue += amount
    } else {
      monthlyData[key].expenses += amount
    }
    monthlyData[key].profit = monthlyData[key].revenue - monthlyData[key].expenses
  }

  return Object.entries(monthlyData)
    .sort(([a], [b]) => a.localeCompare(b))
    .map(([, v]) => v)
}

// ─── Expense By Category ─────────────────────────────────────
export async function getExpensesByCategory(
  organizationId: string,
  dateRange?: { from: Date; to: Date }
) {
  const where: Record<string, unknown> = {
    organizationId,
    type: "EXPENSE",
  }

  if (dateRange) {
    where.date = { gte: dateRange.from, lte: dateRange.to }
  }

  const categories = await prisma.transaction.groupBy({
    by: ["categoryId"],
    where,
    _sum: { amount: true },
    _count: true,
    orderBy: { _sum: { amount: "desc" } },
  })

  const categoryIds = categories
    .filter((c) => c.categoryId)
    .map((c) => c.categoryId!)

  const categoryDetails = await prisma.category.findMany({
    where: { id: { in: categoryIds } },
    select: { id: true, name: true, color: true },
  })

  const total = categories.reduce(
    (sum, c) => sum + parseDecimal(c._sum.amount),
    0
  )

  return categories.map((c) => {
    const detail = categoryDetails.find((d) => d.id === c.categoryId)
    const amount = parseDecimal(c._sum.amount)
    return {
      categoryId: c.categoryId,
      name: detail?.name ?? "Uncategorized",
      color: detail?.color ?? "#6b7280",
      amount,
      count: c._count,
      percentage: total > 0 ? (amount / total) * 100 : 0,
    }
  })
}

// ─── Cash Flow Analysis ──────────────────────────────────────
export async function getCashFlowData(
  organizationId: string,
  months = 6
) {
  const trends = await getMonthlyTrends(organizationId, months)

  // Calculate running balance
  let runningBalance = 0
  return trends.map((t) => {
    runningBalance += t.profit
    return {
      ...t,
      balance: runningBalance,
    }
  })
}

// ─── Cash Flow Forecast (Deterministic Algorithm) ────────────
export async function generateCashFlowForecast(
  organizationId: string,
  forecastMonths = 3
) {
  // Use last 6 months for trend analysis
  const historicalData = await getMonthlyTrends(organizationId, 6)

  if (historicalData.length === 0) {
    return []
  }

  // Calculate averages and trends
  const avgRevenue = historicalData.reduce((s, d) => s + d.revenue, 0) / historicalData.length
  const avgExpenses = historicalData.reduce((s, d) => s + d.expenses, 0) / historicalData.length

  // Linear trend calculation
  const revenueGrowth = historicalData.length > 1
    ? (historicalData[historicalData.length - 1].revenue - historicalData[0].revenue) / historicalData.length
    : 0
  const expenseGrowth = historicalData.length > 1
    ? (historicalData[historicalData.length - 1].expenses - historicalData[0].expenses) / historicalData.length
    : 0

  const lastRevenue = historicalData[historicalData.length - 1]?.revenue ?? avgRevenue
  const lastExpenses = historicalData[historicalData.length - 1]?.expenses ?? avgExpenses

  const forecasts = []
  const now = new Date()

  for (let i = 1; i <= forecastMonths; i++) {
    const forecastDate = new Date(now.getFullYear(), now.getMonth() + i, 1)
    const expectedIncome = Math.max(0, lastRevenue + revenueGrowth * i)
    const expectedExpenses = Math.max(0, lastExpenses + expenseGrowth * i)
    const expectedBalance = expectedIncome - expectedExpenses

    // Confidence decreases with time
    const confidence = Math.max(40, 85 - (i - 1) * 15)

    forecasts.push({
      month: forecastDate.toLocaleDateString("en-US", { month: "short", year: "numeric" }),
      forecastDate,
      expectedIncome: Math.round(expectedIncome * 100) / 100,
      expectedExpenses: Math.round(expectedExpenses * 100) / 100,
      expectedBalance: Math.round(expectedBalance * 100) / 100,
      confidence,
      methodology: "linear_trend",
    })
  }

  return forecasts
}

// ─── Profit & Loss Report ────────────────────────────────────
export async function getProfitLossReport(
  organizationId: string,
  from: Date,
  to: Date
) {
  const [incomeByCategory, expenseByCategory] = await Promise.all([
    prisma.transaction.groupBy({
      by: ["categoryId"],
      where: {
        organizationId,
        type: "INCOME",
        date: { gte: from, lte: to },
      },
      _sum: { amount: true },
    }),
    prisma.transaction.groupBy({
      by: ["categoryId"],
      where: {
        organizationId,
        type: "EXPENSE",
        date: { gte: from, lte: to },
      },
      _sum: { amount: true },
    }),
  ])

  const totalIncome = incomeByCategory.reduce((s, c) => s + parseDecimal(c._sum.amount), 0)
  const totalExpenses = expenseByCategory.reduce((s, c) => s + parseDecimal(c._sum.amount), 0)
  const netProfit = totalIncome - totalExpenses
  const profitMargin = totalIncome > 0 ? (netProfit / totalIncome) * 100 : 0

  return {
    period: { from, to },
    totalIncome,
    totalExpenses,
    netProfit,
    profitMargin,
    incomeByCategory,
    expenseByCategory,
    generatedAt: new Date(),
  }
}

// ─── Invoice Statistics ──────────────────────────────────────
export async function getInvoiceStatistics(organizationId: string) {
  const stats = await prisma.invoice.groupBy({
    by: ["status"],
    where: { organizationId },
    _sum: { total: true, amountDue: true },
    _count: true,
  })

  const result: Record<string, { count: number; total: number; amountDue: number }> = {}
  for (const s of stats) {
    result[s.status] = {
      count: s._count,
      total: parseDecimal(s._sum.total),
      amountDue: parseDecimal(s._sum.amountDue),
    }
  }

  return result
}

// ─── Top Clients by Revenue ──────────────────────────────────
export async function getTopClients(organizationId: string, limit = 5) {
  const clients = await prisma.client.findMany({
    where: { organizationId, isActive: true },
    select: {
      id: true,
      name: true,
      company: true,
      totalRevenue: true,
      invoices: {
        select: { total: true, status: true },
      },
    },
    orderBy: { totalRevenue: "desc" },
    take: limit,
  })

  const totalRevenue = clients.reduce(
    (sum, c) => sum + parseDecimal(c.totalRevenue),
    0
  )

  return clients.map((c) => ({
    id: c.id,
    name: c.name,
    company: c.company,
    revenue: parseDecimal(c.totalRevenue),
    percentage: totalRevenue > 0 ? (parseDecimal(c.totalRevenue) / totalRevenue) * 100 : 0,
    invoiceCount: c.invoices.length,
    paidInvoices: c.invoices.filter((i) => i.status === "PAID").length,
  }))
}

// ─── Anomaly Detection ───────────────────────────────────────
export async function detectAnomalies(
  organizationId: string,
  days = 30
) {
  const endDate = new Date()
  const startDate = new Date()
  startDate.setDate(startDate.getDate() - days)

  const transactions = await prisma.transaction.findMany({
    where: {
      organizationId,
      date: { gte: startDate, lte: endDate },
    },
    include: { category: true },
    orderBy: { date: "desc" },
  })

  // Calculate baseline statistics per category
  const categoryStats: Record<string, number[]> = {}
  for (const tx of transactions) {
    const key = tx.categoryId ?? "uncategorized"
    if (!categoryStats[key]) categoryStats[key] = []
    categoryStats[key].push(parseDecimal(tx.amount))
  }

  const anomalies: Array<{
    transactionId: string
    type: string
    description: string
    severity: string
    amount: number
    expectedMax: number
  }> = []

  for (const tx of transactions) {
    const key = tx.categoryId ?? "uncategorized"
    const amounts = categoryStats[key]
    if (amounts.length < 3) continue

    const avg = amounts.reduce((a, b) => a + b, 0) / amounts.length
    const stdDev = Math.sqrt(
      amounts.reduce((sq, n) => sq + Math.pow(n - avg, 2), 0) / amounts.length
    )
    const amount = parseDecimal(tx.amount)
    const zScore = stdDev > 0 ? Math.abs(amount - avg) / stdDev : 0

    if (zScore > 3) {
      anomalies.push({
        transactionId: tx.id,
        type: "UNUSUAL_AMOUNT",
        description: `Transaction amount (${amount}) is ${zScore.toFixed(1)}x above normal for ${tx.category?.name ?? "this category"}`,
        severity: zScore > 5 ? "high" : "medium",
        amount,
        expectedMax: avg + 2 * stdDev,
      })
    }
  }

  return anomalies
}

// ─── Helper: Percentage Change ───────────────────────────────
function calculatePercentageChange(current: number, previous: number): number {
  if (previous === 0) return current > 0 ? 100 : 0
  return ((current - previous) / Math.abs(previous)) * 100
}

// ─── Financial Insights (Data Only, AI Explains) ─────────────
export async function getFinancialInsightsData(organizationId: string) {
  const [trends, categories, invoiceStats, topClients] = await Promise.all([
    getMonthlyTrends(organizationId, 3),
    getExpensesByCategory(organizationId),
    getInvoiceStatistics(organizationId),
    getTopClients(organizationId, 3),
  ])

  const insights: Array<{
    type: string
    metric: string
    value: number
    comparison?: number
    severity: "info" | "warning" | "critical"
  }> = []

  // Expense spike detection
  if (trends.length >= 2) {
    const latest = trends[trends.length - 1]
    const previous = trends[trends.length - 2]
    const expenseChange = previous.expenses > 0
      ? ((latest.expenses - previous.expenses) / previous.expenses) * 100
      : 0

    if (expenseChange > 20) {
      insights.push({
        type: "expense_spike",
        metric: "Monthly expenses increased",
        value: expenseChange,
        comparison: previous.expenses,
        severity: expenseChange > 50 ? "critical" : "warning",
      })
    }

    // Revenue concentration
    if (topClients.length > 0 && topClients[0].percentage > 40) {
      insights.push({
        type: "revenue_concentration",
        metric: "Top client revenue share",
        value: topClients[0].percentage,
        severity: topClients[0].percentage > 60 ? "critical" : "warning",
      })
    }

    // Cash flow warning
    const avgProfit = trends.reduce((s, t) => s + t.profit, 0) / trends.length
    if (avgProfit < 0) {
      insights.push({
        type: "cash_warning",
        metric: "Average monthly loss",
        value: Math.abs(avgProfit),
        severity: "critical",
      })
    }
  }

  // Overdue invoices
  const overdue = invoiceStats["OVERDUE"]
  if (overdue && overdue.amountDue > 0) {
    insights.push({
      type: "overdue_invoices",
      metric: "Outstanding overdue amount",
      value: overdue.amountDue,
      comparison: overdue.count,
      severity: overdue.amountDue > 10000 ? "critical" : "warning",
    })
  }

  return { insights, trends, categories, invoiceStats, topClients }
}
