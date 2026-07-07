/**
 * Credits Balance API
 * GET /api/credits/balance?key=xxx → returns user's credit balance
 * POST /api/credits/redeem → redeem a Creem license key for credits
 */

export async function onRequestGet(context) {
  const { request, env } = context;
  const url = new URL(request.url);
  const apiKey = url.searchParams.get('key') || 
                 request.headers.get('Authorization')?.replace('Bearer ', '');
  
  const corsHeaders = {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',
  };
  
  if (!apiKey) {
    return new Response(JSON.stringify({ error: 'API key required' }), {
      status: 401, headers: corsHeaders
    });
  }
  
  // Check KV for user credits
  if (env.USER_CREDITS) {
    const userData = await env.USER_CREDITS.get(apiKey);
    if (userData) {
      const user = JSON.parse(userData);
      return new Response(JSON.stringify({
        email: user.email,
        credits: user.credits || 0,
        plan: user.plan || 'free',
        api_calls: user.api_calls || 0,
      }), { headers: corsHeaders });
    }
  }
  
  // Default: free tier with 0 credits
  return new Response(JSON.stringify({
    credits: 0,
    plan: 'free',
    message: 'Purchase credits at https://genetech.tools/credits',
  }), { headers: corsHeaders });
}

export async function onRequestPost(context) {
  const { request, env } = context;
  const corsHeaders = {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',
  };
  
  try {
    const body = await request.json();
    const { license_key, email } = body;
    
    if (!license_key) {
      return new Response(JSON.stringify({ error: 'license_key required' }), {
        status: 400, headers: corsHeaders
      });
    }
    
    // Validate license with Creem API
    const CREEM_API_KEY = typeof env !== 'undefined' ? (env.CREEM_API_KEY || '') : '';
    const creemResponse = await fetch('https://api.creem.io/v1/licenses/validate', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': CREEM_API_KEY,
      },
      body: JSON.stringify({ license_key }),
    });
    
    const creemData = await creemResponse.json();
    
    if (!creemData.valid && !creemData.activated) {
      return new Response(JSON.stringify({ error: 'Invalid license key' }), {
        status: 400, headers: corsHeaders
      });
    }
    
    // Determine credit amount based on product
    const productId = creemData.product?.id || '';
    let credits = 0;
    if (productId.includes('22YhSbY')) credits = 990; // Pro monthly
    else if (productId.includes('4EpFVQ')) credits = 500; // API Access
    else if (productId.includes('pny43r')) credits = 9999; // Lifetime
    else if (productId.includes('5IooNC')) credits = 4999; // One-time data
    else credits = 100; // Default
    
    // Store in KV
    if (env.USER_CREDITS) {
      const userKey = `gtk_${license_key.slice(0, 16)}`;
      const existing = await env.USER_CREDITS.get(userKey);
      const user = existing ? JSON.parse(existing) : { email: email || 'unknown', credits: 0, plan: 'pro' };
      user.credits = (user.credits || 0) + credits;
      user.plan = 'pro';
      user.license_key = license_key;
      await env.USER_CREDITS.put(userKey, JSON.stringify(user));
      
      return new Response(JSON.stringify({
        success: true,
        api_key: userKey,
        credits_added: credits,
        total_credits: user.credits,
        plan: 'pro',
      }), { headers: corsHeaders });
    }
    
    return new Response(JSON.stringify({
      success: true,
      credits_added: credits,
      message: 'License valid. Contact support to activate credits.',
    }), { headers: corsHeaders });
    
  } catch(e) {
    return new Response(JSON.stringify({ error: e.message }), {
      status: 500, headers: corsHeaders
    });
  }
}
