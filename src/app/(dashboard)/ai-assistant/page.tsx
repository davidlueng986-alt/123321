"use client"

import { useState, useRef, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Avatar, AvatarFallback } from "@/components/ui/avatar"
import { Separator } from "@/components/ui/separator"
import { Bot, Send, User, Lightbulb, RefreshCw, TrendingUp, FileText, DollarSign, AlertTriangle } from "lucide-react"
import { cn } from "@/lib/utils"
import ReactMarkdown from "react-markdown"

interface Message {
  id: string
  role: "user" | "assistant"
  content: string
  timestamp: Date
  isStreaming?: boolean
}

const SUGGESTED_QUESTIONS = [
  "How much profit did I make last month?",
  "Which expense category increased the most?",
  "Which clients have overdue invoices?",
  "Predict my cash flow for next month",
  "What are my top 3 revenue sources?",
  "Are there any unusual expenses this period?",
  "What is my current profit margin?",
  "Give me a financial health summary",
]

const QUICK_TOPICS = [
  { icon: TrendingUp, label: "Revenue Analysis", question: "Analyze my revenue trends" },
  { icon: DollarSign, label: "Profit Overview", question: "What is my current profit and loss situation?" },
  { icon: FileText, label: "Invoice Status", question: "Summarize my invoice and payment status" },
  { icon: AlertTriangle, label: "Risk Assessment", question: "What financial risks should I be aware of?" },
]

