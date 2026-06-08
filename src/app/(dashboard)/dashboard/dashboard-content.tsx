"use client"

import { useQuery } from "@tanstack/react-query"
import { MetricCard, MetricCardSkeleton } from "@/components/dashboard/metric-card"
import { RevenueChart } from "@/components/charts/revenue-chart"
import { ExpenseDonut } from "@/components/charts/expense-donut"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import {
  DollarSign, TrendingUp, TrendingDown, FileText,
  AlertTriangle, ArrowRight, Bot, RefreshCw,
  CreditCard, Users, Clock
} from "lucide-react"
import { formatCurrency, formatDate, getStatusColor } from "@/lib/utils"
import Link from "next/link"
import axios from "axios"

// Fetch dashboard metrics from API
async function fetchDashboardData() {
  const res = await axios.get("/api/dashboard")
  return res.data.data
}

async function fetchMonthlyTrends() {
  const res = await axios.get("/api/dashboard/trends")
  return res.data.data
}

async function fetchExpenseCategories() {
  const res = await axios.get("/api/dashboard/categories")
  return res.data.data
}

async function fetchRecentActivity() {
  const res = await axios.get("/api/dashboard/activity")
  return res.data.data
}

export function DashboardContent() {
  const { data: metrics, isLoading: metricsLoading, refetch } = useQuery({
    queryKey: ["dashboard-metrics"],
    queryFn: fetchDashboardData,
  })

  const { data: trends, isLoading: trendsLoading } = useQuery({
    queryKey: ["monthly-trends"],
    queryFn: fetchMonthlyTrends,
  })

  const { data: categories, isLoading: categoriesLoading } = useQuery({
    queryKey: ["expense-categories"],
    queryFn: fetchExpenseCategories,
  })

  const { data: activity } = useQuery({
    queryKey: ["recent-activity"],
    queryFn: fetchRecentActivity,
  })

  if (metricsLoading) {
    return (
      <div className="space-y-6">
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
          {[1, 2, 3, 4].map((i) => <MetricCardSkeleton key={i} />)}
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Refresh Button */}
      <div className="flex items-center justify-end">
        <Button variant="outline" size="sm" onClick={() => refetch()}>
          <RefreshCw className="h-3.5 w-3.5 mr-1.5" />
          Refresh
        </Button>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <MetricCard
          title="Total Revenue"
          value={metrics?.revenue ?? 0}
          change={metrics?.revenueChange}
          icon={DollarSign}
          iconColor="text-blue-600"
          trend="up"
        />
        <MetricCard
          title="Total Expenses"
          value={metrics?.expenses ?? 0}
          change={metrics?.expensesChange}
          icon={CreditCard}
          iconColor="text-red-600"
          trend="down"
        />
        <MetricCard
          title="Net Profit"
          value={metrics?.profit ?? 0}
          change={metrics?.profitChange}
          icon={TrendingUp}
          iconColor="text-emerald-600"
          trend="up"
        />
        <MetricCard
          title="Outstanding Invoices"
          value={metrics?.outstandingInvoices ?? 0}
          icon={FileText}
          iconColor="text-amber-600"
        />
      </div>

      {/* Secondary Metrics */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <Card className="border-l-4 border-l-red-500">
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">Overdue Invoices</p>
                <p className="text-xl font-bold text-red-600">
                  {formatCurrency(metrics?.overdueAmount ?? 0)}
                </p>
                <p className="text-xs text-muted-foreground mt-1">
                  {metrics?.overdueCount ?? 0} invoices overdue
                </p>
              </div>
              <AlertTriangle className="h-8 w-8 text-red-400" />
            </div>
          </CardContent>
        </Card>

        <Card className="border-l-4 border-l-emerald-500">
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">Collected This Period</p>
                <p className="text-xl font-bold text-emerald-600">
                  {formatCurrency(metrics?.collectedThisPeriod ?? 0)}
                </p>
                <p className="text-xs text-muted-foreground mt-1">
                  From payments received
                </p>
              </div>
              <TrendingUp className="h-8 w-8 text-emerald-400" />
            </div>
          </CardContent>
        </Card>

        <Card className="border-l-4 border-l-blue-500">
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">Profit Margin</p>
                <p className="text-xl font-bold text-blue-600">
                  {(metrics?.profitMargin ?? 0).toFixed(1)}%
                </p>
                <p className="text-xs text-muted-foreground mt-1">
                  Current period
                </p>
              </div>
              <TrendingUp className="h-8 w-8 text-blue-400" />
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Revenue Chart */}
        <Card className="lg:col-span-2">
          <CardHeader>
            <div className="flex items-center justify-between">
              <div>
                <CardTitle>Revenue vs Expenses</CardTitle>
                <CardDescription>12-month financial trends</CardDescription>
              </div>
              <Link href="/reports">
                <Button variant="ghost" size="sm">
                  View Reports
                  <ArrowRight className="ml-1 h-3.5 w-3.5" />
                </Button>
              </Link>
            </div>
          </CardHeader>
          <CardContent>
            {trendsLoading ? (
              <div className="skeleton h-[300px] rounded-lg" />
            ) : (
              <RevenueChart data={trends ?? []} />
            )}
          </CardContent>
        </Card>

        {/* Expense Donut */}
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <div>
                <CardTitle>Expenses by Category</CardTitle>
                <CardDescription>Current period breakdown</CardDescription>
              </div>
            </div>
          </CardHeader>
          <CardContent>
            {categoriesLoading ? (
              <div className="skeleton h-[250px] rounded-lg" />
            ) : (
              <ExpenseDonut data={categories ?? []} />
            )}
          </CardContent>
        </Card>
      </div>

      {/* Bottom Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Recent Activity */}
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <div>
                <CardTitle>Recent Activity</CardTitle>
                <CardDescription>Latest transactions and invoices</CardDescription>
              </div>
              <Link href="/transactions">
                <Button variant="ghost" size="sm">
                  View All
                  <ArrowRight className="ml-1 h-3.5 w-3.5" />
                </Button>
              </Link>
            </div>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {activity?.transactions?.slice(0, 5).map((tx: {
                id: string
                type: string
                description: string
                amount: string | number
                date: string
              }) => (
                <div key={tx.id} className="flex items-center justify-between py-2 border-b last:border-0">
                  <div className="flex items-center gap-3">
                    <div className={`h-8 w-8 rounded-full flex items-center justify-center text-xs font-bold ${
                      tx.type === "INCOME" ? "bg-emerald-100 text-emerald-700" : "bg-red-100 text-red-700"
                    }`}>
                      {tx.type === "INCOME" ? "+" : "-"}
                    </div>
                    <div>
                      <p className="text-sm font-medium">{tx.description}</p>
                      <p className="text-xs text-muted-foreground">{formatDate(tx.date, "short")}</p>
                    </div>
                  </div>
                  <span className={`text-sm font-semibold ${
                    tx.type === "INCOME" ? "text-emerald-600" : "text-red-600"
                  }`}>
                    {tx.type === "INCOME" ? "+" : "-"}{formatCurrency(Number(tx.amount))}
                  </span>
                </div>
              )) ?? (
                <div className="text-center py-8 text-muted-foreground">
                  <Clock className="h-8 w-8 mx-auto mb-2 opacity-50" />
                  <p className="text-sm">No recent activity</p>
                </div>
              )}
            </div>
          </CardContent>
        </Card>

        {/* Quick Actions & AI Insights */}
        <Card>
          <CardHeader>
            <CardTitle>Quick Actions</CardTitle>
            <CardDescription>Common tasks and AI assistant</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            {/* Quick Actions */}
            <div className="grid grid-cols-2 gap-2">
              <Link href="/invoices">
                <Button variant="outline" className="w-full h-auto py-3 flex-col gap-1" size="sm">
                  <FileText className="h-5 w-5" />
                  <span className="text-xs">New Invoice</span>
                </Button>
              </Link>
              <Link href="/expenses">
                <Button variant="outline" className="w-full h-auto py-3 flex-col gap-1" size="sm">
                  <CreditCard className="h-5 w-5" />
                  <span className="text-xs">Add Expense</span>
                </Button>
              </Link>
              <Link href="/reports">
                <Button variant="outline" className="w-full h-auto py-3 flex-col gap-1" size="sm">
                  <TrendingDown className="h-5 w-5" />
                  <span className="text-xs">Run Report</span>
                </Button>
              </Link>
              <Link href="/bank-statements">
                <Button variant="outline" className="w-full h-auto py-3 flex-col gap-1" size="sm">
                  <Users className="h-5 w-5" />
                  <span className="text-xs">Upload Statement</span>
                </Button>
              </Link>
            </div>

            {/* AI Assistant CTA */}
            <div className="rounded-xl bg-gradient-to-br from-blue-500 to-purple-600 p-4 text-white">
              <div className="flex items-center gap-2 mb-2">
                <Bot className="h-5 w-5" />
                <span className="font-semibold text-sm">Ask Your AI Assistant</span>
              </div>
              <p className="text-xs text-blue-100 mb-3">
                "How much profit did I make last month?" or "Which expenses increased most?"
              </p>
              <Link href="/ai-assistant">
                <Button size="sm" className="bg-white text-blue-600 hover:bg-blue-50 w-full">
                  Open AI Assistant
                  <ArrowRight className="ml-1 h-3.5 w-3.5" />
                </Button>
              </Link>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
