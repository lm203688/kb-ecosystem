'use client';
import { Card } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { Badge } from '@/components/ui/badge';

export function PredictionResult({ result }: { result: any }) {
  if (!result) return null;
  const { final: f, layers, meta } = result;
  return (
    <div className="space-y-4">
      <Card className="p-6 text-center space-y-3">
        <h3 className="text-lg font-bold">概率预测结果</h3>
        <div className="text-4xl font-bold" style={{color: f.probability>0.6?'#10b981':f.probability>0.4?'#f59e0b':'#ef4444'}}>
          {(f.probability*100).toFixed(1)}%
        </div>
        <div className="text-sm text-muted-foreground">{f.outcome}</div>
        <div className="text-xs text-muted-foreground">
          95% CI: [{(f.ci_low*100).toFixed(0)}%, {(f.ci_high*100).toFixed(0)}%] · 置信度: {(f.confidence*100).toFixed(0)}%
        </div>
        <Progress value={f.probability*100} className="h-2" />
        <div className="text-sm p-3 rounded-lg bg-muted">{f.recommendation}</div>
      </Card>
      {layers.map((layer: any, i: number) => (
        <Card key={i} className="p-4 space-y-2">
          <div className="flex justify-between items-center">
            <span className="font-semibold text-sm">第{layer.layer}层：{layer.layerName}</span>
            <Badge variant="outline">{(layer.confidence*100).toFixed(0)}%</Badge>
          </div>
          <p className="text-xs text-muted-foreground">{layer.method}</p>
          {layer.predictions.map((p: any, j: number) => (
            <div key={j} className="text-xs">
              <div className="flex justify-between"><span>{p.outcome}</span><span className="font-mono">{(p.probability*100).toFixed(1)}%</span></div>
              <Progress value={p.probability*100} className="h-1" />
            </div>
          ))}
          {layer.consensus !== undefined && <div className="text-xs text-muted-foreground">共识度: {(layer.consensus*100).toFixed(0)}%</div>}
        </Card>
      ))}
      <div className="text-xs text-muted-foreground p-2 rounded border-l-4 border-amber-400 bg-amber-50 dark:bg-amber-950/20">
        {meta.methods.join(' + ')} · {meta.total_simulations}次模拟 · {meta.computation_time}ms
        <br />⚠️ {meta.disclaimer}
      </div>
    </div>
  );
}
