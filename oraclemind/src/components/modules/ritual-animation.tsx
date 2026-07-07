'use client';

import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

interface RitualAnimationProps {
  isActive: boolean;
  onComplete: () => void;
  steps?: string[];
}

const DEFAULT_STEPS = [
  '排列八字命盘',
  '推算大运流年',
  '分析五行强弱',
  '多Agent辩论中',
  '生成概率推演',
];

export function RitualAnimation({ isActive, onComplete, steps = DEFAULT_STEPS }: RitualAnimationProps) {
  const [currentStep, setCurrentStep] = useState(0);

  useEffect(() => {
    if (!isActive) {
      setCurrentStep(0);
      return;
    }

    if (currentStep >= steps.length) {
      const timer = setTimeout(() => onComplete(), 500);
      return () => clearTimeout(timer);
    }

    const timer = setTimeout(() => {
      setCurrentStep(prev => prev + 1);
    }, 600);

    return () => clearTimeout(timer);
  }, [isActive, currentStep, steps.length, onComplete]);

  if (!isActive) return null;

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-md"
    >
      <div className="text-center">
        {/* 旋转八卦图 */}
        <motion.div
          animate={{ rotate: 360 }}
          transition={{ duration: 3, repeat: Infinity, ease: 'linear' }}
          className="mx-auto mb-8 text-6xl"
        >
          ☯
        </motion.div>

        <motion.h2
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          className="mb-6 text-2xl font-serif text-amber-100"
        >
          正在起卦
        </motion.h2>

        {/* 步骤进度 */}
        <div className="space-y-3">
          {steps.map((step, idx) => (
            <motion.div
              key={idx}
              initial={{ x: -20, opacity: 0 }}
              animate={{
                x: 0,
                opacity: idx < currentStep ? 1 : idx === currentStep ? 0.7 : 0.3,
              }}
              transition={{ delay: idx * 0.1 }}
              className="flex items-center justify-center gap-3"
            >
              <span className="text-amber-200">
                {idx < currentStep ? '✓' : idx === currentStep ? '◉' : '○'}
              </span>
              <span className={idx < currentStep ? 'text-amber-100' : 'text-amber-200/50'}>
                {step}
              </span>
            </motion.div>
          ))}
        </div>

        {/* 进度条 */}
        <motion.div
          className="mx-auto mt-8 h-1 w-64 overflow-hidden rounded-full bg-amber-900/30"
        >
          <motion.div
            animate={{ width: `${(currentStep / steps.length) * 100}%` }}
            transition={{ duration: 0.5 }}
            className="h-full bg-gradient-to-r from-amber-400 to-amber-200"
          />
        </motion.div>
      </div>
    </motion.div>
  );
}
