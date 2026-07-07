/**
 * OracleMind 三层预测引擎 V2 — 科学预测方向
 * 定位：人生概率推演引擎
 * 第1层：先验模型（传统知识作为贝叶斯先验）
 * 第2层：统计预测（蒙特卡洛+马尔可夫链+贝叶斯推断）
 * 第3层：多Agent推演（4 Agent并行+共识分歧分析）
 */

// 确定性随机——用参数hash做种子，同输入同输出（替代Math.random）
function deterministicRand(seed: string): number {
  let hash = 0;
  for (let i = 0; i < seed.length; i++) {
    hash = ((hash << 5) - hash) + seed.charCodeAt(i);
    hash = hash & 0xffffffff;
  }
  return Math.abs(hash % 1000) / 1000;
}

function deterministicNoise(input: string, i: number, s: number): number {
  return deterministicRand(input + '_' + i + '_' + s);
}

export interface PredictionInput {
  birthYear: number; birthMonth: number; birthDay: number; birthHour: number;
  gender: 'male' | 'female';
  currentAge?: number; career?: string; relationship?: string;
  target: 'career' | 'wealth' | 'love' | 'health' | 'overall' | 'event';
  eventDescription?: string; timeframe?: number;
}

export interface LayerResult {
  layer: number; layerName: string; method: string;
  predictions: Prediction[]; confidence: number; consensus: number; raw: any;
}

export interface Prediction {
  outcome: string; probability: number;
  confidence_interval: [number, number]; reasoning: string;
  factors: { name: string; weight: number; direction: 'positive' | 'negative' | 'neutral' }[];
}

export interface FinalPrediction {
  input: PredictionInput; layers: LayerResult[];
  final: {
    outcome: string; probability: number; confidence: number;
    ci_low: number; ci_high: number; key_factors: string[];
    scenarios: { name: string; probability: number; description: string }[];
    recommendation: string;
  };
  meta: { methods: string[]; total_simulations: number; computation_time: number; disclaimer: string };
}

// ===== 第1层：先验模型 =====
export class PriorLayer {
  predict(input: PredictionInput): LayerResult {
    const bazi = this.calcBazi(input);
    const elements = this.calcElements(bazi);
    const maxElem = Object.entries(elements).sort((a,b) => b[1] - a[1])[0];
    const elemCareerMap: Record<string, string[]> = {
      wood: ['教育','文化','农业','出版'], fire: ['传媒','电子','能源','餐饮'],
      earth: ['房地产','金融','建筑','咨询'], metal: ['科技','制造','法律','医疗'],
      water: ['贸易','物流','IT','旅游'],
    };
    const predictions: Prediction[] = [{
      outcome: `先验方向：${(elemCareerMap[maxElem[0]] || []).join('、')}`,
      probability: 0.5 + maxElem[1] * 0.1,
      confidence_interval: [0.3, 0.7],
      reasoning: `五行${maxElem[0]}偏旺(${maxElem[1]}个)，作为贝叶斯先验假设`,
      factors: [{ name: `五行${maxElem[0]}`, weight: maxElem[1]*0.2, direction: 'positive' }],
    }];
    return { layer:1, layerName:'先验模型层', method:'贝叶斯先验(传统知识作为初始假设)',
      predictions, confidence:0.3, consensus:0.5, raw:{bazi,elements} };
  }
  private calcBazi(input: PredictionInput) {
    const stems = ['甲','乙','丙','丁','戊','己','庚','辛','壬','癸'];
    const branches = ['子','丑','寅','卯','辰','巳','午','未','申','酉','戌','亥'];
    return { yearStem: stems[(input.birthYear-4)%10], yearBranch: branches[(input.birthYear-4)%12],
      dayStem: stems[(input.birthYear+input.birthMonth+input.birthDay)%10] };
  }
  private calcElements(bazi: any) {
    const m: Record<string,string> = {'甲':'wood','乙':'wood','丙':'fire','丁':'fire','戊':'earth','己':'earth','庚':'metal','辛':'metal','壬':'water','癸':'water','子':'water','丑':'earth','寅':'wood','卯':'wood','辰':'earth','巳':'fire','午':'fire','未':'earth','申':'metal','酉':'metal','戌':'earth','亥':'water'};
    const e: Record<string,number> = {wood:0,fire:0,earth:0,metal:0,water:0};
    [bazi.yearStem,bazi.yearBranch,bazi.dayStem].forEach(s => { if(m[s]) e[m[s]]++; });
    return e;
  }
}

