'use client';

import React from 'react';
import { motion } from 'framer-motion';
import { Button } from '@/components/ui/button';
import {
  Sparkles,
  Zap,
  ShieldCheck,
  Users,
  Brain,
  ArrowRight,
  Star,
  Code2,
} from 'lucide-react';
import { cn } from '@/lib/utils';

interface LandingHeroProps {
  onStartFreeReading?: () => void;
  onViewPricing?: () => void;
}

const FEATURES = [
  {
    icon: <Zap className="size-4" />,
    title: 'BaZi Engine',
    desc: 'Deterministic Four Pillars calculation — instant, accurate, verifiable.',
  },
  {
    icon: <Brain className="size-4" />,
    title: 'Smart Routing',
    desc: 'AI classifies your question and routes to the optimal prediction method.',
  },
  {
    icon: <Users className="size-4" />,
    title: 'Multi-Agent Debate',
    desc: 'Complex questions analyzed by AI agents reaching consensus through deliberation.',
  },
  {
    icon: <ShieldCheck className="size-4" />,
    title: 'Verifiable Trust',
    desc: 'Every prediction can be verified. Track accuracy with full transparency.',
  },
  {
    icon: <Sparkles className="size-4" />,
    title: '5-Tier Pricing',
    desc: 'Free basic lookups to deep destiny readings — pay only for what you need.',
  },
  {
    icon: <Code2 className="size-4" />,
    title: 'Open Client',
    desc: 'Chart engine is open-source. Verify the math. AI reasoning stays proprietary.',
  },
];

