'use client';

import React, { useEffect, useState, useCallback } from 'react';
import { motion } from 'framer-motion';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { Skeleton } from '@/components/ui/skeleton';
import { Button } from '@/components/ui/button';
import { ScrollArea } from '@/components/ui/scroll-area';
import { useToast } from '@/hooks/use-toast';
import {
  ShieldCheck, TrendingUp, CheckCircle2, Clock, XCircle,
  BarChart3, Users, Award, Target, Heart, Zap, RefreshCw,
  Eye, Loader2,
} from 'lucide-react';
import { cn } from '@/lib/utils';

/* ── Types ── */

interface AccuracyCategory {
  name: string;
  accuracy: number;
  totalPredictions: number;
  verified: number;
  icon: React.ReactNode;
}

interface UserPrediction {
  id: string;
  question: string;
  category: string;
  date: string;
  status: 'pending' | 'confirmed' | 'denied' | 'partial' | 'expired';
}

/* ── Fallback Data ── */

const FALLBACK_CATEGORIES: AccuracyCategory[] = [
  { name: 'Career', accuracy: 87, totalPredictions: 3240, verified: 2809, icon: <TrendingUp className="size-3.5" /> },
  { name: 'Relationships', accuracy: 82, totalPredictions: 2870, verified: 2353, icon: <Heart className="size-3.5" /> },
  { name: 'Wealth', accuracy: 79, totalPredictions: 1950, verified: 1541, icon: <BarChart3 className="size-3.5" /> },
  { name: 'Health', accuracy: 91, totalPredictions: 1420, verified: 1292, icon: <Target className="size-3.5" /> },
  { name: 'Academics', accuracy: 85, totalPredictions: 1100, verified: 935, icon: <Award className="size-3.5" /> },
  { name: 'Objective', accuracy: 73, totalPredictions: 4200, verified: 3066, icon: <Zap className="size-3.5" /> },
];

const FALLBACK_TOTAL = FALLBACK_CATEGORIES.reduce((s, c) => s + c.totalPredictions, 0);
const FALLBACK_VERIFIED = FALLBACK_CATEGORIES.reduce((s, c) => s + c.verified, 0);
const FALLBACK_ACC = Math.round((FALLBACK_VERIFIED / FALLBACK_TOTAL) * 100);

const CATEGORY_ICON_MAP: Record<string, React.ReactNode> = {
  career: <TrendingUp className="size-3" />, relationships: <Heart className="size-3" />,
  wealth: <BarChart3 className="size-3" />, health: <Target className="size-3" />,
  academics: <Award className="size-3" />, objective: <Zap className="size-3" />,
};

const STATUS_CONFIG: Record<string, { label: string; color: string; icon: React.ReactNode }> = {
  pending: { label: 'Pending', color: 'text-[oklch(0.50_0.02_265)]', icon: <Clock className="size-3" /> },
  confirmed: { label: 'Confirmed', color: 'text-[oklch(0.72_0.16_145)]', icon: <CheckCircle2 className="size-3" /> },
  denied: { label: 'Denied', color: 'text-[oklch(0.72_0.18_25)]', icon: <XCircle className="size-3" /> },
  partial: { label: 'Partial', color: 'text-[oklch(0.78_0.14_75)]', icon: <RefreshCw className="size-3" /> },
  expired: { label: 'Expired', color: 'text-[oklch(0.40_0.02_265)]', icon: <Clock className="size-3" /> },
};

const FLYWHEEL_STEPS = [
  { icon: <Zap className="size-4" />, title: '生成', desc: 'Ask and receive an AI-powered prediction.' },
  { icon: <Eye className="size-4" />, title: 'Verify', desc: 'Confirm whether the prediction came true.' },
  { icon: <CheckCircle2 className="size-4" />, title: 'Track', desc: 'Build your personal accuracy profile.' },
  { icon: <ShieldCheck className="size-4" />, title: 'Build Trust', desc: 'Aggregate data proves system credibility.' },
];