export default function AIAssistantPage() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "welcome",
      role: "assistant",
      content: `# Welcome to FinSight AI Assistant 🤖

I'm your AI financial analyst. I can help you understand your business finances, analyze trends, and answer questions about your financial data.

**What I can do:**
- Analyze your revenue, expenses, and profit
- Explain financial trends and patterns
- Identify risks and opportunities
- Answer questions about specific transactions or invoices
- Generate cash flow insights

**Important:** All financial calculations are performed by our secure backend. I only explain and analyze the actual data from your books.

What would you like to know about your finances?`,
      timestamp: new Date(),
    },
  ])
  const [input, setInput] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const [chatId, setChatId] = useState<string | null>(null)
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const textareaRef = useRef<HTMLTextAreaElement>(null)

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages])

  const sendMessage = async (messageText?: string) => {
    const text = messageText ?? input.trim()
    if (!text || isLoading) return

    setInput("")
    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content: text,
      timestamp: new Date(),
    }

    const aiMessage: Message = {
      id: (Date.now() + 1).toString(),
      role: "assistant",
      content: "",
      timestamp: new Date(),
      isStreaming: true,
    }

    setMessages((prev) => [...prev, userMessage, aiMessage])
    setIsLoading(true)

    try {
      const response = await fetch("/api/ai/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: text, chatId }),
      })

      if (!response.ok) throw new Error("Failed to get response")

      const reader = response.body?.getReader()
      const decoder = new TextDecoder()
      let accumulatedContent = ""

      while (reader) {
        const { done, value } = await reader.read()
        if (done) break

        const chunk = decoder.decode(value, { stream: true })
        const lines = chunk.split("\n")

        for (const line of lines) {
          if (line.startsWith("data: ")) {
            try {
              const data = JSON.parse(line.slice(6))

              if (data.type === "meta") {
                setChatId(data.chatId)
              } else if (data.type === "chunk") {
                accumulatedContent += data.content
                setMessages((prev) =>
                  prev.map((m) =>
                    m.id === aiMessage.id
                      ? { ...m, content: accumulatedContent }
                      : m
                  )
                )
              } else if (data.type === "done") {
                setMessages((prev) =>
                  prev.map((m) =>
                    m.id === aiMessage.id
                      ? { ...m, isStreaming: false }
                      : m
                  )
                )
              }
            } catch {
              // Skip invalid JSON
            }
          }
        }
      }
    } catch (error) {
      setMessages((prev) =>
        prev.map((m) =>
          m.id === aiMessage.id
            ? {
                ...m,
                content: "I'm sorry, I couldn't process your request. Please check your OpenAI API key configuration and try again.",
                isStreaming: false,
              }
            : m
        )
      )
    } finally {
      setIsLoading(false)
    }
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  const clearChat = () => {
    setMessages([{
      id: "welcome-new",
      role: "assistant",
      content: "Chat cleared. How can I help you with your finances?",
      timestamp: new Date(),
    }])
    setChatId(null)
  }

  return (
    <div className="flex gap-6 h-[calc(100vh-10rem)]">
      {/* Sidebar */}
      <div className="w-72 flex-shrink-0 flex flex-col gap-4">
        {/* Quick Topics */}
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm">Quick Analysis</CardTitle>
          </CardHeader>
          <CardContent className="space-y-2">
            {QUICK_TOPICS.map((topic) => (
              <button
                key={topic.label}
                onClick={() => sendMessage(topic.question)}
                disabled={isLoading}
                className="w-full flex items-center gap-2 rounded-lg p-2 text-left hover:bg-accent transition-colors text-sm disabled:opacity-50"
              >
                <topic.icon className="h-4 w-4 text-primary shrink-0" />
                <span>{topic.label}</span>
              </button>
            ))}
          </CardContent>
        </Card>

        {/* Suggested Questions */}
        <Card className="flex-1 overflow-hidden">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm">Suggested Questions</CardTitle>
            <CardDescription className="text-xs">Click to ask</CardDescription>
          </CardHeader>
          <CardContent className="space-y-2 overflow-y-auto">
            {SUGGESTED_QUESTIONS.map((q) => (
              <button
                key={q}
                onClick={() => sendMessage(q)}
                disabled={isLoading}
                className="w-full text-left rounded-lg border p-2 text-xs hover:bg-accent hover:border-primary/30 transition-colors disabled:opacity-50"
              >
                <Lightbulb className="h-3 w-3 text-amber-500 inline mr-1.5" />
                {q}
              </button>
            ))}
          </CardContent>
        </Card>

        {/* Model Info */}
        <Card>
          <CardContent className="p-3">
            <div className="flex items-center gap-2 text-xs text-muted-foreground">
              <Bot className="h-3.5 w-3.5" />
              <span>Powered by GPT-4o + RAG</span>
            </div>
            <p className="text-[10px] text-muted-foreground mt-1">
              AI explains real data from your books. Never invents numbers.
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Chat Area */}
      <Card className="flex-1 flex flex-col overflow-hidden">
        {/* Header */}
        <div className="flex items-center justify-between border-b p-4">
          <div className="flex items-center gap-3">
            <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-gradient-to-br from-blue-500 to-purple-600">
              <Bot className="h-5 w-5 text-white" />
            </div>
            <div>
              <p className="font-semibold text-sm">FinSight AI Assistant</p>
              <div className="flex items-center gap-1.5">
                <div className="h-1.5 w-1.5 rounded-full bg-emerald-500 animate-pulse" />
                <p className="text-xs text-muted-foreground">Online · Real-time financial data</p>
              </div>
            </div>
          </div>
          <Button variant="ghost" size="sm" onClick={clearChat} className="h-8">
            <RefreshCw className="h-3.5 w-3.5 mr-1.5" />
            New Chat
          </Button>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.map((msg) => (
            <div
              key={msg.id}
              className={cn(
                "flex gap-3",
                msg.role === "user" ? "flex-row-reverse" : "flex-row"
              )}
            >
              <Avatar className="h-8 w-8 shrink-0 mt-0.5">
                <AvatarFallback className={msg.role === "assistant" ? "bg-gradient-to-br from-blue-500 to-purple-600 text-white" : "bg-primary text-primary-foreground"}>
                  {msg.role === "assistant" ? <Bot className="h-4 w-4" /> : <User className="h-4 w-4" />}
                </AvatarFallback>
              </Avatar>

              <div className={cn(
                "max-w-[80%] rounded-2xl px-4 py-3",
                msg.role === "user"
                  ? "bg-primary text-primary-foreground rounded-tr-sm"
                  : "bg-muted rounded-tl-sm"
              )}>
                {msg.role === "assistant" ? (
                  <div className="prose prose-sm dark:prose-invert max-w-none text-sm">
                    <ReactMarkdown>{msg.content || (msg.isStreaming ? "..." : "")}</ReactMarkdown>
                  </div>
                ) : (
                  <p className="text-sm whitespace-pre-wrap">{msg.content}</p>
                )}
                {msg.isStreaming && (
                  <div className="flex items-center gap-1 mt-2">
                    {[1, 2, 3].map((i) => (
                      <div
                        key={i}
                        className="h-1.5 w-1.5 rounded-full bg-current opacity-60 typing-dot"
                        style={{ animationDelay: `${(i - 1) * 0.2}s` }}
                      />
                    ))}
                  </div>
                )}
              </div>
            </div>
          ))}
          <div ref={messagesEndRef} />
        </div>

        <Separator />

        {/* Input */}
        <div className="p-4">
          <div className="flex gap-2 items-end">
            <Textarea
              ref={textareaRef}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask about your finances... (Enter to send, Shift+Enter for new line)"
              className="min-h-[80px] max-h-[200px] resize-none"
              disabled={isLoading}
            />
            <Button
              size="icon"
              onClick={() => sendMessage()}
              disabled={!input.trim() || isLoading}
              className="h-10 w-10 shrink-0"
            >
              <Send className="h-4 w-4" />
            </Button>
          </div>
          <p className="text-[10px] text-muted-foreground mt-2 text-center">
            AI responses are based on your actual financial records. All calculations are performed by our secure backend.
          </p>
        </div>
      </Card>
    </div>
  )
}
