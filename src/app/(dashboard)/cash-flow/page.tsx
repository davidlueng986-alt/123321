"use client"

import { useQuery } from "@tanstack/react-query"
import axios from "axios"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { CashFlowChart } from "@/components/charts/cash-flow-chart"
import { formatCurrency } from "@/lib/utils"
import { TrendingUp, TrendingDown, AlertCircle, CheckCircle, Activity } from "lucide-react"

export default function CashFlowPage() {
  const { data, isLoading } = useQuery({
    queryKey: ["cash-flow"],
    queryFn: async () => {
      const res = await axios.get("/api/cash-flow?months=6&forecastMonths=3")
      return res.data.data
    },
  })

  const historical = data?.historical ?? []
  const forecast = data?.forecast ?? []

  // Mark forecast data
  const forecastWithFlag = forecast.map((f: {
    month: string
    expectedIncome: number
    expectedExpenses: number
    expectedBalance: number
    confidence: number
  }) => ({ ...f, isForecast: true }))

  const combined = [
    ...historical.map((h: {
      month: string
      revenue: number
      expenses: number
      profit: number
      balance: number
    }) => ({ ...h, isForecast: false })),
    ...forecastWithFlag,
  ]

  const lastHistorical = historical[historical.length - 1]
  const nextForecast = forecast[0]

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold">Cash Flow</h1>
        <p className="text-muted-foreground">
          Historical cash flow and deterministic 3-month forecast
        </p>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <Card className="border-l-4 border-l-blue-500">
          <CardContent className="p-4">
            <p className="text-sm text-muted-foreground">Last Month Net</p>
            <p className={`text-xl font-bold ${lastHistorical?.profit >= 0 ? "text-emerald-600" : "text-red-600"}`}>
              {isLoading ? "—" : formatCurrency(lastHistorical?.profit ?? 0)}
            </p>
            <div className="flex items-center gap-1 mt-1">
              {lastHistorical?.profit >= 0 ? (
                <TrendingUp className="h-3.5 w-3.5 text-emerald-500" />
              ) : (
                <TrendingDown className="h-3.5 w-3.5 text-red-500" />
              )}
              <p className="text-xs text-muted-foreground">
                Revenue: {formatCurrency(lastHistorical?.revenue ?? 0)}
              </p>
            </div>
          </CardContent>
        </Card>

        <Card className="border-l-4 border-l-purple-500">
          <CardContent className="p-4">
            <p className="text-sm text-muted-foreground">Next Month Forecast</p>
            <p className={`text-xl font-bold ${(nextForecast?.expectedBalance ?? 0) >= 0 ? "text-emerald-600" : "text-red-600"}`}>
              {isLoading ? "—" : formatCurrency(nextForecast?.expectedBalance ?? 0)}
            </p>
            {nextForecast && (
              <div className="flex items-center gap-1 mt-1">
                <Activity className="h-3.5 w-3.5 text-purple-500" />
                <p className="text-xs text-muted-foreground">
                  {nextForecast.confidence}% confidence
                </p>
              </div>
            )}
          </CardContent>
        </Card>

        <Card className="border-l-4 border-l-emerald-500">
          <CardContent className="p-4">
            <p className="text-sm text-muted-foreground">Forecast Status</p>
            <div className="flex items-center gap-2 mt-1">
              {(nextForecast?.expectedBalance ?? 0) >= 0 ? (
                <>
                  <CheckCircle className="h-5 w-5 text-emerald-500" />
                  <p className="text-base font-semibold text-emerald-600">Positive</p>
                </>
              ) : (
                <>
                  <AlertCircle className="h-5 w-5 text-red-500" />
                  <p className="text-base font-semibold text-red-600">Deficit Warning</p>
                </>
              )}
            </div>
            <p className="text-xs text-muted-foreground mt-1">
              Based on 6-month historical trend
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Main Chart */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle>Cash Flow Overview</CardTitle>
              <CardDescription>
                Historical performance + deterministic 3-month forecast
              </CardDescription>
            </div>
            <div className="flex items-center gap-2">
              <Badge variant="secondary" className="text-xs">Historical</Badge>
              <Badge className="text-xs bg-purple-100 text-purple-700 border-purple-200">
                Forecast
              </Badge>
            </div>
          </div>
        </CardHeader>
        <CardContent>
          {isLoading ? (
            <div className="skeleton h-80 rounded-lg" />
          ) : (
            <CashFlowChart data={combined.map((d) => ({
              ...d,
              month: d.month,
            }))} showForecast={false} />
          )}
        </CardContent>
      </Card>

      {/* Forecast Table */}
      {forecast.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>3-Month Forecast Details</CardTitle>
            <CardDescription>
              Calculated using linear trend analysis on historical data. All values are deterministic.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {forecast.map((f: {
                month: string
                expectedIncome: number
                expectedExpenses: number
                expectedBalance: number
                confidence: number
              }) => (
                <div key={f.month} className="flex items-center justify-between border rounded-lg p-4">
                  <div className="flex items-center gap-4">
                    <div>
                      <p className="font-semibold">{f.month}</p>
                      <p className="text-xs text-muted-foreground">
                        {f.confidence}% confidence
                      </p>
                    </div>
                  </div>
                  <div className="grid grid-cols-3 gap-8 text-sm">
                    <div className="text-center">
                      <p className="text-xs text-muted-foreground">Expected Income</p>
                      <p className="font-semibold text-emerald-600">{formatCurrency(f.expectedIncome)}</p>
                    </div>
                    <div className="text-center">
                      <p className="text-xs text-muted-foreground">Expected Expenses</p>
                      <p className="font-semibold text-red-600">{formatCurrency(f.expectedExpenses)}</p>
                    </div>
                    <div className="text-center">
                      <p className="text-xs text-muted-foreground">Expected Balance</p>
                      <p className={`font-bold ${f.expectedBalance >= 0 ? "text-emerald-600" : "text-red-600"}`}>
                        {formatCurrency(f.expectedBalance)}
                      </p>
                    </div>
                  </div>
                  <Badge
                    className={`text-[10px] ${
                      f.confidence > 75
                        ? "bg-emerald-100 text-emerald-700"
                        : f.confidence > 60
                        ? "bg-amber-100 text-amber-700"
                        : "bg-red-100 text-red-700"
                    }`}
                  >
                    {f.confidence > 75 ? "High" : f.confidence > 60 ? "Medium" : "Low"} Confidence
                  </Badge>
                </div>
              ))}
            </div>
            <p className="text-xs text-muted-foreground mt-4 border-t pt-3">
              ⚠️ Forecasts are based on linear trend analysis of historical data. Past performance does not guarantee future results.
              All calculations are deterministic — AI is used only to explain these numbers, not calculate them.
            </p>
          </CardContent>
        </Card>
      )}
    </div>
  )
}
