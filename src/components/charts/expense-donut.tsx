"use client"

import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from "recharts"
import { formatCurrency } from "@/lib/utils"

interface ExpenseData {
  name: string
  amount: number
  percentage: number
  color: string
}

interface ExpenseDonutProps {
  data: ExpenseData[]
}

const CustomTooltip = ({ active, payload }: {
  active?: boolean
  payload?: Array<{ payload: ExpenseData }>
}) => {
  if (active && payload && payload.length) {
    const d = payload[0].payload
    return (
      <div className="rounded-lg border bg-background p-3 shadow-lg">
        <p className="font-semibold text-sm">{d.name}</p>
        <p className="text-xs text-muted-foreground mt-1">
          {formatCurrency(d.amount)}
        </p>
        <p className="text-xs text-muted-foreground">
          {d.percentage.toFixed(1)}% of total
        </p>
      </div>
    )
  }
  return null
}

const RADIAN = Math.PI / 180
const renderCustomLabel = ({
  cx, cy, midAngle, innerRadius, outerRadius, percentage
}: {
  cx: number; cy: number; midAngle: number
  innerRadius: number; outerRadius: number; percentage: number
}) => {
  if (percentage < 5) return null
  const radius = innerRadius + (outerRadius - innerRadius) * 0.5
  const x = cx + radius * Math.cos(-midAngle * RADIAN)
  const y = cy + radius * Math.sin(-midAngle * RADIAN)
  return (
    <text x={x} y={y} fill="white" textAnchor="middle" dominantBaseline="central" fontSize={10} fontWeight="bold">
      {`${percentage.toFixed(0)}%`}
    </text>
  )
}

export function ExpenseDonut({ data }: ExpenseDonutProps) {
  if (!data || data.length === 0) {
    return (
      <div className="flex items-center justify-center h-[250px] text-muted-foreground text-sm">
        No expense data available
      </div>
    )
  }

  return (
    <ResponsiveContainer width="100%" height={250}>
      <PieChart>
        <Pie
          data={data}
          cx="50%"
          cy="50%"
          innerRadius={60}
          outerRadius={90}
          paddingAngle={2}
          dataKey="amount"
          labelLine={false}
          label={renderCustomLabel}
        >
          {data.map((entry, index) => (
            <Cell key={`cell-${index}`} fill={entry.color} />
          ))}
        </Pie>
        <Tooltip content={<CustomTooltip />} />
        <Legend
          iconType="circle"
          iconSize={8}
          wrapperStyle={{ fontSize: "11px" }}
          formatter={(value) => (
            <span className="text-foreground">{value}</span>
          )}
        />
      </PieChart>
    </ResponsiveContainer>
  )
}
