"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"
import { cn } from "@/lib/utils"
import {
  LayoutDashboard,
  FileText,
  Receipt,
  ArrowLeftRight,
  BarChart3,
  Lightbulb,
  TrendingUp,
  Bot,
  Building2,
  Settings,
  ChevronLeft,
  ChevronRight,
  Zap,
} from "lucide-react"
import { useState } from "react"
import { Button } from "@/components/ui/button"

const navigation = [
  {
    title: "Overview",
    items: [
      { name: "Dashboard", href: "/dashboard", icon: LayoutDashboard },
    ],
  },
  {
    title: "Finance",
    items: [
      { name: "Invoices", href: "/invoices", icon: FileText },
      { name: "Expenses", href: "/expenses", icon: Receipt },
      { name: "Transactions", href: "/transactions", icon: ArrowLeftRight },
      { name: "Bank Statements", href: "/bank-statements", icon: Building2 },
    ],
  },
  {
    title: "Intelligence",
    items: [
      { name: "AI Assistant", href: "/ai-assistant", icon: Bot },
      { name: "AI Insights", href: "/insights", icon: Lightbulb },
      { name: "Cash Flow", href: "/cash-flow", icon: TrendingUp },
      { name: "Reports", href: "/reports", icon: BarChart3 },
    ],
  },
  {
    title: "System",
    items: [
      { name: "Settings", href: "/settings", icon: Settings },
    ],
  },
]

export function Sidebar() {
  const pathname = usePathname()
  const [collapsed, setCollapsed] = useState(false)

  return (
    <aside
      className={cn(
        "fixed left-0 top-0 z-30 flex h-screen flex-col border-r bg-card transition-all duration-300",
        collapsed ? "w-16" : "w-64"
      )}
    >
      {/* Logo */}
      <div className={cn(
        "flex h-16 items-center border-b px-4",
        collapsed ? "justify-center" : "justify-between"
      )}>
        {!collapsed && (
          <Link href="/dashboard" className="flex items-center gap-2">
            <div className="flex h-8 w-8 items-center justify-center rounded-lg gradient-blue">
              <Zap className="h-4 w-4 text-white" />
            </div>
            <div>
              <p className="text-sm font-bold tracking-tight">FinSight AI</p>
              <p className="text-[10px] text-muted-foreground">Financial Intelligence</p>
            </div>
          </Link>
        )}
        {collapsed && (
          <Link href="/dashboard">
            <div className="flex h-8 w-8 items-center justify-center rounded-lg gradient-blue">
              <Zap className="h-4 w-4 text-white" />
            </div>
          </Link>
        )}
        <Button
          variant="ghost"
          size="icon"
          className={cn("h-8 w-8 shrink-0", collapsed && "absolute -right-3 top-5 z-50 border bg-background shadow-md rounded-full")}
          onClick={() => setCollapsed(!collapsed)}
        >
          {collapsed ? (
            <ChevronRight className="h-4 w-4" />
          ) : (
            <ChevronLeft className="h-4 w-4" />
          )}
        </Button>
      </div>

      {/* Navigation */}
      <nav className="flex-1 overflow-y-auto px-3 py-4">
        {navigation.map((section) => (
          <div key={section.title} className="mb-6">
            {!collapsed && (
              <p className="mb-2 px-2 text-[10px] font-semibold uppercase tracking-widest text-muted-foreground">
                {section.title}
              </p>
            )}
            <ul className="space-y-1">
              {section.items.map((item) => {
                const isActive = pathname === item.href || pathname?.startsWith(`${item.href}/`)
                return (
                  <li key={item.name}>
                    <Link
                      href={item.href}
                      className={cn(
                        "group flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-all",
                        isActive
                          ? "bg-primary text-primary-foreground shadow-sm"
                          : "text-muted-foreground hover:bg-accent hover:text-accent-foreground",
                        collapsed && "justify-center px-2"
                      )}
                      title={collapsed ? item.name : undefined}
                    >
                      <item.icon className={cn("h-4 w-4 shrink-0", isActive ? "text-white" : "")} />
                      {!collapsed && <span>{item.name}</span>}
                    </Link>
                  </li>
                )
              })}
            </ul>
          </div>
        ))}
      </nav>

      {/* Footer */}
      {!collapsed && (
        <div className="border-t p-4">
          <div className="rounded-lg bg-primary/10 p-3">
            <div className="flex items-center gap-2 mb-2">
              <Bot className="h-4 w-4 text-primary" />
              <span className="text-xs font-semibold text-primary">AI Powered</span>
            </div>
            <p className="text-[10px] text-muted-foreground leading-relaxed">
              Ask your AI assistant anything about your finances.
            </p>
          </div>
        </div>
      )}
    </aside>
  )
}
