'use client';

import React, { useState, useRef, useEffect, useCallback } from 'react';
import ReactMarkdown from 'react-markdown';
import { motion, AnimatePresence } from 'framer-motion';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';
import { Textarea } from '@/components/ui/textarea';
import { Button } from '@/components/ui/button';
import { Skeleton } from '@/components/ui/skeleton';
import { Collapsible, CollapsibleTrigger, CollapsibleContent } from '@/components/ui/collapsible';
import type { BaziChart } from '@/lib/bazi-engine';
import type { PredictionRoute } from '@/lib/prediction-router';
import {
  Send, Bot, User as UserIcon, Sparkles, Zap, BarChart3, Brain,
  DollarSign, Clock, ChevronDown, History, CheckCircle2, MinusCircle, XCircle, Heart,
} from 'lucide-react';
import { cn } from '@/lib/utils';

/* ── Types ── */

interface ChatMessage {
  id: string;
  role: 'user' | 'ai';
  content: string;
  methods?: string[];
  cost?: number;
  tier?: number;
  estimatedTime?: string;
  category?: string;
  predictionId?: string;
  verificationStatus?: string;
}

interface PastPrediction {
  id: string;
  question: string;
  prediction: string;
  result: string;
  category: string;
  predictionDate: string;
}

const QUICK_QUESTIONS = [
  { text: 'Will I get promoted this year?', icon: <Zap className="size-3" /> },
  { text: 'Good time to start a business?', icon: <BarChart3 className="size-3" /> },
  { text: "What's my life purpose?", icon: <Sparkles className="size-3" /> },
  { text: 'Will my relationship last?', icon: <Heart className="size-3" /> },
  { text: 'Stock market outlook?', icon: <DollarSign className="size-3" /> },
];

const METHOD_LABELS: Record<string, { label: string; icon: React.ReactNode }> = {
  rule_engine: { label: 'Rule Engine', icon: <Zap className="size-3" /> },
  statistical: { label: 'Statistical', icon: <BarChart3 className="size-3" /> },
  multi_agent: { label: 'Multi-Agent', icon: <Brain className="size-3" /> },
};

const CATEGORY_LABELS: Record<string, string> = {
  objective: 'Objective',
  personal_related: 'Personal',
  deep_destiny: 'Destiny',
};

const VERIFICATION_STATUS: Record<string, { label: string; color: string }> = {
  confirmed: { label: 'Confirmed', color: 'text-[oklch(0.72_0.16_145)] border-[oklch(0.35_0.10_145)]' },
  partial: { label: 'Partial', color: 'text-[oklch(0.78_0.14_75)] border-[oklch(0.35_0.10_75)]' },
  denied: { label: 'Denied', color: 'text-[oklch(0.72_0.18_25)] border-[oklch(0.35_0.12_25)]' },
};

const RESULT_STATUS: Record<string, { label: string; color: string }> = {
  pending: { label: 'Pending', color: 'text-[oklch(0.50_0.02_265)]' },
  confirmed: { label: 'Confirmed', color: 'text-[oklch(0.72_0.16_145)]' },
  partial: { label: 'Partial', color: 'text-[oklch(0.78_0.14_75)]' },
  denied: { label: 'Denied', color: 'text-[oklch(0.72_0.18_25)]' },
  expired: { label: 'Expired', color: 'text-[oklch(0.40_0.02_265)]' },
};

/* ── Component ── */

interface PredictionChatProps {
  baziChart: BaziChart | null;
  userId?: string;
}

