import type { Metadata, Viewport } from "next"
import { Inter } from "next/font/google"
import { ThemeProvider } from "@/components/shared/theme-provider"
import { QueryProvider } from "@/components/shared/query-provider"
import { Toaster } from "sonner"
import "./globals.css"

const inter = Inter({
  subsets: ["latin"],
  display: "swap",
  variable: "--font-inter",
})

export const metadata: Metadata = {
  title: {
    default: "FinSight AI - AI Financial Assistant for SMEs",
    template: "%s | FinSight AI",
  },
  description:
    "AI-powered financial intelligence platform for small and medium businesses. Track expenses, manage invoices, analyze cash flow, and get AI-driven insights.",
  keywords: [
    "financial assistant",
    "AI accounting",
    "SME finance",
    "invoice management",
    "expense tracking",
    "cash flow",
    "financial dashboard",
  ],
  authors: [{ name: "FinSight AI" }],
  creator: "FinSight AI",
  metadataBase: new URL(process.env.NEXT_PUBLIC_APP_URL ?? "http://localhost:3000"),
  openGraph: {
    type: "website",
    locale: "en_US",
    url: "/",
    title: "FinSight AI - AI Financial Assistant for SMEs",
    description: "AI-powered financial intelligence platform for SMEs",
    siteName: "FinSight AI",
  },
  twitter: {
    card: "summary_large_image",
    title: "FinSight AI",
    description: "AI-powered financial intelligence platform for SMEs",
  },
  robots: {
    index: true,
    follow: true,
  },
}

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
  themeColor: [
    { media: "(prefers-color-scheme: light)", color: "#ffffff" },
    { media: "(prefers-color-scheme: dark)", color: "#0f172a" },
  ],
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" suppressHydrationWarning className={inter.variable}>
      <body className={`${inter.className} antialiased`}>
        <ThemeProvider
          attribute="class"
          defaultTheme="light"
          enableSystem
          disableTransitionOnChange
        >
          <QueryProvider>
            {children}
            <Toaster
              position="top-right"
              richColors
              expand
              visibleToasts={3}
            />
          </QueryProvider>
        </ThemeProvider>
      </body>
    </html>
  )
}
