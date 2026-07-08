'use client';
import { useState } from 'react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';

export function PredictionForm({ onPredict, loading }: { onPredict: (input: any) => void; loading: boolean }) {
  const [input, setInput] = useState({ birthYear:1990, birthMonth:1, birthDay:1, birthHour:12, gender:'male', target:'overall', timeframe:5 });
  return (
    <Card className="p-4 space-y-3">
      <h3 className="font-semibold">概率预测输入</h3>
      <div className="grid grid-cols-4 gap-2">
        {[['birthYear','年'],['birthMonth','月'],['birthDay','日'],['birthHour','时']].map(([k,l]) => (
          <div key={k}><label className="text-xs text-muted-foreground">{l}</label>
          <Input type="number" value={(input as any)[k]} onChange={e => setInput({...input,[k]:+e.target.value})} className="h-8" /></div>
        ))}
      </div>
      <div className="grid grid-cols-3 gap-2">
        <select className="border rounded p-1 text-sm" value={input.gender} onChange={e=>setInput({...input,gender:e.target.value})}>
          <option value="male">男</option><option value="female">女</option>
        </select>
        <select className="border rounded p-1 text-sm" value={input.target} onChange={e=>setInput({...input,target:e.target.value})}>
          <option value="overall">整体</option><option value="career">事业</option><option value="wealth">财运</option>
          <option value="love">感情</option><option value="health">健康</option><option value="event">事件</option>
        </select>
        <select className="border rounded p-1 text-sm" value={input.timeframe} onChange={e=>setInput({...input,timeframe:+e.target.value})}>
          <option value={1}>1年</option><option value={3}>3年</option><option value={5}>5年</option><option value={10}>10年</option>
        </select>
      </div>
      <Button onClick={() => onPredict(input)} disabled={loading} className="w-full">
        {loading ? '推演中(10000次模拟)...' : '运行三层概率推演'}
      </Button>
    </Card>
  );
}