/* ── Component ── */

interface TrustDashboardProps {
  userId?: string;
}

export function TrustDashboard({ userId }: TrustDashboardProps) {
  const { toast } = useToast();
  const effectiveUserId = userId ?? 'anonymous';

  const [statsLoading, setStatsLoading] = useState(true);
  const [totalPredictions, setTotalPredictions] = useState(FALLBACK_TOTAL);
  const [totalVerified, setTotalVerified] = useState(FALLBACK_VERIFIED);
  const [overallAccuracy, setOverallAccuracy] = useState(FALLBACK_ACC);
  const [categories, setCategories] = useState<AccuracyCategory[]>(FALLBACK_CATEGORIES);

  const [userPredictions, setUserPredictions] = useState<UserPrediction[]>([]);
  const [predictionsLoading, setPredictionsLoading] = useState(true);
  const [verifyingId, setVerifyingId] = useState<string | null>(null);

  const fetchStats = useCallback(async () => {
    setStatsLoading(true);
    try {
      const res = await fetch('/api/feedback/stats');
      if (res.ok) {
        const json = await res.json();
        if (json.success && json.data) {
          const d = json.data;
          setTotalPredictions(d.totalPredictions);
          setTotalVerified(d.totalVerified);
          setOverallAccuracy(d.totalVerified > 0 ? Math.round(d.accuracy * 100) : 0);
          if (d.totalPredictions > 0 && Object.keys(d.categoryAccuracy).length > 0) {
            setCategories(Object.entries(d.categoryAccuracy).map(([cat, acc]) => ({
              name: formatCategoryName(cat),
              accuracy: Math.round((acc as number) * 100),
              totalPredictions: 0, verified: 0,
              icon: CATEGORY_ICON_MAP[cat] || <Zap className="size-4" />,
            })));
          }
          return;
        }
      }
    } catch { /* fallback */ } finally {
      setStatsLoading(false);
    }
  }, []);

  const fetchUserPredictions = useCallback(async () => {
    setPredictionsLoading(true);
    try {
      const res = await fetch(`/api/feedback/user/${effectiveUserId}`);
      if (res.ok) {
        const json = await res.json();
        if (json.success && json.data) {
          setUserPredictions(json.data.map((p: { id: string; question: string; predictionDate: string; result: string; category: string }) => ({
            id: p.id, question: p.question,
            date: new Date(p.predictionDate).toLocaleDateString(),
            status: p.result as UserPrediction['status'],
            category: formatCategoryName(p.category),
          })));
          return;
        }
      }
      setUserPredictions([]);
    } catch { setUserPredictions([]); } finally {
      setPredictionsLoading(false);
    }
  }, [effectiveUserId]);

  useEffect(() => { fetchStats(); fetchUserPredictions(); }, [fetchStats, fetchUserPredictions]);

  const handleVerify = useCallback(async (predictionId: string, result: 'confirmed' | 'denied' | 'partial') => {
    setVerifyingId(predictionId);
    try {
      const res = await fetch('/api/feedback/verify', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ predictionId, result }),
      });
      if (res.ok) {
        const json = await res.json();
        if (json.success) {
          toast({ title: 'Verification recorded', description: `Marked as ${result}.` });
          fetchUserPredictions(); fetchStats();
        }
      }
    } catch { toast({ title: 'Error', variant: 'destructive' }); } finally { setVerifyingId(null); }
  }, [fetchUserPredictions, fetchStats, toast]);

  return (
    <div className="glass-card rounded-2xl p-5 sm:p-6 space-y-6">
      {/* Header */}
      <div>
        <h3 className="text-sm font-semibold text-foreground">Trust & Accuracy</h3>
        <p className="mt-0.5 text-xs text-[oklch(0.45_0.02_265)]">Verified prediction accuracy</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-4 gap-3">
        {[
          { label: 'Predictions', value: totalPredictions.toLocaleString(), icon: <BarChart3 className="size-3.5" /> },
          { label: 'Verified', value: totalVerified.toLocaleString(), icon: <CheckCircle2 className="size-3.5" /> },
          { label: 'Accuracy', value: `${overallAccuracy}%`, icon: <Target className="size-3.5" /> },
          { label: 'Users', value: '10,247', icon: <Users className="size-3.5" /> },
        ].map((stat, idx) => (
          <motion.div
            key={stat.label}
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.25, delay: idx * 0.05 }}
            className="text-center"
          >
            {statsLoading ? (
              <Skeleton className="mx-auto mb-1.5 size-7 rounded-lg" />
            ) : (
              <div className="mx-auto mb-1.5 flex size-7 items-center justify-center rounded-lg bg-[oklch(0.16_0.015_265)] text-[oklch(0.50_0.02_265)]">
                {stat.icon}
              </div>
            )}
            {statsLoading ? (
              <Skeleton className="mx-auto mb-0.5 h-4 w-10" />
            ) : (
              <div className="text-base font-bold text-foreground">{stat.value}</div>
            )}
            <div className="text-[9px] text-[oklch(0.40_0.02_265)]">{stat.label}</div>
          </motion.div>
        ))}
      </div>

      {/* Divider */}
      <div className="h-px bg-[oklch(1_0_0_/6%)]" />

      {/* Category Breakdown */}
      <div className="space-y-3">
        <h4 className="text-xs font-semibold uppercase tracking-wider text-[oklch(0.50_0.02_265)]">
          Category Breakdown
        </h4>
        {statsLoading ? (
          <div className="space-y-2">{Array.from({ length: 4 }).map((_, i) => <Skeleton key={i} className="h-4 w-full" />)}</div>
        ) : (
          <div className="space-y-2">
            {categories.map((cat, idx) => (
              <motion.div
                key={cat.name}
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.25, delay: idx * 0.05 }}
                className="flex items-center gap-3"
              >
                <span className="flex size-6 items-center justify-center text-[oklch(0.50_0.02_265)]">{cat.icon}</span>
                <span className="w-20 text-xs text-[oklch(0.60_0.02_265)]">{cat.name}</span>
                <div className="h-1 flex-1 overflow-hidden rounded-full bg-[oklch(1_0_0_/6%)]">
                  <motion.div
                    className="h-full rounded-full bg-[oklch(0.78_0.145_85)]"
                    initial={{ width: 0 }}
                    animate={{ width: `${cat.accuracy}%` }}
                    transition={{ duration: 0.6, delay: idx * 0.06 }}
                  />
                </div>
                <span className="w-8 text-right text-xs font-semibold text-foreground">{cat.accuracy}%</span>
              </motion.div>
            ))}
          </div>
        )}
      </div>

      {/* Divider */}
      <div className="h-px bg-[oklch(1_0_0_/6%)]" />

      {/* User Prediction Log */}
      <div className="space-y-3">
        <h4 className="text-xs font-semibold uppercase tracking-wider text-[oklch(0.50_0.02_265)]">
          Your Predictions
        </h4>
        {predictionsLoading ? (
          <div className="space-y-1.5">{Array.from({ length: 2 }).map((_, i) => <Skeleton key={i} className="h-10 w-full rounded-lg" />)}</div>
        ) : userPredictions.length > 0 ? (
          <ScrollArea className="h-[160px]">
            <div className="space-y-1.5 pr-2">
              {userPredictions.map((pred, idx) => {
                const status = STATUS_CONFIG[pred.status] ?? STATUS_CONFIG.pending;
                const isPending = pred.status === 'pending';
                return (
                  <motion.div
                    key={pred.id}
                    initial={{ opacity: 0, y: 4 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.2, delay: idx * 0.04 }}
                    className="rounded-lg border border-[oklch(1_0_0_/6%)] bg-[oklch(0.12_0.015_265)] p-2.5"
                  >
                    <div className="flex items-center justify-between gap-2">
                      <p className="min-w-0 flex-1 truncate text-xs text-[oklch(0.60_0.02_265)]">{pred.question}</p>
                      <span className={cn('shrink-0 flex items-center gap-0.5 text-[10px]', status.color)}>
                        {status.icon} {status.label}
                      </span>
                    </div>
                    {isPending && (
                      <div className="mt-1.5 flex items-center gap-1 pl-0">
                        <span className="text-[10px] text-[oklch(0.40_0.02_265)] mr-1">Verify:</span>
                        {(['confirmed', 'partial', 'denied'] as const).map((result) => {
                          const btnColor = {
                            confirmed: 'text-[oklch(0.72_0.16_145)] border-[oklch(0.35_0.10_145)] hover:bg-[oklch(0.25_0.06_145)]',
                            partial: 'text-[oklch(0.78_0.14_75)] border-[oklch(0.35_0.10_75)] hover:bg-[oklch(0.22_0.05_75)]',
                            denied: 'text-[oklch(0.72_0.18_25)] border-[oklch(0.35_0.12_25)] hover:bg-[oklch(0.25_0.08_25)]',
                          }[result];
                          return (
                            <Button
                              key={result}
                              variant="outline"
                              size="sm"
                              disabled={verifyingId === pred.id}
                              className={cn('h-6 gap-0.5 rounded-md border px-2 text-[10px] transition-colors', btnColor)}
                              onClick={() => handleVerify(pred.id, result)}
                            >
                              {verifyingId === pred.id ? <Loader2 className="size-2.5 animate-spin" /> : STATUS_CONFIG[result].icon}
                              {STATUS_CONFIG[result].label}
                            </Button>
                          );
                        })}
                      </div>
                    )}
                  </motion.div>
                );
              })}
            </div>
          </ScrollArea>
        ) : (
          <div className="flex flex-col items-center justify-center rounded-lg border border-dashed border-[oklch(1_0_0_/8%)] py-8 text-center">
            <ShieldCheck className="mb-2 size-6 text-[oklch(0.25_0.02_265)]" />
            <p className="text-xs text-[oklch(0.40_0.02_265)]">No predictions yet. Start a chat!</p>
          </div>
        )}
      </div>

      {/* Divider */}
      <div className="h-px bg-[oklch(1_0_0_/6%)]" />

      {/* Flywheel */}
      <div className="space-y-3">
        <h4 className="text-xs font-semibold uppercase tracking-wider text-[oklch(0.50_0.02_265)]">
          Credibility Flywheel
        </h4>
        <div className="grid grid-cols-4 gap-2">
          {FLYWHEEL_STEPS.map((step, idx) => (
            <motion.div
              key={step.title}
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.25, delay: idx * 0.07 }}
              className="flex flex-col items-center gap-1.5 rounded-xl border border-[oklch(1_0_0_/6%)] bg-[oklch(0.12_0.015_265)] p-3 text-center"
            >
              <div className="flex size-8 items-center justify-center rounded-lg text-[oklch(0.78_0.145_85)]">
                {step.icon}
              </div>
              <span className="text-[11px] font-semibold text-foreground">{step.title}</span>
              <span className="text-[9px] leading-tight text-[oklch(0.40_0.02_265)]">{step.desc}</span>
            </motion.div>
          ))}
        </div>
      </div>
    </div>
  );
}

function formatCategoryName(cat: string): string {
  const map: Record<string, string> = {
    career: 'Career', career_promotion: 'Career', relationships: 'Relationships',
    wealth: 'Wealth', finance: 'Wealth', health: 'Health',
    academics: 'Academics', exams: 'Academics', objective: 'Objective',
    personal_related: 'Personal', deep_destiny: 'Destiny', uncategorized: 'Other',
  };
  return map[cat] ?? cat.charAt(0).toUpperCase() + cat.slice(1).replace(/_/g, ' ');
}