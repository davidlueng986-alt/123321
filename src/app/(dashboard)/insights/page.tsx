"use client"

import { useQuery } from "@tanstack/react-query"
import axios from "axios"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { formatCurrency } from "@/lib/utils"
import {
  TrendingUp, TrendingDown, AlertTriangle, AlertCircle,
  CheckCircle, Users, RefreshCw, Lightbulb, Bot
} from "lucide-react"
import { Button } from "@/components/ui/button"

const SEVERITY_CONFIG = {
  info: { color: "bg-blue-50 border-blue-200 text-blue-800", icon: CheckCircle, badge: "bg-blue-100 text-blue-700" },
  warning: { color: "bg-amber-50 border-amber-200 text-amber-800", icon: AlertTriangle, badge: "bg-amber-100 text-amber-700" },
  critical: { color: "bg-red-50 border-red-200 text-red-800", icon: AlertCircle, badge: "bg-red-100 text-red-700" },
}

const TYPE_ICONS: Record<string, React.ElementType> = {
  expense_spike: TrendingUp,
  revenue_concentration: Users,
  cash_warning: TrendingDown,
  overdue_invoices: AlertTriangle,
}

export default function InsightsPage() {
  const { data, isLoading, refetch, isFetching } = useQuery({
    queryKey: ["insights"],
    queryFn: async () => {
      const res = await axios.get("/api/insights")
      return res.data.data
    },
    staleTime: 5 * 60 * 1000, // 5 minutes
  })

  const insights = data?.insights ?? []
  const topClients = data?.topClients ?? []
  const trends = data?.trends ?? []

  const latestTrend = trends[trends.length - 1]
  const prevTrend = trends[trends.length - 2]
  const expenseChange = prevTrend && prevTrend.expenses > 0
    ? ((latestTrend?.expenses - prevTrend.expenses) / prevTrend.expenses) * 100
    : 0

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">AI Insights</h1>
          <p className="text-muted-foreground">
            AI-generated analysis based on your actual financial data
          </p>
        </div>
        <Button variant="outline" onClick={() => refetch()} disabled={isFetching}>
          <RefreshCw className={`h-4 w-4 mr-1.5 ${isFetching ? "animate-spin" : ""}`} />
          Refresh Insights
        </Button>
      </div>

      {/* AI Notice */}
      <Card className="border-blue-200 bg-blue-50/50">
        <CardContent className="p-4">
          <div className="flex items-start gap-3">
            <Bot className="h-5 w-5 text-blue-600 mt-0.5 shrink-0" />
            <div>
              <p className="text-sm font-medium text-blue-800">About These Insights</p>
              <p className="text-xs text-blue-700 mt-0.5">
                All financial metrics are calculated deterministically from your database.
                AI is used only to generate explanations and narratives — never to calculate numbers.
                Every insight references real data from your books.
              </p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* AI Insights */}
      <div className="space-y-3">
        <h2 className="text-lg font-semibold flex items-center gap-2">
          <Lightbulb className="h-5 w-5 text-amber-500" />
          Financial Insights
        </h2>

        {isLoading ? (
          <div className="space-y-3">
            {[1, 2, 3].map((i) => (
              <div key={i} className="skeleton h-28 rounded-xl" />
            ))}
          </div>
        ) : insights.length === 0 ? (
          <Card>
            <CardContent className="py-12 text-center">
              <CheckCircle className="h-12 w-12 text-emerald-500 mx-auto mb-3" />
              <p className="font-medium">No critical insights at this time</p>
              <p className="text-sm text-muted-foreground mt-1">
                Your finances look healthy! Check back as more data is added.
              </p>
            </CardContent>
          </Card>
        ) : (
          insights.map((insight: {
            type: string
            metric: string
            value: number
            severity: "info" | "warning" | "critical"
            aiNarrative?: string
          }, i: number) => {
            const config = SEVERITY_CONFIG[insight.severity] ?? SEVERITY_CONFIG.info
            const TypeIcon = TYPE_ICONS[insight.type] ?? Lightbulb

            return (
              <Card key={i} className={`border ${config.color}`}>
                <CardContent className="p-4">
                  <div className="flex items-start gap-3">
                    <TypeIcon className="h-5 w-5 shrink-0 mt-0.5" />
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-1">
                        <p className="font-semibold text-sm">{insight.metric}</p>
                        <Badge className={`text-[10px] ${config.badge}`}>
                          {insight.severity.toUpperCase()}
                        </Badge>
                      </div>
                      <p className="text-sm mb-2 font-medium">
                        Value: {insight.type === "revenue_concentration" || insight.type === "expense_spike"
                          ? `${insight.value.toFixed(1)}%`
                          : formatCurrency(insight.value)}
                      </p>
                      {insight.aiNarrative && (
                        <p className="text-xs leading-relaxed opacity-80">
                          <Bot className="h-3 w-3 inline mr-1" />
                          {insight.aiNarrative}
                        </p>
                      )}
                    </div>
                  </div>
                </CardContent>
              </Card>
            )
          })
        )}
      </div>

      {/* Top Clients Analysis */}
      {topClients.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>Revenue Concentration Analysis</CardTitle>
            <CardDescription>
              Top clients by revenue contribution — calculated from actual transactions
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {topClients.map((client: {
                id: string
                name: string
                revenue: number
                percentage: number
                invoiceCount: number
              }) => (
                <div key={client.id} className="flex items-center gap-4">
                  <div className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center text-xs font-bold text-primary shrink-0">
                    {client.name.charAt(0)}
                  </div>
                  <div className="flex-1">
                    <div className="flex items-center justify-between mb-1">
                      <p className="text-sm font-medium">{client.name}</p>
                      <div className="flex items-center gap-2">
                        <span className="text-sm font-bold">{formatCurrency(client.revenue)}</span>
                        <Badge className="text-[10px]">{client.percentage.toFixed(1)}%</Badge>
                      </div>
                    </div>
                    <div className="h-2 bg-muted rounded-full overflow-hidden">
                      <div
                        className="h-full bg-primary rounded-full transition-all"
                        style={{ width: `${Math.min(100, client.percentage)}%` }}
                      />
                    </div>
                    <p className="text-xs text-muted-foreground mt-1">
                      {client.invoiceCount} invoice{client.invoiceCount !== 1 ? "s" : ""}
                    </p>
                  </div>
                </div>
              ))}
            </div>
            {topClients[0]?.percentage > 40 && (
              <div className="mt-4 p-3 rounded-lg bg-amber-50 border border-amber-200">
                <p className="text-xs text-amber-800">
                  <AlertTriangle className="h-3.5 w-3.5 inline mr-1" />
                  <strong>Revenue Concentration Risk:</strong> {topClients[0]?.name} accounts for{" "}
                  {topClients[0]?.percentage.toFixed(1)}% of your revenue. Consider diversifying your client base.
                </p>
              </div>
            )}
          </CardContent>
        </Card>
      )}

      {/* Monthly Trends Summary */}
      {trends.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>Recent Trend Analysis</CardTitle>
            <CardDescription>Month-over-month performance metrics</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {[
                {
                  label: "Revenue Trend",
                  value: latestTrend?.revenue,
                  change: expenseChange,
                  icon: TrendingUp,
                  positive: true,
                },
                {
                  label: "Expense Trend",
                  value: latestTrend?.expenses,
                  change: expenseChange,
                  icon: TrendingDown,
                  positive: false,
                },
                {
                  label: "Profit",
                  value: latestTrend?.profit,
                  icon: CheckCircle,
                  positive: latestTrend?.profit >= 0,
                },
              ].map((item) => (
                <div key={item.label} className="border rounded-lg p-3">
                  <div className="flex items-center gap-2 mb-2">
                    <item.icon className={`h-4 w-4 ${item.positive ? "text-emerald-500" : "text-red-500"}`} />
                    <p className="text-xs text-muted-foreground">{item.label}</p>
                  </div>
                  <p className={`text-lg font-bold ${item.positive ? "text-emerald-600" : "text-red-600"}`}>
                    {formatCurrency(item.value ?? 0)}
                  </p>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  )
}
