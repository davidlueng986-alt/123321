"use client"

import { useState } from "react"
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query"
import axios from "axios"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Badge } from "@/components/ui/badge"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs"
import {
  Table, TableBody, TableCell, TableHead, TableHeader, TableRow,
} from "@/components/ui/table"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { formatCurrency, formatDate, getStatusColor, generateInvoiceNumber } from "@/lib/utils"
import { Plus, Search, FileText, Send, DollarSign, Clock, AlertTriangle, Eye } from "lucide-react"
import { toast } from "sonner"

const STATUS_TABS = ["ALL", "DRAFT", "SENT", "PAID", "OVERDUE", "PARTIAL"]

export default function InvoicesPage() {
  const [status, setStatus] = useState("ALL")
  const [search, setSearch] = useState("")
  const [createOpen, setCreateOpen] = useState(false)
  const qc = useQueryClient()

  const { data, isLoading } = useQuery({
    queryKey: ["invoices", status, search],
    queryFn: async () => {
      const params = new URLSearchParams()
      if (status !== "ALL") params.set("status", status)
      if (search) params.set("search", search)
      const res = await axios.get(`/api/invoices?${params}`)
      return res.data.data
    },
  })

  const createMutation = useMutation({
    mutationFn: (data: Record<string, unknown>) => axios.post("/api/invoices", data),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["invoices"] })
      qc.invalidateQueries({ queryKey: ["dashboard-metrics"] })
      setCreateOpen(false)
      toast.success("Invoice created successfully")
    },
    onError: () => toast.error("Failed to create invoice"),
  })

  const sendMutation = useMutation({
    mutationFn: (id: string) => axios.patch(`/api/invoices/${id}`, { _action: "send" }),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["invoices"] })
      toast.success("Invoice marked as sent")
    },
    onError: () => toast.error("Failed to update invoice"),
  })

  const handleCreateInvoice = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    const form = e.currentTarget
    const fd = new FormData(form)

    const amount = parseFloat(fd.get("unitPrice") as string)
    const qty = parseFloat(fd.get("quantity") as string)

    createMutation.mutate({
      invoiceNumber: fd.get("invoiceNumber"),
      issueDate: fd.get("issueDate"),
      dueDate: fd.get("dueDate"),
      currency: "USD",
      notes: fd.get("notes"),
      taxRate: parseFloat(fd.get("taxRate") as string) || 0,
      items: [{
        description: fd.get("itemDescription"),
        quantity: qty,
        unitPrice: amount,
        taxRate: parseFloat(fd.get("taxRate") as string) || 0,
      }],
    })
  }

  const invoices = data?.invoices ?? []
  const stats = {
    total: data?.total ?? 0,
    draft: invoices.filter((i: { status: string }) => i.status === "DRAFT").length,
    overdue: invoices.filter((i: { status: string }) => i.status === "OVERDUE").length,
    paid: invoices.filter((i: { status: string }) => i.status === "PAID").length,
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Invoices</h1>
          <p className="text-muted-foreground">Create, send, and track your invoices</p>
        </div>
        <Dialog open={createOpen} onOpenChange={setCreateOpen}>
          <DialogTrigger asChild>
            <Button>
              <Plus className="h-4 w-4 mr-1.5" />
              New Invoice
            </Button>
          </DialogTrigger>
          <DialogContent className="max-w-2xl">
            <DialogHeader>
              <DialogTitle>Create Invoice</DialogTitle>
            </DialogHeader>
            <form onSubmit={handleCreateInvoice} className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-1.5">
                  <Label>Invoice Number</Label>
                  <Input
                    name="invoiceNumber"
                    defaultValue={generateInvoiceNumber()}
                    required
                  />
                </div>
                <div className="space-y-1.5">
                  <Label>Tax Rate (%)</Label>
                  <Input name="taxRate" type="number" min="0" max="100" defaultValue="0" />
                </div>
                <div className="space-y-1.5">
                  <Label>Issue Date</Label>
                  <Input
                    name="issueDate"
                    type="date"
                    defaultValue={new Date().toISOString().split("T")[0]}
                    required
                  />
                </div>
                <div className="space-y-1.5">
                  <Label>Due Date</Label>
                  <Input
                    name="dueDate"
                    type="date"
                    defaultValue={new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString().split("T")[0]}
                    required
                  />
                </div>
              </div>

              <div className="border rounded-lg p-4 space-y-3">
                <p className="text-sm font-medium">Line Item</p>
                <div className="space-y-1.5">
                  <Label>Description</Label>
                  <Input name="itemDescription" placeholder="Service description" required />
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-1.5">
                    <Label>Quantity</Label>
                    <Input name="quantity" type="number" min="0.01" step="0.01" defaultValue="1" required />
                  </div>
                  <div className="space-y-1.5">
                    <Label>Unit Price ($)</Label>
                    <Input name="unitPrice" type="number" min="0" step="0.01" placeholder="0.00" required />
                  </div>
                </div>
              </div>

              <div className="space-y-1.5">
                <Label>Notes</Label>
                <Textarea name="notes" placeholder="Payment terms or additional notes..." rows={3} />
              </div>

              <div className="flex justify-end gap-2">
                <Button type="button" variant="outline" onClick={() => setCreateOpen(false)}>
                  Cancel
                </Button>
                <Button type="submit" loading={createMutation.isPending}>
                  Create Invoice
                </Button>
              </div>
            </form>
          </DialogContent>
        </Dialog>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {[
          { label: "Total Invoices", value: stats.total, icon: FileText, color: "text-blue-600" },
          { label: "Draft", value: stats.draft, icon: Clock, color: "text-gray-600" },
          { label: "Overdue", value: stats.overdue, icon: AlertTriangle, color: "text-red-600" },
          { label: "Paid", value: stats.paid, icon: DollarSign, color: "text-emerald-600" },
        ].map((s) => (
          <Card key={s.label}>
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-xs text-muted-foreground">{s.label}</p>
                  <p className={`text-2xl font-bold ${s.color}`}>{s.value}</p>
                </div>
                <s.icon className={`h-6 w-6 ${s.color} opacity-70`} />
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Filters */}
      <Card>
        <CardHeader className="pb-3">
          <div className="flex flex-col sm:flex-row gap-3">
            <Tabs value={status} onValueChange={setStatus} className="flex-1">
              <TabsList className="h-8">
                {STATUS_TABS.map((s) => (
                  <TabsTrigger key={s} value={s} className="text-xs px-2">
                    {s}
                  </TabsTrigger>
                ))}
              </TabsList>
            </Tabs>
            <div className="relative w-full sm:w-64">
              <Search className="absolute left-2.5 top-2 h-4 w-4 text-muted-foreground" />
              <Input
                placeholder="Search invoices..."
                className="pl-8 h-8"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
              />
            </div>
          </div>
        </CardHeader>
        <CardContent className="p-0">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Invoice #</TableHead>
                <TableHead>Client</TableHead>
                <TableHead>Issue Date</TableHead>
                <TableHead>Due Date</TableHead>
                <TableHead>Amount</TableHead>
                <TableHead>Status</TableHead>
                <TableHead className="text-right">Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {isLoading ? (
                [...Array(5)].map((_, i) => (
                  <TableRow key={i}>
                    {[...Array(7)].map((_, j) => (
                      <TableCell key={j}>
                        <div className="skeleton h-4 rounded w-24" />
                      </TableCell>
                    ))}
                  </TableRow>
                ))
              ) : invoices.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={7} className="text-center py-12 text-muted-foreground">
                    <FileText className="h-10 w-10 mx-auto mb-3 opacity-30" />
                    <p className="font-medium">No invoices found</p>
                    <p className="text-sm mt-1">Create your first invoice to get started</p>
                  </TableCell>
                </TableRow>
              ) : (
                invoices.map((inv: {
                  id: string
                  invoiceNumber: string
                  client?: { name: string }
                  issueDate: string
                  dueDate: string
                  total: string | number
                  amountDue: string | number
                  status: string
                }) => (
                  <TableRow key={inv.id}>
                    <TableCell className="font-mono text-sm font-medium">{inv.invoiceNumber}</TableCell>
                    <TableCell>{inv.client?.name ?? "—"}</TableCell>
                    <TableCell className="text-muted-foreground">{formatDate(inv.issueDate, "short")}</TableCell>
                    <TableCell className="text-muted-foreground">{formatDate(inv.dueDate, "short")}</TableCell>
                    <TableCell className="font-medium">{formatCurrency(Number(inv.total))}</TableCell>
                    <TableCell>
                      <Badge className={`text-[10px] border ${getStatusColor(inv.status)}`}>
                        {inv.status}
                      </Badge>
                    </TableCell>
                    <TableCell className="text-right">
                      <div className="flex items-center justify-end gap-1">
                        {inv.status === "DRAFT" && (
                          <Button
                            size="sm"
                            variant="ghost"
                            className="h-7 text-xs"
                            onClick={() => sendMutation.mutate(inv.id)}
                          >
                            <Send className="h-3 w-3 mr-1" />
                            Send
                          </Button>
                        )}
                        <Button size="sm" variant="ghost" className="h-7 text-xs">
                          <Eye className="h-3 w-3" />
                        </Button>
                      </div>
                    </TableCell>
                  </TableRow>
                ))
              )}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  )
}
