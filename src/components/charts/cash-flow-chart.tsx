"use client"

import {
  ComposedChart,
  Bar,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
  ReferenceLine,
} from "recharts"
import { formatCurrency } from "@/lib/utils"

interface CashFlowData {
  month: string
  expectedIncome?: number
  expectedExpenses?: number
  expectedBalance?: number
  revenue?: number
  expenses?: number
  balance?: number
  confidence?: number
  isForecast?: boolean
}

interface CashFlowChartProps {
  data: CashFlowData[]
  showForecast?: boolean
}

const CustomTooltip = ({ active, payload, label }: {
  active?: boolean
  payload?: Array<{ color: string; name: string; value: number; payload: CashFlowData }>
  label?: string
}) => {
  if (active && payload && payload.length) {
    const isForecast = payload[0]?.payload?.isForecast
    return (
      <div className="rounded-lg border bg-background p-3 shadow-lg">
        <div className="flex items-center gap-2 mb-2">
          <p className="text-sm font-semibold">{label}</p>
          {isForecast && (
            <span className="text-[10px] bg-purple-100 text-purple-700 px-1.5 py-0.5 rounded font-medium">
              Forecast
            </span>
          )}
        </div>
        {payload.map((entry) => (
          <div key={entry.name} className="flex items-center gap-2 text-xs">
            <div className="h-2 w-2 rounded-full" style={{ backgroundColor: entry.color }} />
            <span className="text-muted-foreground">{entry.name}:</span>
            <span className="font-medium">{formatCurrency(entry.value)}</span>
          </div>
        ))}
      </div>
    )
  }
  return null
}

export function CashFlowChart({ data, showForecast = false }: CashFlowChartProps) {
  return (
    <ResponsiveContainer width="100%" height={320}>
      <ComposedChart data={data} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
        <CartesianGrid strokeDasharray="3 3" className="stroke-border" />
        <XAxis
          dataKey="month"
          tick={{ fontSize: 12 }}
          tickLine={false}
          axisLine={false}
        />
        <YAxis
          tickFormatter={(v) => `$${(v / 1000).toFixed(0)}k`}
          tick={{ fontSize: 12 }}
          tickLine={false}
          axisLine={false}
        />
        <Tooltip content={<CustomTooltip />} />
        <Legend iconType="circle" iconSize={8} wrapperStyle={{ fontSize: "12px", paddingTop: "12px" }} />
        <ReferenceLine y={0} stroke="#e5e7eb" strokeWidth={2} />

        <Bar
          dataKey={showForecast ? "expectedIncome" : "revenue"}
          name="Income"
          fill="#3b82f6"
          radius={[3, 3, 0, 0]}
          maxBarSize={40}
          opacity={showForecast ? 0.7 : 1}
        />
        <Bar
          dataKey={showForecast ? "expectedExpenses" : "expenses"}
          name="Expenses"
          fill="#ef4444"
          radius={[3, 3, 0, 0]}
          maxBarSize={40}
          opacity={showForecast ? 0.7 : 1}
        />
        <Line
          type="monotone"
          dataKey={showForecast ? "expectedBalance" : "balance"}
          name="Net Balance"
          stroke="#8b5cf6"
          strokeWidth={2}
          dot={{ r: 3 }}
          activeDot={{ r: 5 }}
          strokeDasharray={showForecast ? "5 5" : "0"}
        />
      </ComposedChart>
    </ResponsiveContainer>
  )
}