export function PredictionChat({ baziChart, userId }: PredictionChatProps) {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);
  const messageRefs = useRef<Map<string, HTMLDivElement>>(new Map());

  const [pastPredictions, setPastPredictions] = useState<PastPrediction[]>([]);
  const [pastPredictionsOpen, setPastPredictionsOpen] = useState(false);
  const [pastPredictionsLoading, setPastPredictionsLoading] = useState(false);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages, isTyping]);

  const effectiveUserId = userId || 'anonymous';

  const fetchPastPredictions = useCallback(async () => {
    setPastPredictionsLoading(true);
    try {
      const res = await fetch(`/api/feedback/user/${effectiveUserId}`);
      if (res.ok) {
        const json = await res.json();
        if (json.success && json.data) setPastPredictions(json.data);
      }
    } catch { /* silent */ } finally {
      setPastPredictionsLoading(false);
    }
  }, [effectiveUserId]);

  useEffect(() => {
    if (messages.length > 0) fetchPastPredictions();
  }, [messages.length, fetchPastPredictions]);

  const scrollToMessage = useCallback((predictionId: string) => {
    const el = messageRefs.current.get(predictionId);
    if (el) {
      el.scrollIntoView({ behavior: 'smooth', block: 'center' });
      el.classList.add('ring-1', 'ring-[oklch(0.78_0.145_85)]');
      setTimeout(() => el.classList.remove('ring-1', 'ring-[oklch(0.78_0.145_85)]'), 2000);
    }
    setPastPredictionsOpen(false);
  }, []);

  const handleVerify = useCallback(async (predictionId: string, result: 'confirmed' | 'partial' | 'denied') => {
    try {
      const res = await fetch('/api/feedback/verify', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ predictionId, result }),
      });
      if (res.ok) {
        const json = await res.json();
        if (json.success) {
          setMessages((prev) =>
            prev.map((msg) =>
              msg.predictionId === predictionId ? { ...msg, verificationStatus: result } : msg
            )
          );
          fetchPastPredictions();
        }
      }
    } catch { /* silent */ }
  }, [fetchPastPredictions]);

  const sendMessage = async (text: string) => {
    if (!text.trim()) return;
    const userMsg: ChatMessage = { id: crypto.randomUUID(), role: 'user', content: text.trim() };
    setMessages((prev) => [...prev, userMsg]);
    setInput('');
    setIsTyping(true);

    try {
      const res = await fetch('/api/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: text.trim(), chart: baziChart, tier: undefined, userId: effectiveUserId }),
      });

      if (res.ok) {
        const json = await res.json();
        if (json.success && json.data) {
          const route: PredictionRoute = json.data.route;
          const aiMsg: ChatMessage = {
            id: crypto.randomUUID(),
            role: 'ai',
            content: json.data.response,
            methods: route.methods,
            cost: route.estimatedCost,
            tier: route.tier,
            estimatedTime: route.estimatedTime,
            category: route.category,
            predictionId: json.data.predictionId,
          };
          setMessages((prev) => [...prev, aiMsg]);
        } else {
          setMessages((prev) => [...prev, {
            id: crypto.randomUUID(), role: 'ai',
            content: `Something went wrong. ${json.error || 'Please try again.'}`,
          }]);
        }
      } else {
        setMessages((prev) => [...prev, {
          id: crypto.randomUUID(), role: 'ai',
          content: 'Failed to get prediction. Please try again.',
        }]);
      }
    } catch {
      setMessages((prev) => [...prev, {
        id: crypto.randomUUID(), role: 'ai',
        content: 'Network error. Please check your connection.',
      }]);
    } finally {
      setIsTyping(false);
    }
  };

  return (
    <div className="glass-card flex flex-col overflow-hidden rounded-2xl" style={{ height: 600 }}>
      {/* Header */}
      <div className="shrink-0 border-b border-[oklch(1_0_0_/6%)] px-5 py-3">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-sm font-semibold text-foreground">AI Prediction</h3>
            <p className="mt-0.5 text-xs text-[oklch(0.45_0.02_265)]">
              {baziChart ? `问问你的${baziChart.dayMaster}命盘` : '请先生成命盘'}
            </p>
          </div>
          {baziChart && (
            <Badge variant="outline" className="border-[oklch(0.78_0.145_85_/20%)] text-[10px] text-[oklch(0.78_0.145_85)]">
              <Sparkles className="mr-1 size-3" /> Chart Ready
            </Badge>
          )}
        </div>
      </div>

      {/* Past Predictions */}
      <div className="shrink-0 px-4 pt-2">
        <Collapsible open={pastPredictionsOpen} onOpenChange={setPastPredictionsOpen}>
          <CollapsibleTrigger asChild>
            <button className="flex w-full items-center justify-between py-1 text-[11px] text-[oklch(0.45_0.02_265)] transition-colors hover:text-[oklch(0.60_0.02_265)]">
              <span className="flex items-center gap-1.5">
                <History className="size-3" />
                {pastPredictions.length > 0 ? `Predictions (${pastPredictions.length})` : 'My Predictions'}
              </span>
              <ChevronDown className={cn('size-3 transition-transform', pastPredictionsOpen && 'rotate-180')} />
            </button>
          </CollapsibleTrigger>
          <CollapsibleContent>
            <div className="max-h-32 overflow-y-auto rounded-lg border border-[oklch(1_0_0_/6%)] bg-[oklch(0.12_0.015_265)] mt-1">
              {pastPredictionsLoading ? (
                <div className="space-y-2 p-2">
                  <Skeleton className="h-5 w-full" />
                  <Skeleton className="h-5 w-3/4" />
                </div>
              ) : pastPredictions.length > 0 ? (
                <div className="divide-y divide-[oklch(1_0_0_/4%)]">
                  {pastPredictions.map((pred) => {
                    const status = RESULT_STATUS[pred.result] || RESULT_STATUS.pending;
                    const isInChat = messages.some((m) => m.predictionId === pred.id);
                    return (
                      <button
                        key={pred.id}
                        onClick={() => isInChat ? scrollToMessage(pred.id) : undefined}
                        disabled={!isInChat}
                        className={cn(
                          'flex w-full items-center justify-between gap-2 px-3 py-1.5 text-left text-[11px] transition-colors hover:bg-[oklch(0.16_0.015_265)]',
                          !isInChat && 'opacity-50 cursor-not-allowed'
                        )}
                      >
                        <span className="truncate text-[oklch(0.60_0.02_265)] flex-1">
                          {pred.question.length > 35 ? pred.question.slice(0, 35) + '...' : pred.question}
                        </span>
                        <span className={cn('shrink-0 text-[10px]', status.color)}>{status.label}</span>
                      </button>
                    );
                  })}
                </div>
              ) : (
                <p className="px-3 py-3 text-center text-[11px] text-[oklch(0.40_0.02_265)]">
                  No predictions yet
                </p>
              )}
            </div>
          </CollapsibleContent>
        </Collapsible>
      </div>

      <Separator className="shrink-0 bg-[oklch(1_0_0_/6%)]" />

      {/* Messages */}
      <div ref={scrollRef} className="flex-1 overflow-y-auto custom-scrollbar px-4 py-3">
        <div className="space-y-4">
          {messages.length === 0 && (
            <motion.div
              initial={{ opacity: 0, y: 16 }}
              animate={{ opacity: 1, y: 0 }}
              className="flex h-full min-h-[180px] flex-col items-center justify-center gap-3 text-center"
            >
              <div className="flex size-12 items-center justify-center rounded-2xl border border-[oklch(1_0_0_/8%)] bg-[oklch(0.14_0.015_265)]">
                <Bot className="size-5 text-[oklch(0.50_0.02_265)]" />
              </div>
              <div>
                <p className="text-sm text-[oklch(0.60_0.02_265)]">
                  {baziChart
                    ? `问问你的${baziChart.dayMaster}（${baziChart.dayMasterElement}）命盘`
                    : 'Generate your BaZi chart first'}
                </p>
              </div>
            </motion.div>
          )}

          <AnimatePresence mode="popLayout">
            {messages.map((msg) => (
              <motion.div
                key={msg.id}
                ref={(el) => {
                  if (el && msg.predictionId) messageRefs.current.set(msg.predictionId!, el);
                }}
                initial={{ opacity: 0, y: 8, scale: 0.98 }}
                animate={{ opacity: 1, y: 0, scale: 1 }}
                exit={{ opacity: 0, scale: 0.96 }}
                transition={{ duration: 0.2 }}
                className={cn('flex gap-2.5', msg.role === 'user' ? 'flex-row-reverse' : 'flex-row')}
              >
                {/* Avatar */}
                <div className={cn(
                  'flex size-7 shrink-0 items-center justify-center rounded-full',
                  msg.role === 'user'
                    ? 'bg-[oklch(0.78_0.145_85)] text-[oklch(0.12_0.02_265)]'
                    : 'border border-[oklch(1_0_0_/8%)] bg-[oklch(0.14_0.015_265)] text-[oklch(0.50_0.02_265)]'
                )}>
                  {msg.role === 'user' ? <UserIcon className="size-3.5" /> : <Bot className="size-3.5" />}
                </div>

                {/* Content */}
                <div className={cn('max-w-[80%] space-y-1.5', msg.role === 'user' ? 'items-end' : 'items-start')}>
                  <div className={cn(
                    'rounded-xl px-3.5 py-2.5 text-sm leading-relaxed',
                    msg.role === 'user'
                      ? 'bg-[oklch(0.78_0.145_85)] text-[oklch(0.12_0.02_265)]'
                      : 'border border-[oklch(1_0_0_/6%)] bg-[oklch(0.14_0.015_265)] text-[oklch(0.85_0.01_265)] prose-sm prose-invert max-w-none [&_strong]:text-foreground [&_strong]:font-semibold [&_p]:my-1 [&_ul]:my-1 [&_ol]:my-1 [&_li]:my-0.5 [&_blockquote]:border-l-2 [&_blockquote]:border-[oklch(0.78_0.145_85)] [&_blockquote]:pl-3 [&_blockquote]:text-[oklch(0.60_0.02_265)] [&_blockquote]:italic [&_h3]:text-foreground [&_h3]:text-base [&_h3]:font-semibold [&_h3]:mt-3 [&_h3]:mb-1 [&_hr]:border-[oklch(1_0_0_/8%)] [&_hr]:my-3 [&_code]:text-[oklch(0.78_0.145_85)]'
                  )}>
                    {msg.role === 'ai' ? (
                      <ReactMarkdown>{msg.content}</ReactMarkdown>
                    ) : (
                      msg.content
                    )}
                  </div>

                  {/* Verification status */}
                  {msg.role === 'ai' && msg.verificationStatus && (
                    <Badge variant="outline" className={cn('text-[10px] gap-1', VERIFICATION_STATUS[msg.verificationStatus]?.color)}>
                      {VERIFICATION_STATUS[msg.verificationStatus]?.label}
                    </Badge>
                  )}

                  {/* AI metadata */}
                  {msg.role === 'ai' && msg.methods && (
                    <div className="flex flex-wrap items-center gap-1.5 text-[10px] text-[oklch(0.40_0.02_265)]">
                      {msg.methods.map((method) => (
                        <span key={method} className="flex items-center gap-0.5 rounded-md border border-[oklch(1_0_0_/6%)] bg-[oklch(0.12_0.015_265)] px-1.5 py-0.5">
                          {METHOD_LABELS[method]?.icon}
                          {METHOD_LABELS[method]?.label || method}
                        </span>
                      ))}
                      {msg.category && <span>{CATEGORY_LABELS[msg.category] || msg.category}</span>}
                      {msg.tier && <span>T{msg.tier}</span>}
                      {msg.cost !== undefined && <span>${msg.cost.toFixed(2)}</span>}
                    </div>
                  )}

                  {/* Verification buttons */}
                  {msg.role === 'ai' && msg.predictionId && !msg.verificationStatus && (
                    <div className="flex items-center gap-1">
                      <span className="mr-0.5 text-[10px] text-[oklch(0.40_0.02_265)]">Verify:</span>
                      <button
                        onClick={() => handleVerify(msg.predictionId!, 'confirmed')}
                        className="flex items-center gap-0.5 rounded-md border border-[oklch(0.35_0.10_145)] px-1.5 py-0.5 text-[10px] text-[oklch(0.72_0.16_145)] transition-colors hover:bg-[oklch(0.25_0.06_145)]"
                      >
                        <CheckCircle2 className="size-2.5" /> Yes
                      </button>
                      <button
                        onClick={() => handleVerify(msg.predictionId!, 'partial')}
                        className="flex items-center gap-0.5 rounded-md border border-[oklch(0.35_0.10_75)] px-1.5 py-0.5 text-[10px] text-[oklch(0.78_0.14_75)] transition-colors hover:bg-[oklch(0.22_0.05_75)]"
                      >
                        <MinusCircle className="size-2.5" /> Partial
                      </button>
                      <button
                        onClick={() => handleVerify(msg.predictionId!, 'denied')}
                        className="flex items-center gap-0.5 rounded-md border border-[oklch(0.35_0.12_25)] px-1.5 py-0.5 text-[10px] text-[oklch(0.72_0.18_25)] transition-colors hover:bg-[oklch(0.25_0.08_25)]"
                      >
                        <XCircle className="size-2.5" /> No
                      </button>
                    </div>
                  )}
                </div>
              </motion.div>
            ))}
          </AnimatePresence>

          {/* Typing indicator */}
          {isTyping && (
            <motion.div
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0 }}
              className="flex gap-2.5"
            >
              <div className="flex size-7 shrink-0 items-center justify-center rounded-full border border-[oklch(1_0_0_/8%)] bg-[oklch(0.14_0.015_265)]">
                <Bot className="size-3.5 text-[oklch(0.50_0.02_265)]" />
              </div>
              <div className="flex items-center gap-1 rounded-xl border border-[oklch(1_0_0_/6%)] bg-[oklch(0.14_0.015_265)] px-3.5 py-2.5">
                <span className="size-1.5 rounded-full bg-[oklch(0.78_0.145_85)] animate-bounce [animation-delay:0ms]" />
                <span className="size-1.5 rounded-full bg-[oklch(0.78_0.145_85)] animate-bounce [animation-delay:150ms]" />
                <span className="size-1.5 rounded-full bg-[oklch(0.78_0.145_85)] animate-bounce [animation-delay:300ms]" />
              </div>
            </motion.div>
          )}
        </div>
      </div>

      <Separator className="shrink-0 bg-[oklch(1_0_0_/6%)]" />

      {/* 快捷问题 */}
      {messages.length === 0 && (
        <div className="shrink-0 px-4 pt-2.5">
          <div className="flex flex-wrap gap-1.5">
            {QUICK_QUESTIONS.map((q) => (
              <button
                key={q.text}
                onClick={() => sendMessage(q.text)}
                className="flex items-center gap-1.5 rounded-full border border-[oklch(1_0_0_/6%)] px-3 py-1 text-[11px] text-[oklch(0.50_0.02_265)] transition-all hover:border-[oklch(0.78_0.145_85_/20%)] hover:text-[oklch(0.78_0.145_85)]"
              >
                {q.icon}
                {q.text}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Input */}
      <div className="shrink-0 p-3 pt-2">
        <div className="flex gap-2">
          <Textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendMessage(input);
              }
            }}
            placeholder={baziChart ? '关于你的命运，想问什么...' : '请先生成命盘...'}
            className="min-h-[40px] max-h-[100px] resize-none flex-1 border-[oklch(1_0_0_/8%)] bg-[oklch(0.12_0.015_265)] text-sm placeholder:text-[oklch(0.35_0.02_265)] hover:border-[oklch(1_0_0_/12%)] focus:border-[oklch(0.78_0.145_85)]"
            rows={1}
          />
          <Button
            onClick={() => sendMessage(input)}
            disabled={!input.trim() || isTyping}
            size="icon"
            className="shrink-0 size-10 rounded-xl bg-[oklch(0.78_0.145_85)] text-[oklch(0.12_0.02_265)] hover:bg-[oklch(0.82_0.14_85)]"
          >
            <Send className="size-4" />
          </Button>
        </div>
      </div>
    </div>
  );
}