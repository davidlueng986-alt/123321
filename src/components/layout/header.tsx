"use client"

import { UserButton, OrganizationSwitcher } from "@clerk/nextjs"
import { Bell, Search, Moon, Sun, Menu } from "lucide-react"
import { useTheme } from "next-themes"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { useState } from "react"

interface HeaderProps {
  title?: string
  description?: string
}

export function Header({ title, description }: HeaderProps) {
  const { theme, setTheme } = useTheme()
  const [searchOpen, setSearchOpen] = useState(false)

  return (
    <header className="sticky top-0 z-20 flex h-16 items-center gap-4 border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 px-6">
      {/* Page Title */}
      <div className="flex-1">
        {title && (
          <div>
            <h1 className="text-lg font-semibold">{title}</h1>
            {description && (
              <p className="text-xs text-muted-foreground hidden md:block">{description}</p>
            )}
          </div>
        )}
        {!title && searchOpen && (
          <div className="relative max-w-sm">
            <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
            <Input
              placeholder="Search transactions, invoices..."
              className="pl-8 h-8"
              autoFocus
              onBlur={() => setSearchOpen(false)}
            />
          </div>
        )}
      </div>

      {/* Actions */}
      <div className="flex items-center gap-2">
        {/* Search */}
        {!searchOpen && (
          <Button
            variant="ghost"
            size="icon"
            className="h-8 w-8"
            onClick={() => setSearchOpen(true)}
          >
            <Search className="h-4 w-4" />
          </Button>
        )}

        {/* Theme Toggle */}
        <Button
          variant="ghost"
          size="icon"
          className="h-8 w-8"
          onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
        >
          <Sun className="h-4 w-4 rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
          <Moon className="absolute h-4 w-4 rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />
        </Button>

        {/* Notifications */}
        <Button variant="ghost" size="icon" className="h-8 w-8 relative">
          <Bell className="h-4 w-4" />
          <span className="absolute top-1 right-1 h-2 w-2 bg-red-500 rounded-full" />
        </Button>

        {/* Organization Switcher */}
        <div className="hidden md:block">
          <OrganizationSwitcher
            hidePersonal
            appearance={{
              elements: {
                organizationSwitcherTrigger: "border rounded-md px-3 py-1.5 text-sm h-8",
              },
            }}
          />
        </div>

        {/* User Button */}
        <UserButton
          afterSignOutUrl="/sign-in"
          appearance={{
            elements: {
              avatarBox: "h-8 w-8",
            },
          }}
        />
      </div>
    </header>
  )
}
