import { NextRequest, NextResponse } from 'next/server';
import { PredictionEngine, type PredictionInput } from '@/lib/prediction-engine';

export async function POST(req: NextRequest) {
  const body = await req.json();
  const input: PredictionInput = {
    birthYear: body.birthYear || 1990, birthMonth: body.birthMonth || 1,
    birthDay: body.birthDay || 1, birthHour: body.birthHour || 12,
    gender: body.gender || 'male', target: body.target || 'overall',
    timeframe: body.timeframe || 5,
  };
  const engine = new PredictionEngine();
  const result = await engine.predict(input);
  return NextResponse.json(result);
}
