"use client"

import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Separator } from "@/components/ui/separator"
import { Badge } from "@/components/ui/badge"
import { useUser, useOrganization } from "@clerk/nextjs"
import { Shield, Building2, Bell, CreditCard, Users, Key } from "lucide-react"

export default function SettingsPage() {
  const { user } = useUser()
  const { organization } = useOrganization()

  return (
    <div className="space-y-6 max-w-3xl">
      <div>
        <h1 className="text-2xl font-bold">Settings</h1>
        <p className="text-muted-foreground">Manage your account and organization settings</p>
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
            {user?.imageUrl && (
              <img src={user.imageUrl} alt="Avatar" className="h-16 w-16 rounded-full object-cover" />
            )}
            <div>
              <p className="font-semibold">{user?.fullName}</p>
              <p className="text-sm text-muted-foreground">{user?.primaryEmailAddress?.emailAddress}</p>
              <Badge className="mt-1 text-[10px]">Admin</Badge>
            </div>
          </div>
          <Separator />
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-1.5">
              <Label>First Name</Label>
              <Input defaultValue={user?.firstName ?? ""} />
            </div>
            <div className="space-y-1.5">
              <Label>Last Name</Label>
              <Input defaultValue={user?.lastName ?? ""} />
            </div>
          </div>
          <Button size="sm">Save Changes</Button>
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
            <Input defaultValue={organization?.name ?? "My Business"} />
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
          <Button size="sm">Save Organization</Button>
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
            <Badge className="bg-emerald-100 text-emerald-700 text-[10px]">Enabled via Clerk</Badge>
          </div>
          <Separator />
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium">Session Management</p>
              <p className="text-xs text-muted-foreground">Manage active sessions</p>
            </div>
            <Button variant="outline" size="sm">Manage Sessions</Button>
          </div>
          <Separator />
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium">Audit Logs</p>
              <p className="text-xs text-muted-foreground">View all account activity</p>
            </div>
            <Button variant="outline" size="sm">View Logs</Button>
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
            { name: "OpenAI API", status: "Configured", color: "text-emerald-600" },
            { name: "Clerk Auth", status: "Active", color: "text-emerald-600" },
            { name: "AWS S3", status: "Not configured", color: "text-amber-600" },
            { name: "Qdrant Vector DB", status: "Not configured", color: "text-amber-600" },
          ].map((item) => (
            <div key={item.name} className="flex items-center justify-between">
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
            ].map((item) => (
              <div key={item} className="flex items-center justify-between">
                <p className="text-sm">{item}</p>
                <input type="checkbox" defaultChecked className="rounded" />
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
