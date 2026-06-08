"use client"

import { useState } from "react"
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query"
import axios from "axios"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Badge } from "@/components/ui/badge"
import { Card, CardContent, CardHeader } from "@/components/ui/card"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { formatCurrency, formatDate, getStatusColor } from "@/lib/utils"
import { Plus, Search, Receipt, Upload } from "lucide-react"
import { toast } from "sonner"

const STATUS_TABS = ["ALL", "PENDING", "APPROVED", "REJECTED"]

export default function ExpensesPage() {
  const [status, setStatus] = useState("ALL")
  const [search, setSearch] = useState("")
  const [createOpen, setCreateOpen] = useState(false)
  const qc = useQueryClient()

  const { data, isLoading } = useQuery({
    queryKey: ["expenses", status, search],
    queryFn: async () => {
      const params = new URLSearchParams()
      if (status !== "ALL") params.set("status", status)
      const res = await axios.get(`/api/expenses?${params}`)
      return res.data.data
    },
  })

  const createMutation = useMutation({
    mutationFn: (data: Record<string, unknown>) => axios.post("/api/expenses", data),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["expenses"] })
      qc.invalidateQueries({ queryKey: ["dashboard-metrics"] })
      setCreateOpen(false)
      toast.success("Expense added successfully")
    },
    onError: () => toast.error("Failed to add expense"),
  })

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    const form = e.currentTarget
    const fd = new FormData(form)
    createMutation.mutate({
      amount: parseFloat(fd.get("amount") as string),
      description: fd.get("description"),
      date: fd.get("date"),
      notes: fd.get("notes"),
      currency: "USD",
    })
  }

  const expenses = data?.expenses ?? []

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Expenses</h1>
          <p className="text-muted-foreground">Track and manage business expenses</p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline">
            <Upload className="h-4 w-4 mr-1.5" />
            Import CSV
          </Button>
          <Dialog open={createOpen} onOpenChange={setCreateOpen}>
            <DialogTrigger asChild>
              <Button>
                <Plus className="h-4 w-4 mr-1.5" />
                Add Expense
              </Button>
            </DialogTrigger>
            <DialogContent>
              <DialogHeader>
                <DialogTitle>Add Expense</DialogTitle>
              </DialogHeader>
              <form onSubmit={handleSubmit} className="space-y-4">
                <div className="space-y-1.5">
                  <Label>Description *</Label>
                  <Input name="description" placeholder="What was this expense for?" required />
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-1.5">
                    <Label>Amount ($) *</Label>
                    <Input name="amount" type="number" step="0.01" min="0" placeholder="0.00" required />
                  </div>
                  <div className="space-y-1.5">
                    <Label>Date *</Label>
                    <Input name="date" type="date" defaultValue={new Date().toISOString().split("T")[0]} required />
                  </div>
                </div>
                <div className="space-y-1.5">
                  <Label>Notes</Label>
                  <Input name="notes" placeholder="Additional details..." />
                </div>
                <div className="flex justify-end gap-2">
                  <Button type="button" variant="outline" onClick={() => setCreateOpen(false)}>Cancel</Button>
                  <Button type="submit" loading={createMutation.isPending}>Add Expense</Button>
                </div>
              </form>
            </DialogContent>
          </Dialog>
        </div>
      </div>

      {/* Total */}
      <Card>
        <CardContent className="p-4">
          <div className="flex items-center gap-3">
            <Receipt className="h-8 w-8 text-red-500" />
            <div>
              <p className="text-sm text-muted-foreground">Total Expenses</p>
              <p className="text-2xl font-bold text-red-600">
                {formatCurrency(data?.totalAmount ?? 0)}
              </p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Table */}
      <Card>
        <CardHeader className="pb-3">
          <div className="flex flex-col sm:flex-row gap-3">
            <Tabs value={status} onValueChange={setStatus}>
              <TabsList className="h-8">
                {STATUS_TABS.map((s) => (
                  <TabsTrigger key={s} value={s} className="text-xs">{s}</TabsTrigger>
                ))}
              </TabsList>
            </Tabs>
            <div className="relative flex-1 sm:max-w-xs">
              <Search className="absolute left-2.5 top-2 h-4 w-4 text-muted-foreground" />
              <Input
                placeholder="Search expenses..."
                className="pl-8 h-8"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
              />
            </div>
          </div>
        </CardHeader>
        <div>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Description</TableHead>
                <TableHead>Category</TableHead>
                <TableHead>Date</TableHead>
                <TableHead>Amount</TableHead>
                <TableHead>Status</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {isLoading ? (
                [...Array(5)].map((_, i) => (
                  <TableRow key={i}>
                    {[...Array(5)].map((_, j) => (
                      <TableCell key={j}><div className="skeleton h-4 rounded w-20" /></TableCell>
                    ))}
                  </TableRow>
                ))
              ) : expenses.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={5} className="text-center py-10 text-muted-foreground">
                    <Receipt className="h-10 w-10 mx-auto mb-2 opacity-30" />
                    <p>No expenses found</p>
                  </TableCell>
                </TableRow>
              ) : (
                expenses.map((exp: {
                  id: string
                  description: string
                  category?: { name: string; color: string }
                  date: string
                  amount: string | number
                  status: string
                }) => (
                  <TableRow key={exp.id}>
                    <TableCell className="font-medium">{exp.description}</TableCell>
                    <TableCell>
                      {exp.category ? (
                        <Badge variant="outline" style={{ borderColor: exp.category.color, color: exp.category.color }}>
                          {exp.category.name}
                        </Badge>
                      ) : (
                        <span className="text-muted-foreground text-xs">Uncategorized</span>
                      )}
                    </TableCell>
                    <TableCell className="text-muted-foreground">{formatDate(exp.date, "short")}</TableCell>
                    <TableCell className="font-semibold text-red-600">
                      -{formatCurrency(Number(exp.amount))}
                    </TableCell>
                    <TableCell>
                      <Badge className={`text-[10px] border ${getStatusColor(exp.status)}`}>
                        {exp.status}
                      </Badge>
                    </TableCell>
                  </TableRow>
                ))
              )}
            </TableBody>
          </Table>
        </div>
      </Card>
    </div>
  )
}
