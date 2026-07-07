"""项目数据库统一查询层 — Agent通过此模块查询现有项目数据库"""

import json, urllib.request, urllib.error
from typing import Dict, List, Optional

# 14站知识库API
KB_SITES = {
    "genetech": "https://genetech-tools.pages.dev/api/entities.json",
    "tcm": "https://tcm-tools.pages.dev/api/entities.json",
    "agent": "https://agentecosystem.pages.dev/api/entities.json",
    "robot": "https://robotparts.pages.dev/api/entities.json",
    "quantum": "https://quantumcomputing.pages.dev/api/entities.json",
    "brain": "https://brainscience.pages.dev/api/entities.json",
    "nuclear": "https://nuclearenergy.pages.dev/api/entities.json",
    "exo": "https://exoscience.pages.dev/api/entities.json",
    "alien": "https://alienminerals.pages.dev/api/entities.json",
    "deepsea": "https://deepseatech.pages.dev/api/entities.json",
    "newenergy": "https://newenergy-nya.pages.dev/api/entities.json",
    "lifescience": "https://lifescience-epe.pages.dev/api/entities.json",
    "biocomputing": "https://biocomputedb.pages.dev/api/entities.json",
    "bionicai": "https://bionicai.pages.dev/api/entities.json",
}

# ECS服务
ECS_SERVICES = {
    "aishield_api": "http://150.158.119.19:8420/api/v1/status",
    "aishield_compliance": "http://localhost:8450/api/v1/health",
    "swarm_research": "http://150.158.119.19:8460/api/v1/health",
    "bit_assistant": "http://150.158.119.19:8431/v1/models",
    "healthlens": "http://150.158.119.19:8432/",
}


def query_kb(site: str, keyword: str = "", limit: int = 20) -> List[Dict]:
    """查询14站知识库"""
    url = KB_SITES.get(site)
    if not url:
        return [{"error": f"Unknown site: {site}, available: {list(KB_SITES.keys())}"}]
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            entities = data if isinstance(data, list) else data.get("entities", data.get("data", []))
            if keyword:
                kw = keyword.lower()
                entities = [e for e in entities if kw in json.dumps(e, ensure_ascii=False).lower()]
            return entities[:limit]
    except Exception as e:
        return [{"error": f"{site}: {str(e)[:100]}"}]


def query_all_kb(keyword: str, limit_per_site: int = 5) -> Dict[str, List]:
    """跨所有14站搜索关键词"""
    results = {}
    for site in KB_SITES:
        entities = query_kb(site, keyword=keyword, limit=limit_per_site)
        if entities and "error" not in entities[0]:
            results[site] = entities
    return results


def check_ecs_services() -> Dict[str, int]:
    """检查ECS所有服务状态（超时3秒，快速返回）"""
    results = {}
    for name, url in ECS_SERVICES.items():
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=3) as resp:
                results[name] = resp.status
        except urllib.error.HTTPError as e:
            results[name] = e.code
        except Exception as e:
            results[name] = 0  # unreachable
    return results


def check_pages_sites() -> Dict[str, int]:
    """检查14站Pages可用性（超时5秒）"""
    results = {}
    for site, url in KB_SITES.items():
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=5) as resp:
                results[site] = resp.status
        except urllib.error.HTTPError as e:
            results[site] = e.code
        except:
            results[site] = 0
    return results