export function LandingHero({ onStartFreeReading, onViewPricing }: LandingHeroProps) {
  return (
    <div className="relative flex min-h-screen flex-col items-center overflow-hidden">
      {/* Cosmic Background */}
      <div className="pointer-events-none fixed inset-0">
        {/* Deep space base */}
        <div className="absolute inset-0 bg-background" />
        {/* Star field */}
        <div className="absolute inset-0 star-field" />
        {/* Subtle gold radial glow at center top */}
        <div
          className="absolute inset-0 opacity-30"
          style={{
            background: 'radial-gradient(ellipse 60% 40% at 50% 20%, oklch(0.78 0.145 85 / 0.12), transparent 70%)',
          }}
        />
        {/* Secondary glow bottom-left */}
        <motion.div
          animate={{ opacity: [0.15, 0.25, 0.15] }}
          transition={{ duration: 8, repeat: Infinity, ease: 'easeInOut' }}
          className="absolute -bottom-1/4 -left-1/4 size-[600px] rounded-full opacity-20"
          style={{ background: 'radial-gradient(circle, oklch(0.65 0.10 280 / 0.15), transparent 60%)' }}
        />
        {/* Tertiary glow top-right */}
        <motion.div
          animate={{ opacity: [0.1, 0.2, 0.1] }}
          transition={{ duration: 10, repeat: Infinity, ease: 'easeInOut', delay: 3 }}
          className="absolute -top-1/4 -right-1/4 size-[500px] rounded-full"
          style={{ background: 'radial-gradient(circle, oklch(0.68 0.14 350 / 0.1), transparent 60%)' }}
        />
      </div>

      {/* Content */}
      <div className="relative z-10 flex flex-1 flex-col items-center justify-center px-4 py-20">
        <div className="mx-auto max-w-2xl text-center">
          {/* Brand Mark */}
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="mb-8 flex items-center justify-center gap-2.5"
          >
            <div className="flex size-9 items-center justify-center rounded-xl border border-[oklch(1_0_0_/8%)] bg-[oklch(0.14_0.015_265)]">
              <Star className="size-4 text-[oklch(0.78_0.145_85)]" />
            </div>
            <span className="text-sm font-semibold tracking-widest text-[oklch(0.60_0.02_265)] uppercase">
              OracleMind
            </span>
          </motion.div>

          {/* Main Headline */}
          <motion.h1
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.7, delay: 0.1 }}
            className="text-4xl font-bold tracking-tight sm:text-5xl lg:text-6xl"
          >
            <span className="text-foreground">推演你的人生概率</span>
            <br />
            <span className="gold-glow bg-gradient-to-r from-[oklch(0.78_0.145_85)] via-[oklch(0.85_0.14_75)] to-[oklch(0.78_0.145_85)] bg-clip-text text-transparent">
              AI × 八字命理
            </span>
          </motion.h1>

          {/* Subheadline */}
          <motion.p
            initial={{ opacity: 0, y: 15 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="mx-auto mt-5 max-w-md text-sm leading-relaxed text-[oklch(0.55_0.02_265)] sm:text-base"
          >
            八字命理 × 多Agent AI辩论 × 概率化预测
            不是算命，是概率推演——给你置信区间，你自己决定。
          </motion.p>

          {/* CTA Buttons */}
          <motion.div
            initial={{ opacity: 0, y: 15 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.35 }}
            className="mt-8 flex flex-col items-center gap-3 sm:flex-row sm:justify-center"
          >
            <Button
              size="lg"
              onClick={onStartFreeReading}
              className="h-11 gap-2 rounded-xl border border-[oklch(0.78_0.145_85)] bg-[oklch(0.78_0.145_85)] px-7 text-sm font-semibold text-[oklch(0.12_0.02_265)] shadow-lg shadow-[oklch(0.78_0.145_85_/15%)] transition-all hover:shadow-[oklch(0.78_0.145_85_/25%)] hover:bg-[oklch(0.82_0.14_85)]"
            >
              <Sparkles className="size-4" />
              Start Free Reading
              <ArrowRight className="size-3.5" />
            </Button>
            <Button
              variant="ghost"
              size="lg"
              onClick={onViewPricing}
              className="h-11 gap-2 rounded-xl px-7 text-sm font-medium text-[oklch(0.60_0.02_265)] transition-colors hover:text-foreground"
            >
              View Pricing
            </Button>
          </motion.div>

          {/* Trust Indicators */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.6, delay: 0.55 }}
            className="mt-14 flex items-center justify-center gap-8 text-xs text-[oklch(0.50_0.02_265)]"
          >
            <div className="text-center">
              <div className="text-lg font-bold text-foreground">10,000+</div>
              <div>Charts Generated</div>
            </div>
            <div className="h-8 w-px bg-[oklch(1_0_0_/8%)]" />
            <div className="text-center">
              <div className="text-lg font-bold text-foreground">87%</div>
              <div>Verification Rate</div>
            </div>
            <div className="h-8 w-px bg-[oklch(1_0_0_/8%)]" />
            <div className="text-center">
              <div className="text-lg font-bold text-foreground">3</div>
              <div>推演方法</div>
            </div>
          </motion.div>
        </div>
      </div>

      {/* Features Grid */}
      <div className="relative z-10 w-full max-w-4xl px-4 pb-16 sm:pb-24">
        <motion.h2
          initial={{ opacity: 0, y: 15 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.6 }}
          className="mb-8 text-center text-xs font-semibold uppercase tracking-[0.2em] text-[oklch(0.45_0.02_265)]"
        >
          How It Works
        </motion.h2>
        <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
          {FEATURES.map((feat, idx) => (
            <motion.div
              key={feat.title}
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.4, delay: 0.65 + idx * 0.07 }}
              className={cn(
                'group rounded-xl border border-[oklch(1_0_0_/6%)] bg-[oklch(0.12_0.015_265)] p-4 transition-all duration-300',
                'hover:border-[oklch(0.78_0.145_85_/20%)] hover:bg-[oklch(0.14_0.015_265)]'
              )}
            >
              <div className="mb-2.5 flex size-8 items-center justify-center rounded-lg text-[oklch(0.78_0.145_85)] transition-colors group-hover:bg-[oklch(0.78_0.145_85_/10%)]">
                {feat.icon}
              </div>
              <h3 className="mb-1 text-sm font-semibold text-foreground">{feat.title}</h3>
              <p className="text-xs leading-relaxed text-[oklch(0.50_0.02_265)]">{feat.desc}</p>
            </motion.div>
          ))}
        </div>
      </div>

      {/* Footer */}
      <footer className="relative z-10 w-full border-t border-[oklch(1_0_0_/6%)] py-6">
        <div className="mx-auto flex max-w-4xl flex-col items-center gap-3 px-4 sm:flex-row sm:justify-between">
          <div className="flex items-center gap-1.5 text-xs text-[oklch(0.40_0.02_265)]">
            <Star className="size-3" />
            <span>OracleMind &copy; {new Date().getFullYear()}</span>
          </div>
          <div className="flex items-center gap-4 text-[11px] text-[oklch(0.40_0.02_265)]">
            <span className="flex items-center gap-1">
              <Code2 className="size-3" /> Open Source Engine
            </span>
            <span className="flex items-center gap-1">
              <Sparkles className="size-3" /> AI驱动
            </span>
          </div>
        </div>
      </footer>
    </div>
  );
}