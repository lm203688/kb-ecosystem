// GeneTech 14站跨站搜索 API
// 部署到: genetech-tools/website/functions/api/cross-search.js

const SITES = {
  genetech: 'https://genetech-tools.pages.dev/api/entities.json',
  tcm: 'https://tcm-tools.pages.dev/api/entities.json',
  agent: 'https://agentecosystem.pages.dev/api/entities.json',
  robot: 'https://robotparts.pages.dev/api/entities.json',
  quantum: 'https://quantumcomputing.pages.dev/api/entities.json',
  brain: 'https://brainscience.pages.dev/api/entities.json',
  nuclear: 'https://nuclearenergy.pages.dev/api/entities.json',
  exo: 'https://exoscience.pages.dev/api/entities.json',
  mineral: 'https://alienminerals.pages.dev/api/entities.json',
  deepsea: 'https://deepseatech.pages.dev/api/entities.json',
  newenergy: 'https://newenergy-nya.pages.dev/api/entities.json',
  lifescience: 'https://lifescience-epe.pages.dev/api/entities.json',
  biocomputing: 'https://biocomputedb.pages.dev/api/entities.json',
  bionicai: 'https://bionicai.pages.dev/api/entities.json',
};

export async function onRequest(context) {
  const { request } = context;
  const url = new URL(request.url);
  const keyword = url.searchParams.get('q') || '';
  const sitesParam = url.searchParams.get('sites') || ''; // 可选：指定站点
  const limit = parseInt(url.searchParams.get('limit') || '5');
  
  if (!keyword) {
    return new Response(JSON.stringify({ error: '需要q参数（搜索关键词）' }), {
      headers: { 'Content-Type': 'application/json' }
    });
  }
  
  // 决定搜索哪些站
  const sitesToSearch = sitesParam 
    ? sitesParam.split(',').filter(s => SITES[s])
    : Object.keys(SITES);
  
  const results = {};
  let totalCount = 0;
  
  // 并行搜索所有站
  const promises = sitesToSearch.map(async (siteKey) => {
    try {
      const resp = await fetch(SITES[siteKey], { signal: AbortSignal.timeout(5000) });
      const data = await resp.json();
      const entities = Array.isArray(data) ? data : (data.entities || data.data || []);
      
      const matched = entities.filter(e => {
        const name = (e.name || e.title || '').toLowerCase();
        const summary = (e.summary || e.abstract || '').toLowerCase();
        return name.includes(keyword.toLowerCase()) || summary.includes(keyword.toLowerCase());
      }).slice(0, limit);
      
      results[siteKey] = {
        total: matched.length,
        items: matched.map(e => ({
          id: e.id || '',
          name: e.name || e.title || '',
          summary: (e.summary || e.abstract || '').slice(0, 200),
          type: e.type || '',
          category: e.category || '',
        }))
      };
      totalCount += matched.length;
    } catch (e) {
      results[siteKey] = { total: 0, error: e.message.slice(0, 100) };
    }
  });
  
  await Promise.all(promises);
  
  return new Response(JSON.stringify({
    keyword: keyword,
    sites_searched: sitesToSearch.length,
    total_results: totalCount,
    results: results,
  }, null, 2), {
    headers: { 'Content-Type': 'application/json' }
  });
}
