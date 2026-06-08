import OpenAI from "openai"

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
})

export default openai

// ─── Model Config ────────────────────────────────────────────
export const AI_MODEL = process.env.OPENAI_MODEL ?? "gpt-4o"
export const EMBEDDING_MODEL = process.env.OPENAI_EMBEDDING_MODEL ?? "text-embedding-3-small"

// ─── System Prompt for Financial Assistant ───────────────────
export const FINANCIAL_ASSISTANT_SYSTEM_PROMPT = `You are FinSight AI, an expert financial assistant for small and medium businesses.

CRITICAL RULES:
1. NEVER calculate or invent financial numbers. All financial data will be provided to you in the context.
2. ONLY explain, analyze, and provide insights based on the actual data provided.
3. Always cite the source data when referencing specific figures.
4. If data is not available, clearly state that you don't have that information.
5. Be precise, professional, and actionable in your responses.

YOUR CAPABILITIES:
- Explain financial trends and patterns from provided data
- Identify risks and opportunities based on the data
- Provide recommendations for improving financial health
- Answer questions about specific financial records provided
- Generate summaries and narratives from numerical data
- Suggest questions users might want to ask about their finances

FORMATTING:
- Use clear headings and bullet points when appropriate
- Format currency values consistently
- Provide percentage changes where relevant
- Be concise but comprehensive

IMPORTANT: You are an assistant that helps businesses understand their finances. 
You do NOT have access to any external financial data. Everything you reference 
must come from the context provided in this conversation.`

// ─── Generate Embeddings ─────────────────────────────────────
export async function generateEmbedding(text: string): Promise<number[]> {
  const response = await openai.embeddings.create({
    model: EMBEDDING_MODEL,
    input: text.slice(0, 8000), // Truncate to token limit
  })
  return response.data[0].embedding
}

// ─── Generate AI Response (Streaming) ───────────────────────
export async function* generateStreamingResponse(
  messages: Array<{ role: "user" | "assistant" | "system"; content: string }>,
  systemPrompt = FINANCIAL_ASSISTANT_SYSTEM_PROMPT
): AsyncGenerator<string> {
  const stream = await openai.chat.completions.create({
    model: AI_MODEL,
    messages: [
      { role: "system", content: systemPrompt },
      ...messages,
    ],
    stream: true,
    max_tokens: 2048,
    temperature: 0.3, // Lower temperature for more accurate financial responses
  })

  for await (const chunk of stream) {
    const content = chunk.choices[0]?.delta?.content
    if (content) {
      yield content
    }
  }
}

// ─── Generate AI Response (Non-streaming) ────────────────────
export async function generateResponse(
  messages: Array<{ role: "user" | "assistant" | "system"; content: string }>,
  context: string = "",
  systemPrompt = FINANCIAL_ASSISTANT_SYSTEM_PROMPT
): Promise<{ content: string; tokens: number; cost: number }> {
  const fullSystemPrompt = context
    ? `${systemPrompt}\n\n=== CURRENT FINANCIAL DATA ===\n${context}`
    : systemPrompt

  const response = await openai.chat.completions.create({
    model: AI_MODEL,
    messages: [
      { role: "system", content: fullSystemPrompt },
      ...messages,
    ],
    max_tokens: 2048,
    temperature: 0.3,
  })

  const content = response.choices[0]?.message?.content ?? ""
  const tokens = response.usage?.total_tokens ?? 0
  // Approximate cost calculation for GPT-4o
  const cost = tokens * 0.000015

  return { content, tokens, cost }
}

// ─── Build Financial Context for AI ─────────────────────────
export function buildFinancialContext(data: {
  metrics?: Record<string, unknown>
  trends?: unknown[]
  categories?: unknown[]
  invoices?: unknown[]
  expenses?: unknown[]
  forecasts?: unknown[]
}): string {
  const sections: string[] = []

  if (data.metrics) {
    sections.push(`## Key Financial Metrics\n${JSON.stringify(data.metrics, null, 2)}`)
  }
  if (data.trends && data.trends.length > 0) {
    sections.push(`## Monthly Trends\n${JSON.stringify(data.trends, null, 2)}`)
  }
  if (data.categories && data.categories.length > 0) {
    sections.push(`## Expense Categories\n${JSON.stringify(data.categories, null, 2)}`)
  }
  if (data.invoices && data.invoices.length > 0) {
    sections.push(`## Invoice Summary\n${JSON.stringify(data.invoices, null, 2)}`)
  }
  if (data.expenses && data.expenses.length > 0) {
    sections.push(`## Recent Expenses\n${JSON.stringify(data.expenses, null, 2)}`)
  }
  if (data.forecasts && data.forecasts.length > 0) {
    sections.push(`## Cash Flow Forecasts\n${JSON.stringify(data.forecasts, null, 2)}`)
  }

  return sections.join("\n\n")
}

// ─── Classify User Intent ────────────────────────────────────
export async function classifyUserIntent(
  question: string
): Promise<{
  intent: string
  dataNeeded: string[]
}> {
  const response = await openai.chat.completions.create({
    model: "gpt-4o-mini",
    messages: [
      {
        role: "system",
        content: `Classify the user's financial question and identify what data is needed.
        
Return JSON with:
- intent: one of [profit_query, expense_query, invoice_query, cash_flow_query, trend_query, forecast_query, general_query]
- dataNeeded: array of required data types from [metrics, trends, categories, invoices, expenses, forecasts, transactions]

Example: {"intent": "profit_query", "dataNeeded": ["metrics", "trends"]}`,
      },
      { role: "user", content: question },
    ],
    response_format: { type: "json_object" },
    max_tokens: 200,
  })

  try {
    return JSON.parse(response.choices[0]?.message?.content ?? "{}")
  } catch {
    return { intent: "general_query", dataNeeded: ["metrics"] }
  }
}

// ─── Generate Insight Title ──────────────────────────────────
export async function generateInsightTitle(
  insightType: string,
  data: Record<string, unknown>
): Promise<string> {
  const response = await openai.chat.completions.create({
    model: "gpt-4o-mini",
    messages: [
      {
        role: "system",
        content: "Generate a concise, impactful insight title (max 80 chars) based on the financial data. Be specific with numbers.",
      },
      {
        role: "user",
        content: `Insight type: ${insightType}\nData: ${JSON.stringify(data)}`,
      },
    ],
    max_tokens: 100,
    temperature: 0.5,
  })

  return response.choices[0]?.message?.content?.trim() ?? "Financial Insight"
}
