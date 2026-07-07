/**
 * CF Pages Function: API Gateway with Field-Level Paywall
 * - Free: summary fields only (id, name, category, focus truncated)
 * - Pro: full data (requires Creem license key)
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
const FREE_FIELDS = ['id', 'name', 'category', '_type', 'type', 'focus', 'hq', 'founded', 'development_stage', 'status'];
const FOCUS_LIMIT = 200;
const UPGRADE_URL = 'https://www.creem.io/product/prod_5OFcAcJeXzfTMkDDt6woBh';

export async function onRequestGet(context) {
  const { request, env, params } = context;
  const url = new URL(request.url);
  const path = params.path || [];
  const pathStr = Array.isArray(path) ? path.join('/') : path;

  const corsHeaders = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    'Access-Control-Max-Age': '86400',
  };

  if (request.method === 'OPTIONS') {
    return new Response(null, { headers: corsHeaders });
  }

  const requestedFile = pathStr.endsWith('.json') ? pathStr : pathStr + '.json';

  if (requestedFile.includes('..') || requestedFile.includes('//')) {
    return new Response(JSON.stringify({ error: 'Invalid path' }), {
      status: 400,
      headers: { 'Content-Type': 'application/json', ...corsHeaders },
    });
  }

  try {
    const assetUrl = new URL(`/api/${requestedFile}`, url.origin);
    const assetResponse = await env.ASSETS.fetch(assetUrl);

    if (!assetResponse.ok) {
      return new Response(JSON.stringify({
        error: 'Not Found',
        path: `/api/${requestedFile}`,
        status: assetResponse.status,
        hint: 'Available: entities.json, data.json, openapi.json, graph.json'
      }), {
        status: 404,
        headers: { 'Content-Type': 'application/json', ...corsHeaders },
      });
    }

    const data = await assetResponse.text();

    // Apply paywall to entities.json only
    if (requestedFile === 'entities.json' || requestedFile.endsWith('/entities.json')) {
      return await applyPaywall(data, request, corsHeaders);
    }

    return new Response(data, {
      status: 200,
      headers: {
        'Content-Type': 'application/json; charset=utf-8',
        'Cache-Control': 'public, max-age=300',
        'X-API-Tier': 'free',
        'X-Powered-By': 'GeneTech API Gateway',
        ...corsHeaders,
      }
    });
  } catch(e) {
    return new Response(JSON.stringify({
      error: 'Internal error',
      message: e.message,
      path: `/api/${requestedFile}`,
    }), {
      status: 500,
      headers: { 'Content-Type': 'application/json', ...corsHeaders },
    });
  }
}

async function applyPaywall(data, request, corsHeaders) {
  let parsed;
  try {
    parsed = JSON.parse(data);
  } catch(e) {
    return new Response(data, {
      status: 200,
      headers: { 'Content-Type': 'application/json; charset=utf-8', ...corsHeaders },
    });
  }

  // Check for license key
  const authHeader = request.headers.get('Authorization') || '';
  const url = new URL(request.url);
  const queryKey = url.searchParams.get('key') || '';
  let licenseKey = '';
  if (authHeader.startsWith('Bearer ')) {
    licenseKey = authHeader.slice(7).trim();
  } else if (queryKey) {
    licenseKey = queryKey.trim();
  }

  // Validate license key if provided
  if (licenseKey) {
    const isValid = await validateLicense(licenseKey);
    if (isValid) {
      return new Response(data, {
        status: 200,
        headers: {
          'Content-Type': 'application/json; charset=utf-8',
          'Cache-Control': 'no-store',
          'X-API-Tier': 'pro',
          ...corsHeaders,
        }
      });
    }
  }

  // Free tier: filter fields
  let entities, meta;
  if (Array.isArray(parsed)) {
    entities = parsed;
    meta = { total: parsed.length };
  } else {
    entities = parsed.entities || parsed.data || [];
    meta = parsed.meta || {};
  }

  const filtered = entities.map(e => {
    const out = {};
    for (const k of FREE_FIELDS) {
      if (e[k] !== undefined) out[k] = e[k];
    }
    // Truncate focus field
    if (out.focus && typeof out.focus === 'string' && out.focus.length > FOCUS_LIMIT) {
      out.focus = out.focus.slice(0, FOCUS_LIMIT) + '...';
    }
    // Count locked fields
    const lockedCount = Object.keys(e).filter(k => !FREE_FIELDS.includes(k)).length;
    out._locked_fields = lockedCount;
    out._upgrade_url = UPGRADE_URL;
    return out;
  });

  const result = {
    meta: {
      ...meta,
      total_returned: filtered.length,
      tier: 'free',
      locked_fields_per_entity: Object.keys(entities[0] || {}).filter(k => !FREE_FIELDS.includes(k)).length,
      upgrade_url: UPGRADE_URL,
      message: 'Free preview: limited fields shown. Add ?key=CREEM_LICENSE or Authorization: Bearer CREEM_LICENSE for full data.'
    },
    entities: filtered
  };

  return new Response(JSON.stringify(result, null, 2), {
    status: 200,
    headers: {
      'Content-Type': 'application/json; charset=utf-8',
      'Cache-Control': 'no-store',
      'X-API-Tier': 'free',
      ...corsHeaders,
    }
  });
}

async function validateLicense(key) {
  try {
    const resp = await fetch('https://api.creem.io/v1/licenses/validate', {
      method: 'POST',
      headers: {
        'X-API-KEY': CREEM_API_KEY,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ key })
    });
    const data = await resp.json();
    if (data.status === 'active' && PRO_PRODUCTS.includes(data.product_id)) {
      return true;
    }
    // Fallback: search endpoint
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
        if (license.status === 'active' && PRO_PRODUCTS.includes(license.product_id)) {
          return true;
        }
      }
    }
    return false;
  } catch(e) {
    return false;
  }
}
