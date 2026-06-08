"use client"

import { useState } from "react"
import { useQuery, useMutation } from "@tanstack/react-query"
import axios from "axios"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Badge } from "@/components/ui/badge"
import { formatDate, formatCurrency } from "@/lib/utils"
import { FileBarChart, Plus, Download, TrendingUp, Receipt, DollarSign, BarChart3 } from "lucide-react"
import { toast } from "sonner"

const REPORT_TYPES = [
  { value: "PROFIT_LOSS", label: "Profit & Loss", icon: TrendingUp, description: "Revenue, expenses, and net profit" },
  { value: "EXPENSE_SUMMARY", label: "Expense Summary", icon: Receipt, description: "Breakdown by category" },
  { value: "REVENUE_TRENDS", label: "Revenue Trends", icon: BarChart3, description: "Monthly revenue analysis" },
  { value: "CASH_FLOW", label: "Cash Flow", icon: DollarSign, description: "Income vs expense flow" },
]

export default function ReportsPage() {
  const [reportType, setReportType] = useState("PROFIT_LOSS")
  const [from, setFrom] = useState(() => {
    const d = new Date()
    d.setMonth(d.getMonth() - 3)
    return d.toISOString().split("T")[0]
  })
  const [to, setTo] = useState(new Date().toISOString().split("T")[0])
  const [latestReport, setLatestReport] = useState<Record<string, unknown> | null>(null)

  const { data: reports, isLoading } = useQuery({
    queryKey: ["reports"],
    queryFn: async () => {
      const res = await axios.get("/api/reports")
      return res.data.data
    },
  })

  const generateMutation = useMutation({
    mutationFn: async (data: Record<string, unknown>) => {
      const res = await axios.post("/api/reports", data)
      return res.data
    },
    onSuccess: (data) => {
      setLatestReport(data.data)
      toast.success("Report generated successfully")
    },
    onError: () => toast.error("Failed to generate report"),
  })

  const handleGenerate = () => {
    const selectedType = REPORT_TYPES.find((t) => t.value === reportType)
    generateMutation.mutate({
      type: reportType,
      name: `${selectedType?.label} - ${from} to ${to}`,
      from: `${from}T00:00:00.000Z`,
      to: `${to}T23:59:59.999Z`,
    })
  }

  const reportData = latestReport?.data as Record<string, unknown> | undefined

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold">Financial Reports</h1>
        <p className="text-muted-foreground">Generate and export financial reports</p>
      </div>

      {/* Report Generator */}
      <Card>
        <CardHeader>
          <CardTitle>Generate Report</CardTitle>
          <CardDescription>All calculations are deterministic — based on your actual data</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="space-y-1.5">
              <Label>Report Type</Label>
              <Select value={reportType} onValueChange={setReportType}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  {REPORT_TYPES.map((t) => (
                    <SelectItem key={t.value} value={t.value}>{t.label}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            <div className="space-y-1.5">
              <Label>From Date</Label>
              <Input type="date" value={from} onChange={(e) => setFrom(e.target.value)} />
            </div>
            <div className="space-y-1.5">
              <Label>To Date</Label>
              <Input type="date" value={to} onChange={(e) => setTo(e.target.value)} />
            </div>
          </div>

          {/* Report Type Cards */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
            {REPORT_TYPES.map((t) => (
              <button
                key={t.value}
                onClick={() => setReportType(t.value)}
                className={`p-3 rounded-lg border text-left transition-all ${
                  reportType === t.value
                    ? "border-primary bg-primary/5 ring-1 ring-primary"
                    : "hover:border-primary/50 hover:bg-accent"
                }`}
              >
                <t.icon className={`h-5 w-5 mb-1.5 ${reportType === t.value ? "text-primary" : "text-muted-foreground"}`} />
                <p className="text-xs font-semibold">{t.label}</p>
                <p className="text-[10px] text-muted-foreground mt-0.5">{t.description}</p>
              </button>
            ))}
          </div>

          <Button
            onClick={handleGenerate}
            loading={generateMutation.isPending}
            className="w-full"
          >
            <FileBarChart className="h-4 w-4 mr-1.5" />
            Generate Report
          </Button>
        </CardContent>
      </Card>

      {/* Latest Report Results */}
      {reportData && (
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <div>
                <CardTitle>Report Results</CardTitle>
                <CardDescription>{REPORT_TYPES.find(t => t.value === reportType)?.label}</CardDescription>
              </div>
              <Button variant="outline" size="sm">
                <Download className="h-4 w-4 mr-1.5" />
                Export PDF
              </Button>
            </div>
          </CardHeader>
          <CardContent>
            {reportType === "PROFIT_LOSS" && (
              <div className="space-y-4">
                <div className="grid grid-cols-3 gap-4">
                  {[
                    { label: "Total Revenue", value: reportData.totalIncome as number, color: "text-emerald-600" },
                    { label: "Total Expenses", value: reportData.totalExpenses as number, color: "text-red-600" },
                    { label: "Net Profit", value: reportData.netProfit as number, color: (reportData.netProfit as number) >= 0 ? "text-emerald-600" : "text-red-600" },
                  ].map((item) => (
                    <div key={item.label} className="border rounded-lg p-4 text-center">
                      <p className="text-sm text-muted-foreground">{item.label}</p>
                      <p className={`text-xl font-bold mt-1 ${item.color}`}>
                        {formatCurrency(item.value ?? 0)}
                      </p>
                    </div>
                  ))}
                </div>
                <div className="border rounded-lg p-4">
                  <p className="text-sm font-medium mb-2">Profit Margin</p>
                  <div className="flex items-center gap-3">
                    <div className="flex-1 h-3 bg-muted rounded-full overflow-hidden">
                      <div
                        className="h-full bg-primary rounded-full"
                        style={{ width: `${Math.max(0, Math.min(100, reportData.profitMargin as number))}%` }}
                      />
                    </div>
                    <span className="font-bold text-sm">{(reportData.profitMargin as number ?? 0).toFixed(1)}%</span>
                  </div>
                </div>
              </div>
            )}

            {reportType === "REVENUE_TRENDS" && Array.isArray(reportData.trends) && (
              <div className="space-y-2">
                {(reportData.trends as Array<{ month: string; revenue: number; expenses: number; profit: number }>).map((t) => (
                  <div key={t.month} className="flex items-center justify-between border-b pb-2">
                    <span className="text-sm font-medium">{t.month}</span>
                    <div className="flex gap-4 text-sm">
                      <span className="text-emerald-600">+{formatCurrency(t.revenue)}</span>
                      <span className="text-red-600">-{formatCurrency(t.expenses)}</span>
                      <span className={`font-bold ${t.profit >= 0 ? "text-emerald-600" : "text-red-600"}`}>
                        {formatCurrency(t.profit)}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            )}

            {reportType === "EXPENSE_SUMMARY" && Array.isArray(reportData.categories) && (
              <div className="space-y-2">
                {(reportData.categories as Array<{ name: string; amount: number; percentage: number; color: string }>).map((c) => (
                  <div key={c.name} className="flex items-center gap-3">
                    <div className="w-3 h-3 rounded-full shrink-0" style={{ backgroundColor: c.color }} />
                    <div className="flex-1">
                      <div className="flex justify-between text-sm">
                        <span>{c.name}</span>
                        <span className="font-medium">{formatCurrency(c.amount)} ({c.percentage.toFixed(1)}%)</span>
                      </div>
                      <div className="h-1.5 bg-muted rounded mt-1">
                        <div className="h-full rounded" style={{ width: `${c.percentage}%`, backgroundColor: c.color }} />
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      )}

      {/* Report History */}
      {reports && reports.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>Report History</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              {reports.slice(0, 10).map((r: {
                id: string
                name: string
                type: string
                generatedAt: string
              }) => (
                <div key={r.id} className="flex items-center justify-between border rounded-lg p-3">
                  <div className="flex items-center gap-3">
                    <FileBarChart className="h-4 w-4 text-primary" />
                    <div>
                      <p className="text-sm font-medium">{r.name}</p>
                      <p className="text-xs text-muted-foreground">{formatDate(r.generatedAt)}</p>
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    <Badge variant="secondary" className="text-xs">{r.type.replace("_", " ")}</Badge>
                    <Button variant="ghost" size="icon" className="h-7 w-7">
                      <Download className="h-3.5 w-3.5" />
                    </Button>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  )
}
