import { getAuth } from "@/lib/server-auth"
import { redirect } from "next/navigation"
import { Sidebar } from "@/components/layout/sidebar"
import { Header } from "@/components/layout/header"

export default async function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const { userId } = await getAuth()

  if (!userId) {
    redirect("/sign-in")
  }

  return (
    <div className="flex h-screen overflow-hidden bg-background">
      <Sidebar />
      <div className="flex flex-1 flex-col overflow-hidden pl-64 transition-all duration-300">
        <Header />
        <main className="flex-1 overflow-y-auto">
          <div className="container mx-auto max-w-7xl p-6">
            {children}
          </div>
        </main>
      </div>
    </div>
  )
}
