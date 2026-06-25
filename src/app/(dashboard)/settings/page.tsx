"use client"

import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Separator } from "@/components/ui/separator"
import { Badge } from "@/components/ui/badge"
import { Shield, Building2, Bell, Users, Key, CheckCircle2 } from "lucide-react"
import { toast } from "sonner"

// Demo user data
const DEMO_USER = {
  fullName: "Demo User",
  firstName: "Demo",
  lastName: "User",
  email: "demo@finsight.ai",
  imageUrl: null,
}

export default function SettingsPage() {
  const handleSave = () => toast.success("Settings saved (demo mode)")

  return (
    <div className="space-y-6 max-w-3xl">
      <div>
        <h1 className="text-2xl font-bold">Settings</h1>
        <p className="text-muted-foreground">Manage your account and organization settings</p>
      </div>

      {/* Demo Mode Banner */}
      <div className="rounded-xl border border-amber-200 bg-amber-50 p-4 flex items-start gap-3">
        <CheckCircle2 className="h-5 w-5 text-amber-600 shrink-0 mt-0.5" />
        <div>
          <p className="text-sm font-medium text-amber-800">Running in Demo Mode</p>
          <p className="text-xs text-amber-700 mt-0.5">
            Settings changes are shown for UI demonstration purposes. In production, changes would be saved to the database and Clerk would handle authentication.
          </p>
        </div>
      </div>

      {/* Profile */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Users className="h-5 w-5" />
            Profile
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex items-center gap-4">
            <div className="h-16 w-16 rounded-full bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center text-white font-bold text-xl">
              D
            </div>
            <div>
              <p className="font-semibold">{DEMO_USER.fullName}</p>
              <p className="text-sm text-muted-foreground">{DEMO_USER.email}</p>
              <Badge className="mt-1 text-[10px] bg-blue-100 text-blue-700">Admin</Badge>
            </div>
          </div>
          <Separator />
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-1.5">
              <Label>First Name</Label>
              <Input defaultValue={DEMO_USER.firstName} />
            </div>
            <div className="space-y-1.5">
              <Label>Last Name</Label>
              <Input defaultValue={DEMO_USER.lastName} />
            </div>
          </div>
          <div className="space-y-1.5">
            <Label>Email</Label>
            <Input defaultValue={DEMO_USER.email} type="email" />
          </div>
          <Button size="sm" onClick={handleSave}>Save Changes</Button>
        </CardContent>
      </Card>

      {/* Organization */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Building2 className="h-5 w-5" />
            Organization
          </CardTitle>
          <CardDescription>Configure your business settings</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-1.5">
            <Label>Business Name</Label>
            <Input defaultValue="My Business" />
          </div>
          <div className="space-y-1.5">
            <Label>Industry</Label>
            <Input defaultValue="Technology Services" placeholder="e.g. Technology, Retail, Healthcare" />
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-1.5">
              <Label>Currency</Label>
              <Select defaultValue="USD">
                <SelectTrigger><SelectValue /></SelectTrigger>
                <SelectContent>
                  <SelectItem value="USD">USD - US Dollar</SelectItem>
                  <SelectItem value="EUR">EUR - Euro</SelectItem>
                  <SelectItem value="GBP">GBP - British Pound</SelectItem>
                  <SelectItem value="CAD">CAD - Canadian Dollar</SelectItem>
                  <SelectItem value="AUD">AUD - Australian Dollar</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div className="space-y-1.5">
              <Label>Fiscal Year Start</Label>
              <Select defaultValue="1">
                <SelectTrigger><SelectValue /></SelectTrigger>
                <SelectContent>
                  {["January", "February", "March", "April", "May", "June",
                    "July", "August", "September", "October", "November", "December"]
                    .map((m, i) => (
                      <SelectItem key={m} value={String(i + 1)}>{m}</SelectItem>
                    ))}
                </SelectContent>
              </Select>
            </div>
          </div>
          <div className="space-y-1.5">
            <Label>Timezone</Label>
            <Select defaultValue="UTC">
              <SelectTrigger><SelectValue /></SelectTrigger>
              <SelectContent>
                <SelectItem value="UTC">UTC</SelectItem>
                <SelectItem value="America/New_York">Eastern Time (ET)</SelectItem>
                <SelectItem value="America/Chicago">Central Time (CT)</SelectItem>
                <SelectItem value="America/Los_Angeles">Pacific Time (PT)</SelectItem>
                <SelectItem value="Europe/London">London (GMT)</SelectItem>
                <SelectItem value="Europe/Paris">Paris (CET)</SelectItem>
                <SelectItem value="Asia/Tokyo">Tokyo (JST)</SelectItem>
              </SelectContent>
            </Select>
          </div>
          <Button size="sm" onClick={handleSave}>Save Organization</Button>
        </CardContent>
      </Card>

      {/* Security */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Shield className="h-5 w-5" />
            Security
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium">Multi-Factor Authentication</p>
              <p className="text-xs text-muted-foreground">Add an extra layer of security</p>
            </div>
            <Badge className="bg-emerald-100 text-emerald-700 text-[10px]">Enabled in Production</Badge>
          </div>
          <Separator />
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium">RBAC Roles</p>
              <p className="text-xs text-muted-foreground">Admin, Accountant, Employee, Viewer</p>
            </div>
            <Badge className="bg-blue-100 text-blue-700 text-[10px]">4 Roles Available</Badge>
          </div>
          <Separator />
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium">Audit Logging</p>
              <p className="text-xs text-muted-foreground">All CRUD operations are logged</p>
            </div>
            <Badge className="bg-emerald-100 text-emerald-700 text-[10px]">Active</Badge>
          </div>
          <Separator />
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium">Rate Limiting</p>
              <p className="text-xs text-muted-foreground">100 requests per minute per IP</p>
            </div>
            <Badge className="bg-emerald-100 text-emerald-700 text-[10px]">Active</Badge>
          </div>
        </CardContent>
      </Card>

      {/* API Keys */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Key className="h-5 w-5" />
            API & Integrations
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          {[
            { name: "PostgreSQL Database", status: "Connected", color: "text-emerald-600" },
            { name: "OpenAI API (GPT-4o)", status: "Demo fallback active", color: "text-amber-600" },
            { name: "Clerk Authentication", status: "Demo mode active", color: "text-amber-600" },
            { name: "AWS S3 Storage", status: "Not configured", color: "text-gray-500" },
            { name: "Qdrant Vector DB", status: "Not configured", color: "text-gray-500" },
          ].map((item) => (
            <div key={item.name} className="flex items-center justify-between py-1">
              <p className="text-sm">{item.name}</p>
              <span className={`text-xs font-medium ${item.color}`}>{item.status}</span>
            </div>
          ))}
        </CardContent>
      </Card>

      {/* Notifications */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Bell className="h-5 w-5" />
            Notifications
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {[
              "Overdue invoice alerts",
              "Cash flow warnings",
              "Unusual expense detection",
              "Payment received confirmations",
              "Monthly financial summary",
              "AI insight notifications",
            ].map((item) => (
              <div key={item} className="flex items-center justify-between">
                <p className="text-sm">{item}</p>
                <input type="checkbox" defaultChecked className="rounded" />
              </div>
            ))}
          </div>
          <Button size="sm" className="mt-4" onClick={handleSave}>Save Preferences</Button>
        </CardContent>
      </Card>
    </div>
  )
}
