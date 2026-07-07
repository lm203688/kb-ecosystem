'use client';

import React from 'react';
import { motion } from 'framer-motion';
import { Badge } from '@/components/ui/badge';
import { ScrollArea, ScrollBar } from '@/components/ui/scroll-area';
import { Separator } from '@/components/ui/separator';
import { getTierConfigs } from '@/lib/prediction-router';
import type { PredictionMethod } from '@/lib/prediction-router';
import {
  Zap, BarChart3, Brain, Coins, Clock, Check, Sparkles, Crown,
} from 'lucide-react';
import { cn } from '@/lib/utils';

const METHOD_LABELS: Record<PredictionMethod, { label: string; icon: React.ReactNode }> = {
  rule_engine: { label: '规则', icon: <Zap className="size-3" /> },
  statistical: { label: '统计', icon: <BarChart3 className="size-3" /> },
  multi_agent: { label: '多Agent', icon: <Brain className="size-3" /> },
};

const TIER_ICONS: Record<number, React.ReactNode> = {
  1: <Zap className="size-4" />,
  2: <BarChart3 className="size-4" />,
  3: <Brain className="size-4" />,
  4: <Sparkles className="size-4" />,
  5: <Crown className="size-4" />,
};

const TIER_NAMES: Record<number, string> = {
  1: '基础', 2: '标准', 3: '进阶', 4: '深度分析', 5: '全盘推演',
};

interface PricingTiersProps {
  activeTier: number | null;
  onSelectTier: (tier: number) => void;
}

export function PricingTiers({ activeTier, onSelectTier }: PricingTiersProps) {
  const tiers = getTierConfigs();

  return (
    <div className="glass-card rounded-2xl p-5 sm:p-6">
      {/* Header */}
      <div className="mb-5">
        <h3 className="text-sm font-semibold text-foreground">推演方案</h3>
        <p className="mt-0.5 text-xs text-[oklch(0.45_0.02_265)]">选择推演深度</p>
      </div>

      <ScrollArea className="w-full pb-2">
        <div className="flex gap-3 pb-2" style={{ minWidth: 'max-content' }}>
          {tiers.map((tier, idx) => {
            const isActive = activeTier === tier.tier;
            const isFree = tier.cost === 0;
            return (
              <motion.button
                key={tier.tier}
                initial={{ opacity: 0, y: 12 }}
                animate={{ opacity: isActive ? 1 : 0.5, y: 0 }}
                transition={{ duration: 0.25, delay: idx * 0.05 }}
                onClick={() => onSelectTier(tier.tier)}
                className={cn(
                  'relative flex w-[180px] shrink-0 flex-col items-center rounded-xl border p-4 text-left transition-all duration-300 cursor-pointer hover:opacity-100',
                  isActive
                    ? 'border-[oklch(0.78_0.145_85_/30%)] bg-[oklch(0.78_0.145_85_/5%)] shadow-lg shadow-[oklch(0.78_0.145_85_/8%)]'
                    : 'border-[oklch(1_0_0_/6%)] bg-[oklch(0.12_0.015_265)] hover:border-[oklch(0.78_0.145_85_/15%)]'
                )}
              >
                {/* Active indicator */}
                {isActive && (
                  <motion.div
                    layoutId="activeTierPill"
                    className="absolute -top-1.5 left-1/2 -translate-x-1/2 rounded-full bg-[oklch(0.78_0.145_85)] px-2.5 py-0.5 text-[9px] font-bold text-[oklch(0.12_0.02_265)] shadow-sm"
                  >
                    已选
                  </motion.div>
                )}
                {tier.tier === 3 && !isActive && (
                  <motion.div
                    initial={{ opacity: 0, scale: 0.8 }}
                    animate={{ opacity: 1, scale: 1 }}
                    className="absolute -top-1.5 left-1/2 -translate-x-1/2 rounded-full bg-gradient-to-r from-amber-500 to-amber-400 px-2.5 py-0.5 text-[9px] font-bold text-black shadow-sm"
                  >
                    推荐
                  </motion.div>
                )}

                {/* Icon + Name */}
                <div className={cn('mb-3 flex items-center gap-2', isActive ? 'text-[oklch(0.78_0.145_85)]' : 'text-[oklch(0.60_0.02_265)]')}>
                  {TIER_ICONS[tier.tier]}
                  <div>
                    <div className="text-xs font-bold">{TIER_NAMES[tier.tier]}</div>
                    <div className="text-[10px] opacity-60">Tier {tier.tier}</div>
                  </div>
                </div>

                {/* Description */}
                <p className="mb-3 text-[11px] text-[oklch(0.45_0.02_265)] leading-relaxed text-center">
                  {tier.label}
                </p>

                <Separator className="mb-3 bg-[oklch(1_0_0_/6%)]" />

                {/* Methods */}
                <div className="mb-3 flex flex-wrap justify-center gap-1">
                  {tier.methods.map((method) => (
                    <Badge
                      key={method}
                      variant="outline"
                      className={cn(
                        'gap-0.5 text-[10px] border-[oklch(1_0_0_/8%)] text-[oklch(0.50_0.02_265)]',
                        isActive && 'border-[oklch(0.78_0.145_85_/20%)] text-[oklch(0.78_0.145_85)]'
                      )}
                    >
                      {METHOD_LABELS[method]?.icon}
                      {METHOD_LABELS[method]?.label}
                    </Badge>
                  ))}
                </div>

                {/* Stats */}
                <div className="w-full space-y-1.5">
                  <div className="flex items-center justify-between text-[11px]">
                    <span className="text-[oklch(0.40_0.02_265)]">Cost</span>
                    <span className={cn('font-mono font-bold', isFree ? 'text-[oklch(0.72_0.16_145)]' : 'text-foreground')}>
                      {isFree ? '免费' : `$${tier.cost.toFixed(2)}`}
                    </span>
                  </div>
                  <div className="flex items-center justify-between text-[11px]">
                    <span className="text-[oklch(0.40_0.02_265)]">Time</span>
                    <span className="text-foreground">{tier.time}</span>
                  </div>
                </div>

                {/* Select dot */}
                <div className={cn(
                  'mt-3 mx-auto flex h-5 w-5 items-center justify-center rounded-full border-2 transition-colors',
                  isActive
                    ? 'border-[oklch(0.78_0.145_85)] bg-[oklch(0.78_0.145_85)] text-[oklch(0.12_0.02_265)]'
                    : 'border-[oklch(1_0_0_/10%)]'
                )}>
                  {isActive && <Check className="size-3" />}
                </div>
              </motion.button>
            );
          })}
        </div>
        <ScrollBar orientation="horizontal" />
      </ScrollArea>
    </div>
  );
}