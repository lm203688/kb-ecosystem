'use client';

import { motion } from 'framer-motion';

interface StepIndicatorProps {
  currentStep: number; // 0-indexed
  steps?: string[];
}

const DEFAULT_STEPS = ['输入信息', 'AI推演中', '查看结果'];

export function StepIndicator({ currentStep, steps = DEFAULT_STEPS }: StepIndicatorProps) {
  return (
    <div className="flex items-center justify-center gap-2 py-4">
      {steps.map((step, idx) => (
        <div key={idx} className="flex items-center">
          {/* 圆点 */}
          <motion.div
            initial={false}
            animate={{
              scale: idx === currentStep ? 1.2 : 1,
              backgroundColor: idx <= currentStep ? 'rgb(251 191 36)' : 'rgb(120 53 15)',
            }}
            className="flex h-8 w-8 items-center justify-center rounded-full text-sm font-medium"
          >
            <span className={idx <= currentStep ? 'text-black' : 'text-amber-200/50'}>
              {idx < currentStep ? '✓' : idx + 1}
            </span>
          </motion.div>

          {/* 标签 */}
          <span
            className={`ml-2 text-sm ${
              idx === currentStep
                ? 'font-medium text-amber-100'
                : idx < currentStep
                ? 'text-amber-200/70'
                : 'text-amber-200/30'
            }`}
          >
            {step}
          </span>

          {/* 连接线 */}
          {idx < steps.length - 1 && (
            <div className="mx-3 h-px w-12 bg-amber-900/30">
              <motion.div
                initial={false}
                animate={{ width: idx < currentStep ? '100%' : '0%' }}
                transition={{ duration: 0.3 }}
                className="h-full bg-amber-400"
              />
            </div>
          )}
        </div>
      ))}
    </div>
  );
}
