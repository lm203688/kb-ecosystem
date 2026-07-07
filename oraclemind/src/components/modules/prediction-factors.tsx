'use client';
import { Card } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { Info } from 'lucide-react';

export function PredictionFactors({ result }: { result: any }) {
  if (!result?.layers) return null;
  
  return (
    <Card className="p-4 space-y-3">
      <div className="flex items-center gap-2">
        <Info className="size-4 text-primary" />
        <h3 className="font-semibold text-sm">预测因子分析</h3>
      </div>
      <p className="text-xs text-muted-foreground">影响预测结果的关键因素及其权重</p>
      
      {result.layers.map((layer: any, i: number) => (
        <div key={i} className="space-y-1">
          <div className="text-xs font-medium text-muted-foreground">第{layer.layer}层 {layer.layerName}</div>
          {layer.predictions?.flatMap((p: any) => p.factors || []).map((f: any, j: number) => (
            <div key={j} className="flex items-center gap-2 text-xs">
              <span className="w-24 truncate">{f.name}</span>
              <Progress value={f.weight * 100} className="h-1 flex-1" />
              <span className={`w-12 text-right ${f.direction === 'positive' ? 'text-green-600' : f.direction === 'negative' ? 'text-red-600' : 'text-muted-foreground'}`}>
                {f.direction === 'positive' ? '+' : f.direction === 'negative' ? '-' : '~'}{(f.weight * 100).toFixed(0)}%
              </span>
            </div>
          ))}
        </div>
      ))}
      
      {/* 置信区间教育 */}
      <div className="p-2 rounded-lg bg-blue-50 dark:bg-blue-950/20 text-xs space-y-1">
        <div className="font-medium">📊 如何理解这个预测？</div>
        <div>• 概率{(result.final.probability*100).toFixed(0)}%：模拟10000次中约{((result.final.probability)*100).toFixed(0)}%的结果指向此方向</div>
        <div>• 95%置信区间[{(result.final.ci_low*100).toFixed(0)}%, {(result.final.ci_high*100).toFixed(0)}%]：真实值有95%的概率落在此范围</div>
        <div>• 共识度{(result.final.confidence*100).toFixed(0)}%：4个Agent的预测一致程度，越高越可信</div>
      </div>
    </Card>
  );
}
