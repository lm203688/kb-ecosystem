'use client';

import React, { useState, useMemo, useCallback, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useSession, signIn } from 'next-auth/react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { LandingHero } from '@/components/modules/landing-hero';
import { BirthInputForm, type BirthFormData } from '@/components/modules/birth-input-form';
import { BaziChartDisplay } from '@/components/modules/bazi-chart-display';
import { ElementChart } from '@/components/modules/element-chart';
import { PredictionChat } from '@/components/modules/prediction-chat';
import { PricingTiers } from '@/components/modules/pricing-tiers';
import { TrustDashboard } from '@/components/modules/trust-dashboard';
import { LuckPillarsTimeline } from '@/components/modules/luck-pillars-timeline';
import type { BaziChart, DayMasterStrength } from '@/lib/bazi-engine';
import {
  Star,
  LayoutDashboard,
  MessageSquare,
  Coins,
  ShieldCheck,
  Clock,
  Sparkles,
  TrendingUp,
  AlertTriangle,
  Flame,
  Leaf,
  Droplets,
  Mountain,
  Swords,
  ArrowRight,
} from 'lucide-react';
import { cn } from '@/lib/utils';

/* ── Helpers ── */

const STRENGTH_BADGE: Record<string, { label: string; color: string }> = {
  very_strong: { label: '身旺 Very Strong', color: 'text-[oklch(0.72_0.18_25)] border-[oklch(0.35_0.12_25)]' },
  strong: { label: '身强 Strong', color: 'text-[oklch(0.78_0.14_75)] border-[oklch(0.35_0.10_75)]' },
  balanced: { label: '中和 Balanced', color: 'text-[oklch(0.72_0.16_145)] border-[oklch(0.35_0.10_145)]' },
  weak: { label: '身弱 Weak', color: 'text-[oklch(0.68_0.12_240)] border-[oklch(0.30_0.08_240)]' },
  very_weak: { label: '极弱 Very Weak', color: 'text-[oklch(0.65_0.10_280)] border-[oklch(0.30_0.06_280)]' },
};

const ELEMENT_DISPLAY: Record<string, { chinese: string; label: string; color: string; icon: React.ReactNode }> = {
  wood: { chinese: '木', label: 'Wood', color: 'text-[oklch(0.72_0.16_145)]', icon: <Leaf className="size-3" /> },
  fire: { chinese: '火', label: 'Fire', color: 'text-[oklch(0.72_0.18_25)]', icon: <Flame className="size-3" /> },
  earth: { chinese: '土', label: 'Earth', color: 'text-[oklch(0.78_0.14_75)]', icon: <Mountain className="size-3" /> },
  metal: { chinese: '金', label: 'Metal', color: 'text-[oklch(0.75_0.03_265)]', icon: <Swords className="size-3" /> },
  water: { chinese: '水', label: 'Water', color: 'text-[oklch(0.68_0.12_240)]', icon: <Droplets className="size-3" /> },
};

/* ── Main Page ── */

