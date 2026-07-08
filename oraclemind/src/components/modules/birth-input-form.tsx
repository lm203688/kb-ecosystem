'use client';

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Calendar } from '@/components/ui/calendar';
import { Popover, PopoverContent, PopoverTrigger } from '@/components/ui/popover';
import { CalendarIcon, Loader2, MapPin, Clock } from 'lucide-react';
import { format } from 'date-fns';
import { cn } from '@/lib/utils';

export interface BirthFormData {
  year: number;
  month: number;
  day: number;
  hour: number;
  gender: 'male' | 'female';
  place: string;
}

const TWO_HOUR_PERIODS = [
  { label: '子', pinyin: 'Zi', range: '23:00–01:00', value: 23 },
  { label: '丑', pinyin: 'Chou', range: '01:00–03:00', value: 1 },
  { label: '寅', pinyin: 'Yin', range: '03:00–05:00', value: 3 },
  { label: '卯', pinyin: 'Mao', range: '05:00–07:00', value: 5 },
  { label: '辰', pinyin: 'Chen', range: '07:00–09:00', value: 7 },
  { label: '巳', pinyin: 'Si', range: '09:00–11:00', value: 9 },
  { label: '午', pinyin: 'Wu', range: '11:00–13:00', value: 11 },
  { label: '未', pinyin: 'Wei', range: '13:00–15:00', value: 13 },
  { label: '申', pinyin: 'Shen', range: '15:00–17:00', value: 15 },
  { label: '酉', pinyin: 'You', range: '17:00–19:00', value: 17 },
  { label: '戌', pinyin: 'Xu', range: '19:00–21:00', value: 19 },
  { label: '亥', pinyin: 'Hai', range: '21:00–23:00', value: 21 },
];

interface BirthInputFormProps {
  onSubmit: (data: BirthFormData) => void;
  isLoading: boolean;
}

