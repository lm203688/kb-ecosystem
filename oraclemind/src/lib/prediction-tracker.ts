/**
 * 预测追踪+回测系统
 * 记录历史预测，追踪准确度，提供预测校准
 */

export interface PredictionRecord {
  id: string;
  date: string;
  input: any;
  result: any;
  actualOutcome?: 'positive' | 'neutral' | 'negative';
  actualNote?: string;
  accuracy?: number; // 预测vs实际偏差
}

const STORAGE_KEY = 'oraclemind_predictions';

export class PredictionTracker {
  static getAll(): PredictionRecord[] {
    if (typeof window === 'undefined') return [];
    try {
      return JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]');
    } catch { return []; }
  }
  
  static save(record: PredictionRecord): void {
    if (typeof window === 'undefined') return;
    const all = this.getAll();
    all.unshift(record);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(all.slice(0, 50)));
  }
  
  static updateActual(id: string, outcome: 'positive'|'neutral'|'negative', note: string): void {
    const all = this.getAll();
    const rec = all.find(r => r.id === id);
    if (rec) {
      rec.actualOutcome = outcome;
      rec.actualNote = note;
      // 计算准确度
      const predicted = rec.result?.final?.probability || 0.5;
      const actual = outcome === 'positive' ? 0.8 : outcome === 'neutral' ? 0.5 : 0.2;
      rec.accuracy = 1 - Math.abs(predicted - actual);
      localStorage.setItem(STORAGE_KEY, JSON.stringify(all));
    }
  }
  
  static getStats(): { total: number; verified: number; avgAccuracy: number; calibration: number } {
    const all = this.getAll();
    const verified = all.filter(r => r.actualOutcome);
    const avgAccuracy = verified.length > 0
      ? verified.reduce((s, r) => s + (r.accuracy || 0), 0) / verified.length
      : 0;
    // 校准度：预测概率与实际频率的差异
    const calibration = verified.length > 0
      ? 1 - Math.abs(verified.filter(r => r.result?.final?.probability > 0.5).length / verified.length -
                    verified.filter(r => r.actualOutcome === 'positive').length / verified.length)
      : 1;
    return { total: all.length, verified: verified.length, avgAccuracy, calibration };
  }
  
  static getTimeline(): { date: string; probability: number; target: string }[] {
    return this.getAll().map(r => ({
      date: r.date,
      probability: r.result?.final?.probability || 0,
      target: r.input?.target || 'overall',
    }));
  }
}
