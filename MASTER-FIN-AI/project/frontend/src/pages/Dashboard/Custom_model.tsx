"use client"

import type React from "react"

import { useState, useRef, useEffect } from "react"
import { Card, CardContent, CardHeader, CardTitle, CardDescription, CardFooter } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Badge } from "@/components/ui/badge"
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip"
import {
  Send,
  Trash2,
  Bot,
  Info,
  Sparkles,
  ArrowDown,
  Plus,
  MessageSquare,
  ChevronDown,
  ChevronRight,
  History,
} from "lucide-react"
import { format } from "date-fns"
import { motion, AnimatePresence } from "framer-motion"
import { cn } from "@/lib/utils"

interface Message {
  id: string
  role: "user" | "assistant" | "system"
  content: string
  timestamp: Date
}

interface ChatHistory {
  id: string
  title: string
  lastMessage: string
  timestamp: Date
  messages: Message[]
}

interface MonthSection {
  month: string
  year: number
  chats: ChatHistory[]
}

export default function CustomModel() {
  // Sample chat history data
  const [historyData, setHistoryData] = useState<MonthSection[]>([
    {
      month: "March",
      year: 2025,
      chats: [
        {
          id: "current",
          title: "Current Chat",
          lastMessage: "How can I help you today?",
          timestamp: new Date(),
          messages: [
            {
              id: "welcome",
              role: "system",
              content: "Welcome to the AI assistant. How can I help you today?",
              timestamp: new Date(),
            },
          ],
        },
      ],
    },
    {
      month: "February",
      year: 2025,
      chats: [
        {
          id: "feb-1",
          title: "React MongoDB CRUD App",
          lastMessage: "Here is the code for connecting MongoDB with React...",
          timestamp: new Date(2025, 1, 25),
          messages: [
            {
              id: "feb-1-welcome",
              role: "system",
              content: "Welcome to the AI assistant. How can I help you today?",
              timestamp: new Date(2025, 1, 25, 10, 0),
            },
            {
              id: "feb-1-user-1",
              role: "user",
              content: "How do I create a CRUD app with React and MongoDB?",
              timestamp: new Date(2025, 1, 25, 10, 1),
            },
            {
              id: "feb-1-assistant-1",
              role: "assistant",
              content: "Here is the code for connecting MongoDB with React...",
              timestamp: new Date(2025, 1, 25, 10, 2),
            },
          ],
        },
      ],
    },
    {
      month: "January",
      year: 2025,
      chats: [
        {
          id: "jan-1",
          title: "DeepSeek vs GPT Potential",
          lastMessage: "DeepSeek and GPT have different strengths...",
          timestamp: new Date(2025, 0, 15),
          messages: [],
        },
        {
          id: "jan-2",
          title: "API Contract Fetch Frontend",
          lastMessage: "Here is how you can fetch API data in React...",
          timestamp: new Date(2025, 0, 12),
          messages: [],
        },
      ],
    },
  ])

  const [activeChat, setActiveChat] = useState<string>("current")
  const [collapsedSections, setCollapsedSections] = useState<string[]>([])
  const [isSidebarOpen, setIsSidebarOpen] = useState(true)
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const [showScrollButton, setShowScrollButton] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const scrollAreaRef = useRef<HTMLDivElement>(null)
  const inputRef = useRef<HTMLInputElement>(null)
  const MAX_CHARS = 1000

  // Load messages for active chat
  useEffect(() => {
    // Find the active chat in history data
    for (const section of historyData) {
      const chat = section.chats.find((chat) => chat.id === activeChat)
      if (chat) {
        setMessages(chat.messages)
        break
      }
    }
  }, [activeChat, historyData])

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    scrollToBottom()
  }, [messages])

  // Focus input on load
  useEffect(() => {
    if (inputRef.current) {
      inputRef.current.focus()
    }
  }, [])

  // Check scroll position to show/hide scroll button
  const handleScroll = (e: React.UIEvent<HTMLDivElement>) => {
    const { scrollTop, scrollHeight, clientHeight } = e.currentTarget
    const bottomThreshold = 100
    const isNearBottom = scrollHeight - scrollTop - clientHeight < bottomThreshold
    setShowScrollButton(!isNearBottom)
  }

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  const toggleSection = (sectionName: string) => {
    if (collapsedSections.includes(sectionName)) {
      setCollapsedSections(collapsedSections.filter((s) => s !== sectionName))
    } else {
      setCollapsedSections([...collapsedSections, sectionName])
    }
  }

  const isSectionCollapsed = (sectionName: string) => {
    return collapsedSections.includes(sectionName)
  }

  const createNewChat = () => {
    const newChatId = `chat-${Date.now()}`
    const newChat: ChatHistory = {
      id: newChatId,
      title: "New Conversation",
      lastMessage: "How can I help you today?",
      timestamp: new Date(),
      messages: [
        {
          id: `${newChatId}-welcome`,
          role: "system",
          content: "Welcome to the AI assistant. How can I help you today?",
          timestamp: new Date(),
        },
      ],
    }

    // Add to current month or create new month section
    const currentDate = new Date()
    const currentMonth = format(currentDate, "MMMM")
    const currentYear = currentDate.getFullYear()

    const updatedHistory = [...historyData]
    const currentMonthSection = updatedHistory.find(
      (section) => section.month === currentMonth && section.year === currentYear,
    )

    if (currentMonthSection) {
      currentMonthSection.chats = [newChat, ...currentMonthSection.chats]
    } else {
      updatedHistory.unshift({
        month: currentMonth,
        year: currentYear,
        chats: [newChat],
      })
    }

    setHistoryData(updatedHistory)
    setActiveChat(newChatId)
    setMessages(newChat.messages)
  }

  const updateChatHistory = (chatId: string, newMessages: Message[]) => {
    const updatedHistory = historyData.map((section) => {
      const updatedChats = section.chats.map((chat) => {
        if (chat.id === chatId) {
          // Get the last non-system message for the title
          const lastUserMessage = [...newMessages].reverse().find((msg) => msg.role === "user")

          const lastAssistantMessage = [...newMessages].reverse().find((msg) => msg.role === "assistant")

          return {
            ...chat,
            messages: newMessages,
            title: lastUserMessage
              ? lastUserMessage.content.length > 30
                ? lastUserMessage.content.substring(0, 30) + "..."
                : lastUserMessage.content
              : chat.title,
            lastMessage: lastAssistantMessage
              ? lastAssistantMessage.content.length > 40
                ? lastAssistantMessage.content.substring(0, 40) + "..."
                : lastAssistantMessage.content
              : chat.lastMessage,
          }
        }
        return chat
      })
      return { ...section, chats: updatedChats }
    })

    setHistoryData(updatedHistory)
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim()) return

    // Generate a unique ID for the message
    const messageId = Date.now().toString()

    // Add user message
    const userMessage: Message = {
      id: `user-${messageId}`,
      role: "user",
      content: input.trim(),
      timestamp: new Date(),
    }

    const updatedMessages = [...messages, userMessage]
    setMessages(updatedMessages)
    updateChatHistory(activeChat, updatedMessages)

    setInput("")
    setIsLoading(true)

    // Simulated bot response (replace with actual API call)
    setTimeout(() => {
      const botMessage: Message = {
        id: `assistant-${messageId}`,
        role: "assistant",
        content:
          "This is an enhanced response from the AI assistant. In production, this would connect to your chosen AI model API. The response can include detailed information based on your query and can help with a wide range of tasks.",
        timestamp: new Date(),
      }

      const finalMessages = [...updatedMessages, botMessage]
      setMessages(finalMessages)
      updateChatHistory(activeChat, finalMessages)

      setIsLoading(false)
    }, 1500)
  }

  const clearChat = () => {
    const clearedMessages = [
      {
        id: "welcome-new",
        role: "system" as const,
        content: "Chat history cleared. How can I help you today?",
        timestamp: new Date(),
      },
    ]

    setMessages(clearedMessages)
    updateChatHistory(activeChat, clearedMessages)
  }

  // Handle keyboard shortcuts
  const handleKeyDown = (e: React.KeyboardEvent) => {
    // Ctrl+Enter to submit
    if (e.ctrlKey && e.key === "Enter") {
      handleSubmit(e as unknown as React.FormEvent)
    }
  }

  // Generate test messages for debugging
  const generateTestMessages = () => {
    const testMessages: Message[] = [
      {
        id: "system-1",
        role: "system",
        content: "Welcome to the AI assistant. How can I help you today?",
        timestamp: new Date(2025, 2, 1, 10, 0),
      },
    ]

    // Generate 15 test messages
    for (let i = 1; i <= 15; i++) {
      testMessages.push({
        id: `user-${i}`,
        role: "user",
        content: `This is test question ${i}. How does this work?`,
        timestamp: new Date(2025, 2, 1, 10, i),
      })

      testMessages.push({
        id: `assistant-${i}`,
        role: "assistant",
        content: `This is test response ${i}. Here's how it works: Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam auctor, nisl eget ultricies aliquam, nunc nisl aliquet nunc, quis aliquam nisl nunc quis nisl.`,
        timestamp: new Date(2025, 2, 1, 10, i + 0.5),
      })
    }

    setMessages(testMessages)
    updateChatHistory(activeChat, testMessages)
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-background to-background/80 pt-24 px-4">
  <div className="max-w-6xl mx-auto flex">
    {/* Sidebar */}
    <div className={cn("transition-all duration-300 overflow-hidden", isSidebarOpen ? "w-64" : "w-0")}>
      <div className="h-[700px] bg-card border border-r-0 border-primary/10 rounded-l-lg flex flex-col">
        {/* New chat button */}
        <div className="p-3 border-b">
          <Button variant="outline" className="w-full justify-start gap-2" onClick={createNewChat}>
            <Plus className="h-4 w-4" />
            New chat
          </Button>
        </div>

        {/* Chat history list */}
        <ScrollArea className="flex-1 p-2">
          {historyData.map((section) => (
            <div key={`${section.month}-${section.year}`} className="mb-4">
              <button
                className="flex items-center justify-between w-full py-1 text-sm font-medium text-muted-foreground"
                onClick={() => toggleSection(`${section.month}-${section.year}`)}
              >
                <span>
                  {section.month} {section.year}
                </span>
                <span>
                  {isSectionCollapsed(`${section.month}-${section.year}`) ? (
                    <ChevronRight className="h-4 w-4" />
                  ) : (
                    <ChevronDown className="h-4 w-4" />
                  )}
                </span>
              </button>

              {!isSectionCollapsed(`${section.month}-${section.year}`) && (
                <div className="mt-1 space-y-1">
                  {section.chats.map((chat) => (
                    <button
                      key={chat.id}
                      className={cn(
                        "w-full text-left px-2 py-2 rounded-lg text-sm truncate flex items-start gap-2",
                        activeChat === chat.id ? "bg-primary/10 text-primary" : "hover:bg-muted",
                      )}
                      onClick={() => setActiveChat(chat.id)}
                    >
                      <MessageSquare className="h-4 w-4 flex-shrink-0 mt-0.5" />
                      <div className="overflow-hidden">
                        <div className="truncate font-medium">{chat.title}</div>
                        <div className="truncate text-xs text-muted-foreground">{chat.lastMessage}</div>
                      </div>
                    </button>
                  ))}
                </div>
              )}
            </div>
          ))}
        </ScrollArea>
      </div>
    </div>

    {/* Main chat area */}
    <Card className="h-[700px] flex-1 flex flex-col shadow-lg border-primary/10 rounded-l-none">
      <CardHeader className="border-b bg-card/50 backdrop-blur-sm py-3 px-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Button
              variant="ghost"
              size="icon"
              className="h-8 w-8 mr-1"
              onClick={() => setIsSidebarOpen(!isSidebarOpen)}
            >
              <History className="h-4 w-4" />
            </Button>
            <div className="h-8 w-8 rounded-full bg-primary/20 flex items-center justify-center">
              <Bot className="h-4 w-4 text-primary" />
            </div>
            <div>
              <CardTitle className="text-base">AI Assistant</CardTitle>
              <CardDescription className="text-xs">Powered by custom model</CardDescription>
            </div>
          </div>
          <div className="flex gap-2">
            {/* Debug button - only for development */}
            <Button variant="outline" size="sm" onClick={generateTestMessages} className="h-8 text-xs">
              Test 30 msgs
            </Button>
            <TooltipProvider>
              <Tooltip>
                <TooltipTrigger asChild>
                  <Button variant="outline" size="icon" onClick={clearChat} className="h-8 w-8">
                    <Trash2 className="h-4 w-4" />
                  </Button>
                </TooltipTrigger>
                <TooltipContent>
                  <p>Clear chat history</p>
                </TooltipContent>
              </Tooltip>
            </TooltipProvider>
          </div>
        </div>
      </CardHeader>

      <CardContent className="flex-1 p-0 relative overflow-hidden">
        <ScrollArea className="h-full py-4 px-4" onScroll={handleScroll} ref={scrollAreaRef} type="always">
          <div className="pb-2">
            <AnimatePresence>
              {messages.map((message) => (
                <motion.div
                  key={message.id}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.3 }}
                  className="mb-4 last:mb-2"
                >
                  {message.role === "system" ? (
                    <div className="flex justify-center my-4">
                      <Badge
                        variant="outline"
                        className="bg-muted/50 text-muted-foreground flex items-center gap-1.5 px-3 py-1.5"
                      >
                        <Info className="h-3.5 w-3.5" />
                        {message.content}
                      </Badge>
                    </div>
                  ) : (
                    <div className={`flex gap-3 ${message.role === "user" ? "justify-end" : "justify-start"}`}>
                      {message.role === "assistant" && (
                        <Avatar className="h-8 w-8 mt-1 flex-shrink-0">
                          <AvatarFallback className="bg-primary/20 text-primary">AI</AvatarFallback>
                          <AvatarImage src="/placeholder.svg?height=32&width=32" />
                        </Avatar>
                      )}

                      <div className={`max-w-[80%]`}>
                        <div
                          className={`rounded-2xl px-4 py-2.5 ${
                            message.role === "user"
                              ? "bg-primary text-primary-foreground rounded-tr-none"
                              : "bg-muted rounded-tl-none"
                          }`}
                        >
                          {message.content}
                        </div>
                        <div
                          className={`text-xs text-muted-foreground mt-1 ${
                            message.role === "user" ? "text-right mr-1" : "ml-1"
                          }`}
                        >
                          {format(message.timestamp, "h:mm a")}
                        </div>
                      </div>

                      {message.role === "user" && (
                        <Avatar className="h-8 w-8 mt-1 flex-shrink-0">
                          <AvatarFallback className="bg-secondary/20">ME</AvatarFallback>
                          <AvatarImage src="/placeholder.svg?height=32&width=32" />
                        </Avatar>
                      )}
                    </div>
                  )}
                </motion.div>
              ))}

              {isLoading && (
                <motion.div
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="flex justify-start gap-3 mb-4"
                >
                  <Avatar className="h-8 w-8 mt-1 flex-shrink-0">
                    <AvatarFallback className="bg-primary/20 text-primary">AI</AvatarFallback>
                  </Avatar>
                  <div className="bg-muted rounded-2xl rounded-tl-none px-4 py-3">
                    <div className="flex space-x-2 items-center h-5">
                      <div className="w-2 h-2 bg-primary/60 rounded-full animate-bounce" />
                      <div className="w-2 h-2 bg-primary/60 rounded-full animate-bounce [animation-delay:0.2s]" />
                      <div className="w-2 h-2 bg-primary/60 rounded-full animate-bounce [animation-delay:0.4s]" />
                    </div>
                  </div>
                </motion.div>
              )}
              <div ref={messagesEndRef} />
            </AnimatePresence>
          </div>
        </ScrollArea>

        {/* Input form */}
        <form onSubmit={handleSubmit} className="border-t p-4 bg-card/50 backdrop-blur-sm">
          <div className="flex gap-2">
            <Input
              ref={inputRef}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Type your message..."
              className="flex-1"
              maxLength={MAX_CHARS}
            />
            <Button type="submit" disabled={isLoading}>
              <Send className="h-4 w-4" />
            </Button>
          </div>
        </form>

        {showScrollButton && (
          <Button
            variant="outline"
            size="icon"
            className="absolute bottom-20 right-4 rounded-full shadow-md bg-background/80 backdrop-blur-sm z-10"
            onClick={scrollToBottom}
          >
            <ArrowDown className="h-4 w-4" />
          </Button>
        )}
      </CardContent>
    </Card>
  </div>
</div>
  )
}

