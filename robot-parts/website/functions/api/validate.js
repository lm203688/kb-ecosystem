/**
 * License Validation API — Cloudflare Pages Function
 * Validates Creem license keys without exposing API key to client
 */

const CREEM_API_KEY = typeof env !== 'undefined' ? (env.CREEM_API_KEY || '') : '';
const PRO_PRODUCTS = [
  'prod_22YhSbYonX9hiC0OppnXTn',
  'prod_4EpFVQGKm5vWXChbRiFdbE',
  'prod_pny43rzDa0mmBaj7d9k4w',
  'prod_5IooNCEQoCyqp758oeVPGT',
  'prod_5OFcAcJeXzfTMkDDt6woBh',
  'prod_44o1TOBce0Zt00X4E5ACET'
];

export async function onRequestPost(context) {
  return handleRequest(context);
}

export async function onRequestGet(context) {
  return handleRequest(context);
}

async function handleRequest(context) {
  const origin = context.request.headers.get('Origin') || '';
  const corsHeaders = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Content-Type': 'application/json',
    'Cache-Control': 'no-store'
  };

  // Handle CORS preflight
  if (context.request.method === 'OPTIONS') {
    return new Response(null, { headers: corsHeaders });
  }

  try {
    const url = new URL(context.request.url);
    let key = url.searchParams.get('key');
    
    if (!key && context.request.method === 'POST') {
      try {
        const body = await context.request.json();
        key = body.key;
      } catch(e) {}
    }

    if (!key) {
      return new Response(JSON.stringify({ valid: false, error: 'Missing license key' }), {
        status: 400, headers: corsHeaders
      });
    }

    // Validate via Creem API
    const resp = await fetch('https://api.creem.io/v1/licenses/validate', {
      method: 'POST',
      headers: {
        'X-API-KEY': CREEM_API_KEY,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ key })
    });

    const data = await resp.json();
    
    if (data.status === 'active') {
      const productId = data.product_id;
      return new Response(JSON.stringify({
        valid: true,
        product_id: productId,
        product_name: data.product_name || 'Pro',
        is_pro: PRO_PRODUCTS.includes(productId),
        expires_at: data.expires_at || null
      }), { headers: corsHeaders });
    }

    // Try search endpoint as fallback
    const searchResp = await fetch('https://api.creem.io/v1/licenses/search', {
      method: 'POST',
      headers: {
        'X-API-KEY': CREEM_API_KEY,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ key })
    });

    if (searchResp.ok) {
      const searchData = await searchResp.json();
      if (searchData.items && searchData.items.length > 0) {
        const license = searchData.items[0];
        if (license.status === 'active') {
          return new Response(JSON.stringify({
            valid: true,
            product_id: license.product_id,
            product_name: license.product_name || 'Pro',
            is_pro: PRO_PRODUCTS.includes(license.product_id),
            expires_at: license.expires_at || null
          }), { headers: corsHeaders });
        }
      }
    }

    return new Response(JSON.stringify({ valid: false, error: 'Invalid or inactive license key' }), {
      headers: corsHeaders
    });
  } catch(e) {
    return new Response(JSON.stringify({ valid: false, error: 'Validation service error' }), {
      status: 500, headers: corsHeaders
    });
  }
}
