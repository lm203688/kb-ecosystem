'use client';
import { useState, useEffect } from 'react';
import { Card } from '@/components/ui/card';
import { PredictionTracker, type PredictionRecord } from '@/lib/prediction-tracker';

export function PredictionHistory() {
  const [records, setRecords] = useState<PredictionRecord[]>([]);
  const [stats, setStats] = useState({ total:0, verified:0, avgAccuracy:0, calibration:0 });
  
  useEffect(() => {
    setRecords(PredictionTracker.getAll());
    setStats(PredictionTracker.getStats());
  }, []);
  
  if (records.length === 0) {
    return (
      <Card className="p-4 text-center text-sm text-muted-foreground">
        暂无预测记录 · 运行预测后将自动保存
      </Card>
    );
  }
  
  return (
    <div className="space-y-3">
      <Card className="p-4 space-y-2">
        <h3 className="font-semibold text-sm">预测准确度追踪</h3>
        <div className="grid grid-cols-4 gap-2 text-center text-xs">
          <div><div className="font-bold text-lg">{stats.total}</div><div className="text-muted-foreground">总预测</div></div>
          <div><div className="font-bold text-lg">{stats.verified}</div><div className="text-muted-foreground">已验证</div></div>
          <div><div className="font-bold text-lg">{(stats.avgAccuracy*100).toFixed(0)}%</div><div className="text-muted-foreground">平均准确度</div></div>
          <div><div className="font-bold text-lg">{(stats.calibration*100).toFixed(0)}%</div><div className="text-muted-foreground">校准度</div></div>
        </div>
      </Card>
      
      <Card className="p-4 space-y-2">
        <h4 className="font-semibold text-sm">历史预测</h4>
        {records.slice(0, 10).map(r => (
          <div key={r.id} className="flex justify-between items-center text-xs border-b border-border pb-1">
            <span>{r.date.slice(0,10)} · {r.input?.target}</span>
            <span className="font-mono">{(r.result?.final?.probability*100).toFixed(0)}%</span>
            {r.actualOutcome && (
              <span className={r.accuracy > 0.7 ? 'text-green-600' : r.accuracy > 0.4 ? 'text-yellow-600' : 'text-red-600'}>
                {(r.accuracy*100).toFixed(0)}%
              </span>
            )}
          </div>
        ))}
      </Card>
    </div>
  );
}
