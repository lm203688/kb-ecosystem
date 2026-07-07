"""
Agent 1: 情报员（Scout）— 项目情报顾问
职责：数据采集、竞品监控、论文/专利追踪、行业趋势
模型：glm-4-plus（分析）+ web_search
端口：8460（注意：蜂群科研占用了8460，改为8470）
"""

import sys, os, json, time, traceback
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shared.base_agent import BaseAgent
from shared.llm_client import call_llm, call_llm_multi, synthesize, web_search
from shared.project_db import query_kb, query_all_kb


class ScoutAgent(BaseAgent):
    def __init__(self):
        super().__init__("scout", "项目情报顾问", 8470)

    def execute(self, task: str, params: dict) -> dict:
        start = time.time()
        project_id = params.get("project_id", "default")
        try:
            handlers = {
                "intel_search": self._intel_search,
                "competitor_watch": self._competitor_watch,
                "trend_analysis": self._trend_analysis,
                "trend_clustering": self._trend_clustering,
                "research_trending": self._research_trending,
                "kb_search": self._kb_search,
                "daily_brief": self._daily_brief,
                "health_check": lambda p: self.health_check(),
                "capabilities": lambda p: self.get_capabilities(),
                "register_project": lambda p: self.register_project(p["project_id"], p["name"], p.get("profile", "")),
            }
            handler = handlers.get(task)
            if not handler:
                return {"error": f"Unknown task: {task}", "available": list(handlers.keys())}
            result = handler(params)
            duration = int((time.time() - start) * 1000)
            self._log_task(project_id, task, "success", json.dumps(result, ensure_ascii=False)[:500], duration)
            return result
        except Exception as e:
            duration = int((time.time() - start) * 1000)
            err = traceback.format_exc()[:500]
            self._log_task(project_id, task, "error", err, duration)
            self.log_growth("failure", f"Task {task} failed: {err}")
            return {"error": str(e), "traceback": err}

    def _intel_search(self, params: dict) -> dict:
        """情报搜索 — 互联网为主，项目数据库补充"""
        query = params.get("query", "")
        depth = params.get("depth", "standard")  # quick/standard/deep
        project_id = params.get("project_id", "default")

        if not query:
            return {"error": "Missing 'query' parameter"}

        # 1. 互联网搜索
        count = 5 if depth == "quick" else 10 if depth == "standard" else 20
        web_results = web_search(query, count=count)

        # 2. 项目数据库补充（14站知识库）
        kb_results = query_all_kb(query, limit_per_site=3)

        # 3. LLM分析综合
        if depth in ("standard", "deep"):
            prompt = f"""你是情报分析师。请分析以下搜索结果，输出结构化情报简报：

搜索关键词：{query}

互联网搜索结果：
{json.dumps(web_results[:10], ensure_ascii=False, indent=2)[:3000]}

项目数据库匹配：
{json.dumps(kb_results, ensure_ascii=False)[:1000]}

请输出：
1. 核心发现（3-5条）
2. 趋势信号
3. 对项目的潜在影响
4. 建议行动
5. 信息源质量评估"""
            analysis = call_llm(prompt, model="glm-4-plus", max_tokens=1500)
        else:
            analysis = "快速模式，跳过深度分析"

        # 记录到项目记忆
        if project_id != "default":
            self.add_project_note(project_id, f"情报搜索: {query}\n分析摘要: {analysis[:200]}")

        return {
            "query": query,
            "depth": depth,
            "web_results_count": len(web_results),
            "web_results": web_results[:10],
            "kb_results": kb_results,
            "analysis": analysis
        }

    def _competitor_watch(self, params: dict) -> dict:
        """竞品监控"""
        competitor = params.get("competitor", "")
        url = params.get("url", "")

        results = web_search(f"{competitor} 最新动态 新功能 更新", count=10)

        prompt = f"""分析竞品 {competitor} 的最新动态：
{json.dumps(results, ensure_ascii=False)[:2000]}

请输出：
1. 竞品最近动态摘要
2. 新功能/新产品
3. 定价变化
4. 对我们项目的威胁评估
5. 建议应对策略"""

        analysis = call_llm(prompt, model="glm-4-plus", max_tokens=1000)
        return {"competitor": competitor, "findings": results[:5], "analysis": analysis}

    def _trend_analysis(self, params: dict) -> dict:
        """趋势分析"""
        field = params.get("field", "")
        query = f"{field} 2026 趋势 发展 前沿"
        results = web_search(query, count=15)

        prompt = f"""分析 {field} 领域的趋势：
{json.dumps(results, ensure_ascii=False)[:3000]}

请输出：
1. 当前热点（Top 5）
2. 新兴方向
3. 技术成熟度评估
4. 商业机会
5. 风险信号"""

        analysis = call_llm(prompt, model="glm-4-plus", max_tokens=1500)
        return {"field": field, "trend_analysis": analysis}

    def _kb_search(self, params: dict) -> dict:
        """知识库搜索"""
        keyword = params.get("keyword", "")
        site = params.get("site", "all")  # all或具体站名

        if site == "all":
            results = query_all_kb(keyword, limit_per_site=5)
        else:
            results = {site: query_kb(site, keyword=keyword, limit=10)}

        return {"keyword": keyword, "results": results}

    def _trend_clustering(self, params: dict) -> dict:
        """时序聚类分析 — 无监督聚类+时序建模"""
        data = params.get('data', [])
        if not data or len(data) < 3:
            return {'error': '请提供至少3个数据点'}
        
        # 简化版K-means聚类
        k = min(3, len(data) // 2)
        centroids = data[:k] if isinstance(data[0], (int, float)) else [0]*k
        
        for _ in range(10):  # 10次迭代
            clusters = [[] for _ in range(k)]
            for d in data:
                if isinstance(d, (int, float)):
                    dists = [abs(d - c) for c in centroids]
                    clusters[dists.index(min(dists))].append(d)
            centroids = [sum(c)/len(c) if c else 0 for c in clusters]
        
        # 时序趋势
        if isinstance(data[0], (int, float)):
            trend = '上升' if data[-1] > data[0] else '下降' if data[-1] < data[0] else '平稳'
            change_pct = ((data[-1] - data[0]) / data[0] * 100) if data[0] != 0 else 0
        else:
            trend = '未知'
            change_pct = 0
        
        return {
            'clusters': [{'center': c, 'size': len(clusters[i])} for i, c in enumerate(centroids)],
            'trend': trend,
            'change_pct': round(change_pct, 2),
            'data_points': len(data),
            'method': f'K-means聚类(k={k})+时序趋势分析'
        }
    
    def _research_trending(self, params: dict) -> dict:
        """科研趋势榜单——借鉴AI科研工具榜"""
        category = params.get('category', 'all')  # all/agent/notebook/literature
        
        import urllib.request, json
        trending = []
        
        # GitHub trending
        try:
            url = 'https://api.github.com/search/repositories?q=AI+research+science+agent&sort=stars&order=desc&per_page=10'
            req = urllib.request.Request(url, headers={'User-Agent': 'ScoutAgent/1.0'})
            r = urllib.request.urlopen(req, timeout=10)
            data = json.loads(r.read())
            for repo in data.get('items', [])[:10]:
                trending.append({
                    'name': repo['full_name'],
                    'stars': repo['stargazers_count'],
                    'description': repo.get('description', '')[:80],
                    'url': repo['html_url'],
                    'language': repo.get('language', ''),
                    'category': 'research',
                })
        except:
            pass
        
        return {
            'category': category,
            'trending': trending[:10],
            'total': len(trending),
            'method': 'GitHub科研趋势榜单（借鉴AI科研工具榜）'
        }
    
    def _daily_brief(self, params: dict) -> dict:
        """每日简报 — 扫描多领域"""
        fields = params.get("fields", ["CRISPR", "AI Agent", "机器人", "核能", "量子计算"])
        briefs = {}
        for field in fields:
            results = web_search(f"{field} 最新突破 新闻 2026", count=5)
            briefs[field] = results[:3]
            time.sleep(2)

        # LLM生成综合简报
        prompt = f"""生成今日科技情报简报：
{json.dumps(briefs, ensure_ascii=False)[:3000]}

请输出简洁的每日简报，每个领域2-3条要点。"""
        summary = call_llm(prompt, model="glm-4-flash", max_tokens=1000)

        return {"date": time.strftime("%Y-%m-%d"), "fields": fields, "briefs": briefs, "summary": summary}

    def get_capabilities(self) -> dict:
        return {
            "agent": "scout",
            "description": self.description,
            "capabilities": [
                "情报搜索（互联网+项目数据库）",
                "竞品监控",
                "趋势分析",
                "14站知识库搜索",
                "每日情报简报",
                "项目长期情报跟踪"
            ],
            "tools": ["web_search", "14站知识库API", "PubMed", "Scrapling"],
            "models": ["glm-4-plus", "glm-4-flash", "agnes"],
            "version": "1.0.0",
            "port": 8470
        }


if __name__ == "__main__":
    agent = ScoutAgent()
    print("=== Health Check ===")
    print(json.dumps(agent.health_check(), ensure_ascii=False, indent=2))
    print("\n=== Capabilities ===")
    print(json.dumps(agent.get_capabilities(), ensure_ascii=False, indent=2))
    print("\n=== KB Search Test ===")
    result = agent.execute("kb_search", {"keyword": "CRISPR", "site": "genetech"})
    print(json.dumps(result, ensure_ascii=False, indent=2)[:1000])