export function BirthInputForm({ onSubmit, isLoading }: BirthInputFormProps) {
  const [date, setDate] = useState<Date | undefined>(undefined);
  const [selectedHour, setSelectedHour] = useState<number>(12);
  const [gender, setGender] = useState<'male' | 'female'>('male');
  const [place, setPlace] = useState('');
  const [dateOpen, setDateOpen] = useState(false);

  const handleSubmit = () => {
    if (!date) return;
    onSubmit({
      year: date.getFullYear(),
      month: date.getMonth() + 1,
      day: date.getDate(),
      hour: selectedHour,
      gender,
      place,
    });
  };

  const isValid = date !== undefined;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="glass-card mx-auto w-full max-w-md rounded-2xl p-6 sm:p-8"
    >
      {/* Title */}
      <div className="mb-6 text-center">
        <h2 className="text-lg font-semibold text-foreground">
          Enter Birth Details
        </h2>
        <p className="mt-1 text-xs text-[oklch(0.50_0.02_265)]">
          Provide your birth information for BaZi chart generation
        </p>
      </div>

      <div className="space-y-5">
        {/* Date Picker */}
        <div className="space-y-2">
          <Label className="text-xs font-medium text-[oklch(0.60_0.02_265)]">
            Birth Date
          </Label>
          <Popover open={dateOpen} onOpenChange={setDateOpen}>
            <PopoverTrigger asChild>
              <Button
                variant="outline"
                className={cn(
                  'w-full justify-start border-[oklch(1_0_0_/8%)] bg-[oklch(0.12_0.015_265)] text-left font-normal hover:border-[oklch(0.78_0.145_85_/20%)] hover:bg-[oklch(0.14_0.015_265)]',
                  !date && 'text-[oklch(0.50_0.02_265)]'
                )}
              >
                <CalendarIcon className="mr-2 size-4 text-[oklch(0.50_0.02_265)]" />
                {date ? format(date, 'yyyy-MM-dd') : 'Select date'}
              </Button>
            </PopoverTrigger>
            <PopoverContent className="w-auto p-0 border-[oklch(1_0_0_/8%)] bg-[oklch(0.14_0.015_265)]" align="start">
              <Calendar
                mode="single"
                selected={date}
                onSelect={(d) => {
                  setDate(d);
                  setDateOpen(false);
                }}
                defaultMonth={date}
                disabled={(d) => d > new Date() || d < new Date('1900-01-01')}
                captionLayout="dropdown"
                fromYear={1920}
                toYear={new Date().getFullYear()}
              />
            </PopoverContent>
          </Popover>
        </div>

        {/* Hour Selector */}
        <div className="space-y-2">
          <Label className="text-xs font-medium text-[oklch(0.60_0.02_265)]">
            Birth Hour
          </Label>
          <div className="grid grid-cols-6 gap-1.5">
            {TWO_HOUR_PERIODS.map((period) => {
              const isSelected = selectedHour === period.value;
              return (
                <button
                  key={period.value}
                  type="button"
                  onClick={() => setSelectedHour(period.value)}
                  className={cn(
                    'flex flex-col items-center gap-0.5 rounded-lg border px-1 py-2 text-xs transition-all duration-200',
                    isSelected
                      ? 'border-[oklch(0.78_0.145_85)] bg-[oklch(0.78_0.145_85_/10%)] text-[oklch(0.78_0.145_85)] shadow-sm shadow-[oklch(0.78_0.145_85_/10%)]'
                      : 'border-[oklch(1_0_0_/6%)] bg-transparent text-[oklch(0.50_0.02_265)] hover:border-[oklch(1_0_0_/12%)] hover:text-[oklch(0.70_0.02_265)]'
                  )}
                >
                  <span className="text-sm font-bold">{period.label}</span>
                  <span className="text-[9px]">{period.pinyin}</span>
                </button>
              );
            })}
          </div>
        </div>

        {/* Gender Toggle */}
        <div className="space-y-2">
          <Label className="text-xs font-medium text-[oklch(0.60_0.02_265)]">
            Gender
          </Label>
          <div className="grid grid-cols-2 gap-2">
            {([
              { g: 'male' as const, label: '男 Male' },
              { g: 'female' as const, label: '女 Female' },
            ]).map(({ g, label }) => {
              const isSelected = gender === g;
              return (
                <button
                  key={g}
                  type="button"
                  onClick={() => setGender(g)}
                  className={cn(
                    'rounded-lg border px-4 py-2.5 text-sm font-medium transition-all duration-200',
                    isSelected
                      ? 'border-[oklch(0.78_0.145_85)] bg-[oklch(0.78_0.145_85_/10%)] text-[oklch(0.78_0.145_85)]'
                      : 'border-[oklch(1_0_0_/6%)] text-[oklch(0.50_0.02_265)] hover:border-[oklch(1_0_0_/12%)] hover:text-[oklch(0.70_0.02_265)]'
                  )}
                >
                  {label}
                </button>
              );
            })}
          </div>
        </div>

        {/* Birthplace */}
        <div className="space-y-2">
          <Label className="text-xs font-medium text-[oklch(0.60_0.02_265)]">
            Birthplace
            <span className="ml-1.5 font-normal text-[oklch(0.40_0.02_265)]">(optional)</span>
          </Label>
          <div className="relative">
            <MapPin className="absolute left-3 top-1/2 -translate-y-1/2 size-3.5 text-[oklch(0.40_0.02_265)]" />
            <Input
              placeholder="e.g. Beijing"
              value={place}
              onChange={(e) => setPlace(e.target.value)}
              className="border-[oklch(1_0_0_/8%)] bg-[oklch(0.12_0.015_265)] pl-9 text-sm placeholder:text-[oklch(0.40_0.02_265)] hover:border-[oklch(1_0_0_/12%)] focus:border-[oklch(0.78_0.145_85)]"
            />
          </div>
        </div>

        {/* Submit */}
        <Button
          onClick={handleSubmit}
          disabled={!isValid || isLoading}
          className={cn(
            'w-full h-11 gap-2 rounded-xl text-sm font-semibold transition-all',
            isValid && !isLoading
              ? 'bg-[oklch(0.78_0.145_85)] text-[oklch(0.12_0.02_265)] shadow-lg shadow-[oklch(0.78_0.145_85_/15%)] hover:shadow-[oklch(0.78_0.145_85_/25%)] hover:bg-[oklch(0.82_0.14_85)]'
              : ''
          )}
        >
          {isLoading ? (
            <>
              <Loader2 className="size-4 animate-spin" />
              Generating...
            </>
          ) : (
            <>
              <Clock className="size-4" />
              Generate Chart
            </>
          )}
        </Button>
      </div>
    </motion.div>
  );
}