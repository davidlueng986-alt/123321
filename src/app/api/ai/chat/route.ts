import { auth } from "@clerk/nextjs/server"
import { NextRequest } from "next/server"
import { prisma } from "@/lib/prisma"
import { apiError, rateLimit } from "@/lib/rate-limit"
import { chatMessageSchema } from "@/lib/validations"
import {
  generateStreamingResponse,
  buildFinancialContext,
  classifyUserIntent,
  FINANCIAL_ASSISTANT_SYSTEM_PROMPT,
} from "@/lib/openai"
import {
  getDashboardMetrics,
  getMonthlyTrends,
  getExpensesByCategory,
  generateCashFlowForecast,
  getInvoiceStatistics,
  getTopClients,
} from "@/lib/financial-calculations"

const checkRateLimit = rateLimit({ limit: 20, windowMs: 60000 })

async function getOrg(userId: string, orgId: string | null) {
  return orgId
    ? await prisma.organization.findUnique({ where: { clerkOrgId: orgId } })
    : await prisma.organization.findFirst({ where: { clerkOrgId: `personal_${userId}` } })
}

export async function POST(request: NextRequest) {
  const rateLimitResponse = checkRateLimit(request)
  if (rateLimitResponse) return rateLimitResponse

  try {
    const { userId, orgId } = await auth()
    if (!userId) return apiError("Unauthorized", 401)

    const org = await getOrg(userId, orgId ?? null)
    if (!org) return apiError("Organization not found", 404)

    const user = await prisma.user.findUnique({ where: { clerkId: userId } })
    if (!user) return apiError("User not found", 404)

    const body = await request.json()
    const parsed = chatMessageSchema.safeParse(body)
    if (!parsed.success) {
      return apiError("Invalid message", 400)
    }

    const { message, chatId } = parsed.data

    // Get or create chat
    let chat
    if (chatId) {
      chat = await prisma.aIChat.findFirst({
        where: { id: chatId, organizationId: org.id, userId: user.id },
        include: { messages: { orderBy: { createdAt: "asc" }, take: 20 } },
      })
    }

    if (!chat) {
      chat = await prisma.aIChat.create({
        data: {
          organizationId: org.id,
          userId: user.id,
          title: message.slice(0, 100),
        },
        include: { messages: true },
      })
    }

    // Classify intent to know what data to retrieve
    let intent: { intent: string; dataNeeded: string[] }
    try {
      intent = await classifyUserIntent(message)
    } catch {
      intent = { intent: "general_query", dataNeeded: ["metrics"] }
    }

    // Fetch required financial data (deterministic calculations only)
    const financialData: Record<string, unknown> = {}

    await Promise.all([
      intent.dataNeeded.includes("metrics") &&
        getDashboardMetrics(org.id).then((m) => { financialData.metrics = m }),
      intent.dataNeeded.includes("trends") &&
        getMonthlyTrends(org.id, 6).then((t) => { financialData.trends = t }),
      intent.dataNeeded.includes("categories") &&
        getExpensesByCategory(org.id).then((c) => { financialData.categories = c }),
      intent.dataNeeded.includes("invoices") &&
        getInvoiceStatistics(org.id).then((i) => { financialData.invoices = i }),
      intent.dataNeeded.includes("forecasts") &&
        generateCashFlowForecast(org.id, 3).then((f) => { financialData.forecasts = f }),
    ])

    // Build context from financial data
    const context = buildFinancialContext({
      metrics: financialData.metrics as Record<string, unknown>,
      trends: financialData.trends as unknown[],
      categories: financialData.categories as unknown[],
      invoices: financialData.invoices ? [financialData.invoices] : undefined,
      forecasts: financialData.forecasts as unknown[],
    })

    // Save user message
    await prisma.aIChatMessage.create({
      data: {
        chatId: chat.id,
        role: "user",
        content: message,
      },
    })

    // Build message history for context
    const messageHistory = (chat.messages ?? []).slice(-10).map((m) => ({
      role: m.role as "user" | "assistant",
      content: m.content,
    }))

    // Add current message
    messageHistory.push({ role: "user", content: message })

    // System prompt with context
    const systemWithContext = context
      ? `${FINANCIAL_ASSISTANT_SYSTEM_PROMPT}\n\n=== REAL-TIME FINANCIAL DATA ===\n${context}\n\n=== IMPORTANT ===\nAll numbers above are actual calculated values from the database. Reference them precisely when answering.`
      : FINANCIAL_ASSISTANT_SYSTEM_PROMPT

    // Stream the response
    const encoder = new TextEncoder()
    let fullResponse = ""

    const stream = new ReadableStream({
      async start(controller) {
        try {
          // Send chat ID first
          controller.enqueue(
            encoder.encode(`data: ${JSON.stringify({ type: "meta", chatId: chat.id })}\n\n`)
          )

          for await (const chunk of generateStreamingResponse(
            messageHistory,
            systemWithContext
          )) {
            fullResponse += chunk
            controller.enqueue(
              encoder.encode(`data: ${JSON.stringify({ type: "chunk", content: chunk })}\n\n`)
            )
          }

          // Save AI response to DB
          await prisma.aIChatMessage.create({
            data: {
              chatId: chat.id,
              role: "assistant",
              content: fullResponse,
              citations: financialData as object,
            },
          })

          controller.enqueue(
            encoder.encode(`data: ${JSON.stringify({ type: "done", chatId: chat.id })}\n\n`)
          )
          controller.close()
        } catch (streamError) {
          console.error("Streaming error:", streamError)
          // Fallback response when AI is not available
          const fallbackMsg = `I'm sorry, I couldn't process your question right now. Based on your financial data:\n\n${
            financialData.metrics
              ? `- Revenue: ${JSON.stringify((financialData.metrics as Record<string, unknown>).revenue)}\n- Expenses: ${JSON.stringify((financialData.metrics as Record<string, unknown>).expenses)}\n- Profit: ${JSON.stringify((financialData.metrics as Record<string, unknown>).profit)}`
              : "Financial data is being loaded."
          }\n\nPlease try again in a moment.`

          controller.enqueue(
            encoder.encode(`data: ${JSON.stringify({ type: "chunk", content: fallbackMsg })}\n\n`)
          )
          controller.enqueue(
            encoder.encode(`data: ${JSON.stringify({ type: "done", chatId: chat.id })}\n\n`)
          )
          controller.close()
        }
      },
    })

    return new Response(stream, {
      headers: {
        "Content-Type": "text/event-stream",
        "Cache-Control": "no-cache",
        Connection: "keep-alive",
        "X-Accel-Buffering": "no",
      },
    })
  } catch (error) {
    console.error("AI Chat error:", error)
    return apiError("Failed to process message", 500)
  }
}

// GET /api/ai/chat - Get chat history
export async function GET(request: NextRequest) {
  try {
    const { userId, orgId } = await auth()
    if (!userId) return apiError("Unauthorized", 401)

    const org = await getOrg(userId, orgId ?? null)
    if (!org) return apiError("Organization not found", 404)

    const user = await prisma.user.findUnique({ where: { clerkId: userId } })
    if (!user) return apiError("User not found", 404)

    const chatId = request.nextUrl.searchParams.get("chatId")

    if (chatId) {
      const chat = await prisma.aIChat.findFirst({
        where: { id: chatId, organizationId: org.id, userId: user.id },
        include: {
          messages: { orderBy: { createdAt: "asc" } },
        },
      })
      return Response.json({ success: true, data: chat })
    }

    const chats = await prisma.aIChat.findMany({
      where: { organizationId: org.id, userId: user.id, isActive: true },
      orderBy: { updatedAt: "desc" },
      take: 20,
      select: {
        id: true,
        title: true,
        createdAt: true,
        updatedAt: true,
        _count: { select: { messages: true } },
      },
    })

    return Response.json({ success: true, data: chats })
  } catch (error) {
    return apiError("Failed to fetch chats", 500)
  }
}
