"use client"

import { Card, CardContent } from "@/components/ui/card"
import { cn, formatCurrency, formatPercentage } from "@/lib/utils"
import { TrendingUp, TrendingDown, Minus, LucideIcon } from "lucide-react"

interface MetricCardProps {
  title: string
  value: number
  change?: number
  changeLabel?: string
  icon: LucideIcon
  iconColor?: string
  format?: "currency" | "number" | "percentage"
  prefix?: string
  suffix?: string
  className?: string
  trend?: "up" | "down" | "neutral"
}

export function MetricCard({
  title,
  value,
  change,
  changeLabel = "vs last period",
  icon: Icon,
  iconColor = "text-primary",
  format = "currency",
  prefix,
  suffix,
  className,
  trend,
}: MetricCardProps) {
  const isPositive = change !== undefined ? change >= 0 : true
  const TrendIcon = change === 0 ? Minus : change && change > 0 ? TrendingUp : TrendingDown

  const formattedValue =
    format === "currency"
      ? formatCurrency(value)
      : format === "percentage"
      ? `${value.toFixed(1)}%`
      : `${prefix ?? ""}${value.toLocaleString()}${suffix ?? ""}`

  const trendColor =
    trend === "up"
      ? isPositive
        ? "text-emerald-600"
        : "text-red-500"
      : trend === "down"
      ? isPositive
        ? "text-red-500"
        : "text-emerald-600"
      : isPositive
      ? "text-emerald-600"
      : "text-red-500"

  return (
    <Card className={cn("card-hover relative overflow-hidden", className)}>
      {/* Background decoration */}
      <div className="absolute -right-4 -top-4 h-24 w-24 rounded-full opacity-5 bg-primary" />
      
      <CardContent className="p-6">
        <div className="flex items-start justify-between">
          <div className="flex-1">
            <p className="text-sm font-medium text-muted-foreground">{title}</p>
            <p className="mt-2 text-2xl font-bold tracking-tight">{formattedValue}</p>
            
            {change !== undefined && (
              <div className={cn("mt-2 flex items-center gap-1 text-xs font-medium", trendColor)}>
                <TrendIcon className="h-3 w-3" />
                <span>{formatPercentage(Math.abs(change))}</span>
                <span className="text-muted-foreground font-normal ml-1">{changeLabel}</span>
              </div>
            )}
          </div>

          <div className={cn(
            "flex h-10 w-10 items-center justify-center rounded-xl",
            "bg-primary/10"
          )}>
            <Icon className={cn("h-5 w-5", iconColor)} />
          </div>
        </div>
      </CardContent>
    </Card>
  )
}

// Skeleton version
export function MetricCardSkeleton() {
  return (
    <Card>
      <CardContent className="p-6">
        <div className="flex items-start justify-between">
          <div className="flex-1 space-y-2">
            <div className="skeleton h-4 w-24 rounded" />
            <div className="skeleton h-8 w-32 rounded" />
            <div className="skeleton h-3 w-40 rounded" />
          </div>
          <div className="skeleton h-10 w-10 rounded-xl" />
        </div>
      </CardContent>
    </Card>
  )
}
