"use client"

import { useState } from "react"
import { useQuery } from "@tanstack/react-query"
import axios from "axios"
import { Card, CardContent, CardHeader } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { formatCurrency, formatDate, getStatusColor } from "@/lib/utils"
import { Search, ArrowLeftRight, TrendingUp, TrendingDown } from "lucide-react"

export default function TransactionsPage() {
  const [type, setType] = useState("ALL")
  const [search, setSearch] = useState("")
  const [page, setPage] = useState(1)

  const { data, isLoading } = useQuery({
    queryKey: ["transactions", type, search, page],
    queryFn: async () => {
      const params = new URLSearchParams({ page: String(page), limit: "20" })
      if (type !== "ALL") params.set("type", type)
      if (search) params.set("search", search)
      const res = await axios.get(`/api/transactions?${params}`)
      return res.data.data
    },
  })

  const transactions = data?.transactions ?? []
  const summary = data?.summary ?? { income: 0, expenses: 0, net: 0 }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold">Transactions</h1>
        <p className="text-muted-foreground">All financial transactions in one place</p>
      </div>

      {/* Summary */}
      <div className="grid grid-cols-3 gap-4">
        <Card className="border-l-4 border-l-emerald-500">
          <CardContent className="p-4">
            <div className="flex items-center gap-2">
              <TrendingUp className="h-5 w-5 text-emerald-500" />
              <div>
                <p className="text-xs text-muted-foreground">Total Income</p>
                <p className="text-lg font-bold text-emerald-600">{formatCurrency(summary.income)}</p>
              </div>
            </div>
          </CardContent>
        </Card>
        <Card className="border-l-4 border-l-red-500">
          <CardContent className="p-4">
            <div className="flex items-center gap-2">
              <TrendingDown className="h-5 w-5 text-red-500" />
              <div>
                <p className="text-xs text-muted-foreground">Total Expenses</p>
                <p className="text-lg font-bold text-red-600">{formatCurrency(summary.expenses)}</p>
              </div>
            </div>
          </CardContent>
        </Card>
        <Card className="border-l-4 border-l-blue-500">
          <CardContent className="p-4">
            <div className="flex items-center gap-2">
              <ArrowLeftRight className="h-5 w-5 text-blue-500" />
              <div>
                <p className="text-xs text-muted-foreground">Net Balance</p>
                <p className={`text-lg font-bold ${summary.net >= 0 ? "text-emerald-600" : "text-red-600"}`}>
                  {formatCurrency(summary.net)}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Table */}
      <Card>
        <CardHeader className="pb-3">
          <div className="flex flex-col sm:flex-row gap-3">
            <Tabs value={type} onValueChange={(v) => { setType(v); setPage(1) }}>
              <TabsList className="h-8">
                {["ALL", "INCOME", "EXPENSE", "TRANSFER"].map((t) => (
                  <TabsTrigger key={t} value={t} className="text-xs">{t}</TabsTrigger>
                ))}
              </TabsList>
            </Tabs>
            <div className="relative flex-1 sm:max-w-xs">
              <Search className="absolute left-2.5 top-2 h-4 w-4 text-muted-foreground" />
              <Input
                placeholder="Search..."
                className="pl-8 h-8"
                value={search}
                onChange={(e) => { setSearch(e.target.value); setPage(1) }}
              />
            </div>
          </div>
        </CardHeader>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Description</TableHead>
              <TableHead>Category</TableHead>
              <TableHead>Date</TableHead>
              <TableHead>Type</TableHead>
              <TableHead className="text-right">Amount</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {isLoading ? (
              [...Array(8)].map((_, i) => (
                <TableRow key={i}>
                  {[...Array(5)].map((_, j) => (
                    <TableCell key={j}><div className="skeleton h-4 rounded w-24" /></TableCell>
                  ))}
                </TableRow>
              ))
            ) : transactions.length === 0 ? (
              <TableRow>
                <TableCell colSpan={5} className="text-center py-10 text-muted-foreground">
                  <ArrowLeftRight className="h-10 w-10 mx-auto mb-2 opacity-30" />
                  No transactions found
                </TableCell>
              </TableRow>
            ) : (
              transactions.map((tx: {
                id: string
                description: string
                category?: { name: string; color: string }
                date: string
                type: string
                amount: string | number
              }) => (
                <TableRow key={tx.id}>
                  <TableCell className="font-medium">{tx.description}</TableCell>
                  <TableCell>
                    {tx.category ? (
                      <Badge variant="outline" style={{ borderColor: tx.category.color }}>
                        {tx.category.name}
                      </Badge>
                    ) : "—"}
                  </TableCell>
                  <TableCell className="text-muted-foreground">{formatDate(tx.date, "short")}</TableCell>
                  <TableCell>
                    <Badge className={`text-[10px] border ${getStatusColor(tx.type)}`}>
                      {tx.type}
                    </Badge>
                  </TableCell>
                  <TableCell className={`text-right font-semibold ${tx.type === "INCOME" ? "text-emerald-600" : "text-red-600"}`}>
                    {tx.type === "INCOME" ? "+" : "-"}{formatCurrency(Number(tx.amount))}
                  </TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>

        {/* Pagination */}
        {data?.pages > 1 && (
          <div className="flex items-center justify-between p-4 border-t">
            <p className="text-sm text-muted-foreground">
              Page {page} of {data.pages}
            </p>
            <div className="flex gap-2">
              <Button variant="outline" size="sm" onClick={() => setPage(p => Math.max(1, p - 1))} disabled={page === 1}>
                Previous
              </Button>
              <Button variant="outline" size="sm" onClick={() => setPage(p => p + 1)} disabled={page >= data.pages}>
                Next
              </Button>
            </div>
          </div>
        )}
      </Card>
    </div>
  )
}
