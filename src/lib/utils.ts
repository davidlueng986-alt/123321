import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

// ─── Currency Formatting ─────────────────────────────────────
export function formatCurrency(
  amount: number | string,
  currency = "USD",
  locale = "en-US"
): string {
  const num = typeof amount === "string" ? parseFloat(amount) : amount
  if (isNaN(num)) return "$0.00"
  return new Intl.NumberFormat(locale, {
    style: "currency",
    currency,
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(num)
}

// ─── Percentage Formatting ───────────────────────────────────
export function formatPercentage(value: number, decimals = 1): string {
  return `${value >= 0 ? "+" : ""}${value.toFixed(decimals)}%`
}

// ─── Number Formatting ───────────────────────────────────────
export function formatNumber(num: number, locale = "en-US"): string {
  return new Intl.NumberFormat(locale).format(num)
}

// ─── Compact Number Formatting ───────────────────────────────
export function formatCompactNumber(num: number): string {
  if (Math.abs(num) >= 1_000_000) {
    return `$${(num / 1_000_000).toFixed(1)}M`
  }
  if (Math.abs(num) >= 1_000) {
    return `$${(num / 1_000).toFixed(1)}K`
  }
  return formatCurrency(num)
}

// ─── Date Formatting ─────────────────────────────────────────
export function formatDate(
  date: Date | string | null,
  format: "short" | "medium" | "long" = "medium"
): string {
  if (!date) return "—"
  const d = typeof date === "string" ? new Date(date) : date
  if (isNaN(d.getTime())) return "—"

  switch (format) {
    case "short":
      return d.toLocaleDateString("en-US", { month: "short", day: "numeric" })
    case "long":
      return d.toLocaleDateString("en-US", {
        year: "numeric",
        month: "long",
        day: "numeric",
      })
    default:
      return d.toLocaleDateString("en-US", {
        year: "numeric",
        month: "short",
        day: "numeric",
      })
  }
}

export function formatRelativeDate(date: Date | string): string {
  const d = typeof date === "string" ? new Date(date) : date
  const now = new Date()
  const diffMs = now.getTime() - d.getTime()
  const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24))

  if (diffDays === 0) return "Today"
  if (diffDays === 1) return "Yesterday"
  if (diffDays < 7) return `${diffDays} days ago`
  if (diffDays < 30) return `${Math.floor(diffDays / 7)} weeks ago`
  if (diffDays < 365) return `${Math.floor(diffDays / 30)} months ago`
  return `${Math.floor(diffDays / 365)} years ago`
}

// ─── Days Until Date ─────────────────────────────────────────
export function daysUntil(date: Date | string): number {
  const d = typeof date === "string" ? new Date(date) : date
  const now = new Date()
  const diffMs = d.getTime() - now.getTime()
  return Math.ceil(diffMs / (1000 * 60 * 60 * 24))
}

// ─── Calculate Percentage Change ─────────────────────────────
export function percentageChange(current: number, previous: number): number {
  if (previous === 0) return current > 0 ? 100 : 0
  return ((current - previous) / Math.abs(previous)) * 100
}

// ─── Sanitize Input ──────────────────────────────────────────
export function sanitizeInput(input: string): string {
  return input
    .replace(/[<>]/g, "") // Remove HTML tags
    .replace(/javascript:/gi, "") // Remove JS protocol
    .trim()
}

// ─── Generate Invoice Number ─────────────────────────────────
export function generateInvoiceNumber(prefix = "INV"): string {
  const date = new Date()
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, "0")
  const random = Math.floor(Math.random() * 9000) + 1000
  return `${prefix}-${year}${month}-${random}`
}

// ─── Truncate Text ───────────────────────────────────────────
export function truncate(text: string, maxLength: number): string {
  if (text.length <= maxLength) return text
  return `${text.slice(0, maxLength)}...`
}

// ─── Status Color Mapping ────────────────────────────────────
export function getStatusColor(status: string): string {
  const map: Record<string, string> = {
    PAID: "text-emerald-600 bg-emerald-50 border-emerald-200",
    SENT: "text-blue-600 bg-blue-50 border-blue-200",
    DRAFT: "text-gray-600 bg-gray-50 border-gray-200",
    OVERDUE: "text-red-600 bg-red-50 border-red-200",
    PARTIAL: "text-amber-600 bg-amber-50 border-amber-200",
    CANCELLED: "text-gray-400 bg-gray-50 border-gray-200",
    APPROVED: "text-emerald-600 bg-emerald-50 border-emerald-200",
    PENDING: "text-amber-600 bg-amber-50 border-amber-200",
    REJECTED: "text-red-600 bg-red-50 border-red-200",
    INCOME: "text-emerald-600 bg-emerald-50 border-emerald-200",
    EXPENSE: "text-red-600 bg-red-50 border-red-200",
  }
  return map[status] ?? "text-gray-600 bg-gray-50 border-gray-200"
}

// ─── Parse Decimal ───────────────────────────────────────────
export function parseDecimal(value: unknown): number {
  if (typeof value === "number") return value
  if (typeof value === "string") return parseFloat(value) || 0
  if (value && typeof value === "object" && "toString" in value) {
    return parseFloat(value.toString()) || 0
  }
  return 0
}

// ─── Chunk Array ─────────────────────────────────────────────
export function chunkArray<T>(array: T[], size: number): T[][] {
  const chunks: T[][] = []
  for (let i = 0; i < array.length; i += size) {
    chunks.push(array.slice(i, i + size))
  }
  return chunks
}

// ─── Generate Color from String ─────────────────────────────
export function stringToColor(str: string): string {
  let hash = 0
  for (let i = 0; i < str.length; i++) {
    hash = str.charCodeAt(i) + ((hash << 5) - hash)
  }
  const colors = [
    "#3b82f6", "#8b5cf6", "#06b6d4", "#10b981",
    "#f59e0b", "#ef4444", "#ec4899", "#84cc16",
    "#f97316", "#6366f1"
  ]
  return colors[Math.abs(hash) % colors.length]
}

// ─── Sleep ───────────────────────────────────────────────────
export function sleep(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms))
}

// ─── Is Valid Date ───────────────────────────────────────────
export function isValidDate(date: unknown): boolean {
  if (!date) return false
  const d = new Date(date as string)
  return !isNaN(d.getTime())
}