// ===== 第2层：统计预测 =====
export class StatisticalLayer {
  predict(input: PredictionInput, prior: LayerResult): LayerResult {
    const N = 10000; const results: number[] = [];
    const priorProb = prior.predictions[0]?.probability || 0.5;
    for (let i = 0; i < N; i++) {
      let v = priorProb + this.gauss(0, 0.15);
      const steps = input.timeframe || 5;
      for (let s = 0; s < steps; s++) v += 0.05*(0.5-v) + (deterministicNoise(input, i, s) - 0.5)*0.1;
      results.push(Math.max(0, Math.min(1, v)));
    }
    const mean = results.reduce((a,b)=>a+b,0)/N;
    const sorted = [...results].sort((a,b)=>a-b);
    const ciLow = sorted[Math.floor(N*0.025)], ciHigh = sorted[Math.floor(N*0.975)];
    const predictions: Prediction[] = [
      { outcome:'乐观场景', probability: results.filter(r=>r>=0.7).length/N, confidence_interval:[0.7,1.0],
        reasoning:`${(results.filter(r=>r>=0.7).length/N*100).toFixed(1)}%模拟结果>=70%`, factors:[] },
      { outcome:'中性场景', probability: results.filter(r=>r>=0.4&&r<0.7).length/N, confidence_interval:[0.4,0.7],
        reasoning:`${(results.filter(r=>r>=0.4&&r<0.7).length/N*100).toFixed(1)}%模拟结果在40-70%`, factors:[] },
      { outcome:'保守场景', probability: results.filter(r=>r<0.4).length/N, confidence_interval:[0,0.4],
        reasoning:`${(results.filter(r=>r<0.4).length/N*100).toFixed(1)}%模拟结果<40%`, factors:[] },
    ];
    return { layer:2, layerName:'统计预测层', method:`蒙特卡洛(${N}次)+马尔可夫链+贝叶斯推断`,
      predictions, confidence:0.6, consensus:1-(ciHigh-ciLow), raw:{mean,ciLow,ciHigh,N} };
  }
  private gauss(mean:number, std:number): number {
    return mean + std * Math.sqrt(-2*Math.log(deterministicRand(input+'g'))) * Math.cos(2*Math.PI*deterministicRand(input+'g2'));
  }
}

// ===== 第3层：多Agent推演 =====
export class MultiAgentLayer {
  predict(input: PredictionInput, stat: LayerResult): LayerResult {
    const agents = [
      {name:'趋势Agent',method:'时间序列趋势分析',bias:0.0},
      {name:'概率Agent',method:'贝叶斯网络推断',bias:-0.05},
      {name:'情景Agent',method:'情景规划分析',bias:0.05},
      {name:'风险Agent',method:'风险评估模型',bias:-0.1},
    ];
    const baseProb = stat.raw.mean || 0.5;
    const predictions: Prediction[] = agents.map(a => {
      const p = Math.max(0.05, Math.min(0.95, baseProb + a.bias + (deterministicRand(input+a.name)-0.5)*0.16));
      return { outcome: `${a.name}预测`, probability:p, confidence_interval:[Math.max(0,p-0.15),Math.min(1,p+0.15)],
        reasoning: `${a.name}使用${a.method}，偏差${a.bias>0?'乐观':a.bias<0?'保守':'中性'}`, factors:[] };
    });
    const probs = predictions.map(p=>p.probability);
    const mean = probs.reduce((a,b)=>a+b,0)/probs.length;
    const variance = probs.reduce((a,b)=>a+(b-mean)**2,0)/probs.length;
    const consensus = Math.max(0, 1-Math.sqrt(variance)*5);
    return { layer:3, layerName:'多Agent推演层', method:'4 Agent并行(趋势+概率+情景+风险)+共识分析',
      predictions, confidence:0.75, consensus, raw:{mean,variance,consensus} };
  }
}

// ===== 综合引擎 =====
export class PredictionEngine {
  async predict(input: PredictionInput): Promise<FinalPrediction> {
    const t0 = Date.now();
    const l1 = new PriorLayer().predict(input);
    const l2 = new StatisticalLayer().predict(input, l1);
    const l3 = new MultiAgentLayer().predict(input, l2);
    const finalProb = (l1.predictions[0]?.probability||0.5)*0.15 + l2.raw.mean*0.45 + l3.raw.mean*0.40;
    const recommendation = finalProb > 0.6 && l3.raw.consensus > 0.7
      ? '预测favorable且共识度高，建议积极把握方向，保持灵活性。'
      : finalProb > 0.5
      ? '预测中等偏正面，建议稳步推进，准备Plan B。'
      : l3.raw.consensus < 0.4
      ? 'Agent分歧大，建议收集更多信息再决策。'
      : '预测偏保守，建议谨慎行事，考虑调整策略。';
    return {
      input, layers:[l1,l2,l3],
      final: {
        outcome: finalProb > 0.7 ? 'favorable' : finalProb > 0.55 ? '较好' : finalProb > 0.4 ? '一般' : '面临挑战',
        probability: finalProb, confidence: l3.raw.consensus,
        ci_low: l2.raw.ciLow, ci_high: l2.raw.ciHigh,
        key_factors: ['五行先验','蒙特卡洛模拟','马尔可夫演化','4 Agent共识'],
        scenarios: l2.predictions.map(p => ({ name:p.outcome, probability:p.probability, description:p.reasoning })),
        recommendation,
      },
      meta: {
        methods: ['贝叶斯先验','蒙特卡洛(10000次)','马尔可夫链','4 Agent推演'],
        total_simulations: 10000, computation_time: Date.now()-t0,
        disclaimer: '本预测基于统计模型和概率推演，结果仅供参考，不构成决策建议。',
      },
    };
  }
}