export default function Home() {
  const { data: session, status } = useSession();
  const userId = (session?.user as { id?: string } | undefined)?.id;

  const [hasStarted, setHasStarted] = useState(false);
  const [baziChart, setBaziChart] = useState<BaziChart | null>(null);
  const [dayMasterStrength, setDayMasterStrength] = useState<DayMasterStrength | null>(null);
  const [birthYear, setBirthYear] = useState<number | null>(null);
  const [isGenerating, setIsGenerating] = useState(false);
  const [activeTier, setActiveTier] = useState<number | null>(null);
  const [activeTab, setActiveTab] = useState('overview');

  // Auto sign-in as guest on mount
  useEffect(() => {
    if (status === 'unauthenticated') {
      signIn('guest', { guestId: crypto.randomUUID(), redirect: false });
    }
  }, [status]);

  const handleStartReading = useCallback(() => { setHasStarted(true); }, []);
  const handleViewPricing = useCallback(() => { setHasStarted(true); setActiveTab('pricing'); }, []);

  const handleBirthSubmit = useCallback(async (data: BirthFormData) => {
    setIsGenerating(true);
    try {
      const res = await fetch('/api/bazi/calculate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      });
      if (res.ok) {
        const json = await res.json();
        if (json.success && json.data) {
          setBaziChart(json.data.chart);
          setDayMasterStrength(json.data.dayMasterStrength);
          setBirthYear(data.year);
        }
      }
    } catch {
      const { calculateBazi, getDayMasterStrength } = await import('@/lib/bazi-engine');
      const chart = calculateBazi(data.year, data.month, data.day, data.hour);
      setBaziChart(chart);
      setDayMasterStrength(getDayMasterStrength(chart));
      setBirthYear(data.year);
    } finally {
      setIsGenerating(false);
    }
  }, []);

  const currentAge = useMemo(() => {
    if (!baziChart || !birthYear) return 30;
    return new Date().getFullYear() - birthYear;
  }, [baziChart, birthYear]);

  return (
    <div className="min-h-screen bg-background">
      <AnimatePresence mode="wait">
        {!hasStarted ? (
          <motion.div
            key="landing"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0, y: -10 }}
            transition={{ duration: 0.3 }}
          >
            <LandingHero
              onStartFreeReading={handleStartReading}
              onViewPricing={handleViewPricing}
            />
          </motion.div>
        ) : (
          <motion.div
            key="app"
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
            className="min-h-screen"
          >
            {/* Top Nav — minimal, Linear-style */}
            <header className="sticky top-0 z-50 border-b border-[oklch(1_0_0_/6%)] bg-[oklch(0.10_0.015_265_/80%)] backdrop-blur-xl">
              <div className="mx-auto flex h-12 max-w-5xl items-center justify-between px-4">
                <button
                  onClick={() => setHasStarted(false)}
                  className="flex items-center gap-2 transition-opacity hover:opacity-70"
                >
                  <div className="flex size-7 items-center justify-center rounded-lg border border-[oklch(1_0_0_/8%)] bg-[oklch(0.14_0.015_265)]">
                    <Star className="size-3.5 text-[oklch(0.78_0.145_85)]" />
                  </div>
                  <span className="text-xs font-semibold tracking-wide text-[oklch(0.70_0.02_265)]">
                    OracleMind
                  </span>
                </button>
                <div className="flex items-center gap-3">
                  {baziChart && (
                    <Badge
                      variant="outline"
                      className="border-[oklch(0.78_0.145_85_/15%)] text-[10px] text-[oklch(0.78_0.145_85)]"
                    >
                      <Sparkles className="mr-1 size-3" />
                      {baziChart.dayMaster} · {baziChart.dayMasterElement}
                    </Badge>
                  )}
                  <div className="flex items-center gap-1.5">
                    <div className="size-1.5 rounded-full bg-[oklch(0.72_0.16_145)] animate-pulse" />
                    <span className="text-[10px] text-[oklch(0.40_0.02_265)]">Online</span>
                  </div>
                </div>
              </div>
            </header>

            {/* Main Content */}
            <div className="mx-auto max-w-5xl px-4 py-5">
              {!baziChart ? (
                <div className="flex min-h-[60vh] items-center justify-center">
                  <BirthInputForm onSubmit={handleBirthSubmit} isLoading={isGenerating} />
                </div>
              ) : (
                <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-5">
                  {/* Tabs — minimal pill style */}
                  <TabsList className="w-full justify-start gap-1 rounded-lg border border-[oklch(1_0_0_/6%)] bg-[oklch(0.12_0.015_265)] p-1">
                    {[
                      { value: 'overview', icon: <LayoutDashboard className="size-3.5" />, label: 'Overview' },
                      { value: 'chat', icon: <MessageSquare className="size-3.5" />, label: 'AI Chat' },
                      { value: 'luck', icon: <Clock className="size-3.5" />, label: 'Luck Pillars' },
                      { value: 'pricing', icon: <Coins className="size-3.5" />, label: 'Pricing' },
                      { value: 'trust', icon: <ShieldCheck className="size-3.5" />, label: 'Trust' },
                    ].map((tab) => (
                      <TabsTrigger
                        key={tab.value}
                        value={tab.value}
                        className={cn(
                          'gap-1.5 rounded-md px-3 py-1.5 text-xs font-medium transition-all data-[state=active]:bg-[oklch(0.78_0.145_85)] data-[state=active]:text-[oklch(0.12_0.02_265)] data-[state=active]:shadow-sm data-[state=active]:shadow-[oklch(0.78_0.145_85_/15%)] text-[oklch(0.45_0.02_265)] hover:text-[oklch(0.60_0.02_265)]',
                        )}
                      >
                        {tab.icon}
                        <span className="hidden sm:inline">{tab.label}</span>
                      </TabsTrigger>
                    ))}
                  </TabsList>

                  {/* Overview Tab */}
                  <TabsContent value="overview" className="space-y-5">
                    <div className="grid gap-5 lg:grid-cols-3">
                      {/* Left Column */}
                      <div className="space-y-5 lg:col-span-2">
                        <BaziChartDisplay chart={baziChart} />
                        <LuckPillarsTimeline luckPillars={baziChart.luckPillars} currentAge={currentAge} />

                        {/* Day Master Strength */}
                        {dayMasterStrength && (
                          <motion.div
                            initial={{ opacity: 0, y: 12 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ duration: 0.3, delay: 0.15 }}
                            className="glass-card rounded-2xl p-5 sm:p-6"
                          >
                            <div className="mb-4 flex items-center justify-between">
                              <h3 className="text-sm font-semibold text-foreground">Day Master Strength</h3>
                              <Badge variant="outline" className={cn('text-[10px]', STRENGTH_BADGE[dayMasterStrength.strength]?.color)}>
                                {STRENGTH_BADGE[dayMasterStrength.strength]?.label}
                              </Badge>
                            </div>

                            <p className="mb-4 text-xs text-[oklch(0.50_0.02_265)] leading-relaxed">
                              {dayMasterStrength.description}
                            </p>

                            <div className="grid gap-3 sm:grid-cols-2">
                              {/* Favorable */}
                              <div className="rounded-xl border border-[oklch(0.35_0.10_145)] bg-[oklch(0.25_0.06_145_/30%)] p-3">
                                <div className="mb-2 flex items-center gap-1.5 text-[10px] font-semibold uppercase tracking-wider text-[oklch(0.72_0.16_145)]">
                                  <Sparkles className="size-3" /> Favorable (喜用神)
                                </div>
                                <div className="flex flex-wrap gap-1.5">
                                  {dayMasterStrength.favorableElements.map((el) => {
                                    const info = ELEMENT_DISPLAY[el];
                                    return (
                                      <span
                                        key={el}
                                        className={cn('flex items-center gap-1 rounded-md border px-2 py-1 text-xs', info?.color, 'border-current/20')}
                                      >
                                        {info?.icon} {info?.chinese}
                                      </span>
                                    );
                                  })}
                                </div>
                              </div>

                              {/* Unfavorable */}
                              <div className="rounded-xl border border-[oklch(0.35_0.12_25)] bg-[oklch(0.25_0.08_25_/20%)] p-3">
                                <div className="mb-2 flex items-center gap-1.5 text-[10px] font-semibold uppercase tracking-wider text-[oklch(0.72_0.18_25)]">
                                  <AlertTriangle className="size-3" /> Unfavorable (忌神)
                                </div>
                                <div className="flex flex-wrap gap-1.5">
                                  {dayMasterStrength.unfavorableElements.map((el) => {
                                    const info = ELEMENT_DISPLAY[el];
                                    return (
                                      <span
                                        key={el}
                                        className={cn('flex items-center gap-1 rounded-md border px-2 py-1 text-xs', info?.color, 'border-current/20')}
                                      >
                                        {info?.icon} {info?.chinese}
                                      </span>
                                    );
                                  })}
                                </div>
                              </div>
                            </div>
                          </motion.div>
                        )}
                      </div>

                      {/* Right Column */}
                      <div className="space-y-5">
                        <ElementChart scores={baziChart.elementScores} />

                        {/* Quick Chat CTA */}
                        <div className="glass-card rounded-2xl p-5">
                          <div className="mb-3 flex items-center gap-1.5">
                            <MessageSquare className="size-3.5 text-[oklch(0.78_0.145_85)]" />
                            <span className="text-sm font-semibold text-foreground">Quick Prediction</span>
                          </div>
                          <p className="mb-3 text-xs text-[oklch(0.45_0.02_265)]">
                            Ask about your {baziChart.dayMaster} ({baziChart.dayMasterElement}) chart
                          </p>
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => setActiveTab('chat')}
                            className="w-full gap-1.5 text-xs border-[oklch(1_0_0_/8%)] text-[oklch(0.60_0.02_265)] hover:border-[oklch(0.78_0.145_85_/20%)] hover:text-[oklch(0.78_0.145_85)]"
                          >
                            Open AI Chat
                            <ArrowRight className="size-3" />
                          </Button>
                        </div>
                      </div>
                    </div>
                  </TabsContent>

                  {/* Chat Tab */}
                  <TabsContent value="chat">
                    <PredictionChat baziChart={baziChart} userId={userId} />
                  </TabsContent>

                  {/* Luck Tab */}
                  <TabsContent value="luck" className="space-y-5">
                    <LuckPillarsTimeline luckPillars={baziChart.luckPillars} currentAge={currentAge} />
                    <BaziChartDisplay chart={baziChart} />
                  </TabsContent>

                  {/* Pricing Tab */}
                  <TabsContent value="pricing" className="space-y-5">
                    <PricingTiers activeTier={activeTier} onSelectTier={setActiveTier} />
                    <TrustDashboard userId={userId} />
                  </TabsContent>

                  {/* Trust Tab */}
                  <TabsContent value="trust">
                    <TrustDashboard userId={userId} />
                  </TabsContent>
                </Tabs>
              )}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}