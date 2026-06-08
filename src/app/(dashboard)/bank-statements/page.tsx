"use client"

import { useState, useRef } from "react"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { formatCurrency, formatDate } from "@/lib/utils"
import { Upload, FileText, CheckCircle, AlertCircle, Building2, TrendingUp } from "lucide-react"
import { toast } from "sonner"

const DEMO_STATEMENTS = [
  {
    id: "1",
    fileName: "bank-statement-oct-2024.pdf",
    bankName: "Chase Business",
    statementFrom: new Date("2024-10-01"),
    statementTo: new Date("2024-10-31"),
    totalCredits: 23500,
    totalDebits: 18200,
    transactionCount: 47,
    isProcessed: true,
  },
  {
    id: "2",
    fileName: "bank-statement-sep-2024.csv",
    bankName: "Chase Business",
    statementFrom: new Date("2024-09-01"),
    statementTo: new Date("2024-09-30"),
    totalCredits: 19800,
    totalDebits: 15600,
    transactionCount: 38,
    isProcessed: true,
  },
]

export default function BankStatementsPage() {
  const [isDragging, setIsDragging] = useState(false)
  const [isUploading, setIsUploading] = useState(false)
  const fileInputRef = useRef<HTMLInputElement>(null)

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(false)
    const files = e.dataTransfer.files
    if (files.length > 0) handleFiles(files)
  }

  const handleFiles = async (files: FileList) => {
    const file = files[0]
    const allowedTypes = ["application/pdf", "text/csv", "application/vnd.ms-excel",
      "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"]

    if (!allowedTypes.includes(file.type)) {
      toast.error("Please upload PDF, CSV, or Excel files only")
      return
    }

    if (file.size > 10 * 1024 * 1024) {
      toast.error("File size must be less than 10MB")
      return
    }

    setIsUploading(true)
    try {
      await new Promise(resolve => setTimeout(resolve, 2000))
      toast.success(`${file.name} uploaded successfully. Processing transactions...`)
    } catch {
      toast.error("Upload failed. Please try again.")
    } finally {
      setIsUploading(false)
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold">Bank Statement Analyzer</h1>
        <p className="text-muted-foreground">
          Upload bank statements to extract and categorize transactions automatically
        </p>
      </div>

      {/* Upload Area */}
      <Card>
        <CardContent className="p-6">
          <div
            className={`border-2 border-dashed rounded-xl p-10 text-center cursor-pointer transition-colors ${
              isDragging
                ? "border-primary bg-primary/5"
                : "border-border hover:border-primary/50 hover:bg-accent/50"
            }`}
            onDragOver={(e) => { e.preventDefault(); setIsDragging(true) }}
            onDragLeave={() => setIsDragging(false)}
            onDrop={handleDrop}
            onClick={() => fileInputRef.current?.click()}
          >
            <input
              ref={fileInputRef}
              type="file"
              accept=".pdf,.csv,.xlsx,.xls"
              className="hidden"
              onChange={(e) => e.target.files && handleFiles(e.target.files)}
            />
            <div className="flex flex-col items-center gap-3">
              {isUploading ? (
                <div className="h-12 w-12 rounded-full border-4 border-primary border-t-transparent animate-spin" />
              ) : (
                <Upload className={`h-12 w-12 ${isDragging ? "text-primary" : "text-muted-foreground"}`} />
              )}
              <div>
                <p className="font-semibold text-lg">
                  {isUploading ? "Processing..." : "Drop your bank statement here"}
                </p>
                <p className="text-sm text-muted-foreground mt-1">
                  Supports PDF, CSV, and Excel formats (max 10MB)
                </p>
              </div>
              <Button variant="outline" disabled={isUploading}>
                Browse Files
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Features */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {[
          {
            icon: FileText,
            title: "Auto-Extract Transactions",
            description: "Automatically parse and extract all transactions from uploaded statements",
          },
          {
            icon: Building2,
            title: "Smart Categorization",
            description: "AI-assisted categorization with deterministic rule-based classification",
          },
          {
            icon: TrendingUp,
            title: "Anomaly Detection",
            description: "Statistical analysis to detect unusual transactions and duplicates",
          },
        ].map((f) => (
          <Card key={f.title}>
            <CardContent className="p-4">
              <div className="flex items-start gap-3">
                <f.icon className="h-5 w-5 text-primary mt-0.5 shrink-0" />
                <div>
                  <p className="font-medium text-sm">{f.title}</p>
                  <p className="text-xs text-muted-foreground mt-1">{f.description}</p>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Statement History */}
      <Card>
        <CardHeader>
          <CardTitle>Uploaded Statements</CardTitle>
          <CardDescription>Previously analyzed bank statements</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {DEMO_STATEMENTS.map((stmt) => (
              <div key={stmt.id} className="border rounded-lg p-4">
                <div className="flex items-start justify-between">
                  <div className="flex items-start gap-3">
                    <div className="h-10 w-10 rounded-lg bg-blue-100 flex items-center justify-center shrink-0">
                      <FileText className="h-5 w-5 text-blue-600" />
                    </div>
                    <div>
                      <p className="font-medium text-sm">{stmt.fileName}</p>
                      <p className="text-xs text-muted-foreground">
                        {stmt.bankName} · {formatDate(stmt.statementFrom, "short")} – {formatDate(stmt.statementTo, "short")}
                      </p>
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    {stmt.isProcessed ? (
                      <Badge className="text-[10px] bg-emerald-100 text-emerald-700">
                        <CheckCircle className="h-3 w-3 mr-1" />
                        Processed
                      </Badge>
                    ) : (
                      <Badge className="text-[10px] bg-amber-100 text-amber-700">
                        <AlertCircle className="h-3 w-3 mr-1" />
                        Processing
                      </Badge>
                    )}
                  </div>
                </div>

                <div className="grid grid-cols-3 gap-4 mt-3 pt-3 border-t">
                  <div>
                    <p className="text-xs text-muted-foreground">Credits</p>
                    <p className="text-sm font-semibold text-emerald-600">{formatCurrency(stmt.totalCredits)}</p>
                  </div>
                  <div>
                    <p className="text-xs text-muted-foreground">Debits</p>
                    <p className="text-sm font-semibold text-red-600">{formatCurrency(stmt.totalDebits)}</p>
                  </div>
                  <div>
                    <p className="text-xs text-muted-foreground">Transactions</p>
                    <p className="text-sm font-semibold">{stmt.transactionCount}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
