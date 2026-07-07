"""
Agent 8: 科研员（Researcher）— 项目技术论证顾问
职责：论文解读、技术可行性分析、专利分析、前沿追踪、科研论证
模型：glm-4-plus + agnes（交叉论证）
端口：8466
"""

import sys, os, json, time, traceback
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shared.base_agent import BaseAgent
from shared.llm_client import call_llm, call_llm_multi, synthesize, web_search
from shared.project_db import query_all_kb


class ResearcherAgent(BaseAgent):
    def __init__(self):
        super().__init__("researcher", "项目技术论证顾问", 8466)

    def execute(self, task: str, params: dict) -> dict:
        start = time.time()
        project_id = params.get("project_id", "default")
        try:
            handlers = {
                "paper_analysis": self._paper_analysis,
                "tech_feasibility": self._tech_feasibility,
                "patent_analysis": self._patent_analysis,
                "frontier_tracking": self._frontier_tracking,
                "research_argument": self._research_argument,
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

    def _paper_analysis(self, params: dict) -> dict:
        """论文深度解读"""
        paper_url = params.get("paper_url", "")
        topic = params.get("topic", "")

        # 搜索论文
        results = web_search(f"{topic} arxiv nature science 论文 2026", count=10)

        prompt = f"""你是科研论文分析专家。

论文主题：{topic}
论文URL：{paper_url}

搜索到的相关论文：
{json.dumps(results[:5], ensure_ascii=False)[:2000]}

请输出：
1. 研究背景与动机
2. 核心创新点
3. 方法论
4. 关键结果
5. 局限性
6. 应用价值
7. 对我们项目的影响"""

        analysis = call_llm(prompt, model="glm-4-plus", max_tokens=2000)

        # agnes交叉验证
        cross_check = call_llm(f"请验证以下论文分析是否准确，补充遗漏点：\n{analysis}", model="agnes", max_tokens=1000)

        return {"paper_analysis": analysis, "cross_check": cross_check, "sources": results[:5]}

    def _tech_feasibility(self, params: dict) -> dict:
        """技术可行性分析"""
        tech = params.get("technology", "")
        application = params.get("application", "")

        # 搜索技术现状
        results = web_search(f"{tech} technology readiness level 2026 maturity", count=10)

        # 查知识库
        kb_data = query_all_kb(tech, limit_per_site=3)

        prompt = f"""你是技术评估专家。评估以下技术的可行性：

技术：{tech}
应用场景：{application}

搜索结果：
{json.dumps(results[:5], ensure_ascii=False)[:2000]}

知识库数据：
{json.dumps(kb_data, ensure_ascii=False)[:800]}

请输出：
1. 技术成熟度评估（TRL 1-9）
2. 关键技术瓶颈
3. 竞争技术对比
4. 实现路径建议
5. 时间表预估
6. 风险评估
7. 投入产出比"""

        analysis = call_llm(prompt, model="glm-4-plus", max_tokens=2000)
        return {"tech_feasibility": analysis, "sources": results[:5]}

    def _patent_analysis(self, params: dict) -> dict:
        """专利分析"""
        keyword = params.get("keyword", "")
        patent_id = params.get("patent_id", "")

        results = web_search(f"{keyword} 专利 patent {patent_id}", count=10)

        prompt = f"""你是专利分析专家。

关键词：{keyword}
专利号：{patent_id}

搜索结果：
{json.dumps(results[:5], ensure_ascii=False)[:2000]}

请输出：
1. 专利概况
2. 权利要求分析
3. 技术方案
4. 规避建议
5. 自由实施分析（FTO）
6. 专利布局建议"""

        analysis = call_llm(prompt, model="glm-4-plus", max_tokens=1500)
        return {"patent_analysis": analysis, "sources": results[:5]}

    def _frontier_tracking(self, params: dict) -> dict:
        """前沿技术追踪"""
        field = params.get("field", "")
        days = params.get("days", 7)

        results = web_search(f"{field} breakthrough arxiv nature science {days}days", count=15)

        prompt = f"""你是前沿技术追踪专家。

追踪领域：{field}
时间范围：最近{days}天

搜索结果：
{json.dumps(results[:10], ensure_ascii=False)[:3000]}

请输出：
1. 本周重要突破
2. 趋势分析
3. 关键论文/团队
4. 对行业的影响
5. 建议关注方向
6. 与我们项目的关联"""

        analysis = call_llm(prompt, model="glm-4-plus", max_tokens=1500)
        return {"field": field, "tracking": analysis, "sources": results[:10]}

    def _multi_perspective_analysis(self, params: dict) -> dict:
        """多视角并行分析+自我反驳 — 借鉴ai-berkshire的多Agent投资分析模式"""
        topic = params.get('topic', '')
        if not topic:
            return {'error': '请提供分析主题'}
        
        perspectives = [
            {'name': '乐观视角', 'prompt': f'从乐观角度分析"{topic}"的优势和机会，给出3个理由'},
            {'name': '悲观视角', 'prompt': f'从悲观角度分析"{topic}"的风险和问题，给出3个理由'},
            {'name': '实用视角', 'prompt': f'从实用角度分析"{topic}"的落地可行性，给出3个建议'},
            {'name': '反驳视角', 'prompt': f'对"{topic}"的常见观点进行反驳，找出3个盲点'},
        ]
        
        results = []
        from shared.llm_client import call_llm
        for p in perspectives:
            try:
                analysis = call_llm(p['prompt'], model='glm-4-flash', max_tokens=300)
                results.append({'perspective': p['name'], 'analysis': analysis[:500]})
            except:
                results.append({'perspective': p['name'], 'analysis': '分析失败'})
        
        # 综合结论
        perspectives_text = '\n'.join([r["perspective"]+":"+r["analysis"][:100] for r in results])
        synthesis = call_llm(
            f'综合以下4个视角的分析，给出平衡结论：\n{perspectives_text}',
            model='glm-4-flash', max_tokens=300
        )
        
        return {
            'topic': topic,
            'perspectives': results,
            'synthesis': synthesis[:500],
            'method': '多视角并行分析(乐观/悲观/实用/反驳)+综合'
        }
    
    def _self_improve(self, params: dict) -> dict:
        """自我改进 — 借鉴NVIDIA ASPIRE框架，Agent从过往任务中学习"""
        task_type = params.get('task_type', '')
        feedback = params.get('feedback', '')
        
        # 记录到growth log
        import os, json
        log_path = os.path.join(os.path.dirname(__file__), 'growth-log.md')
        entry = f"\n## {params.get('date', 'today')} - {task_type}\n反馈: {feedback}\n改进点: {params.get('improvement', '待记录')}\n"
        with open(log_path, 'a') as f:
            f.write(entry)
        
        return {'status': 'recorded', 'task_type': task_type, 'message': '自我改进记录已保存，后续任务将参考'}
    
    def _research_argument(self, params: dict) -> dict:
        """科研论证"""
        hypothesis = params.get("hypothesis", "")
        evidence = params.get("evidence", "")

        # 搜索支持/反驳证据
        support = web_search(f"{hypothesis} 支持 证据 研究", count=5)
        against = web_search(f"{hypothesis} 反对 质疑 局限", count=5)

        prompt = f"""你是科研论证专家。

假设：{hypothesis}
已有证据：{evidence}

支持证据：
{json.dumps(support[:3], ensure_ascii=False)[:1000]}

反对证据：
{json.dumps(against[:3], ensure_ascii=False)[:1000]}

请输出：
1. 假设的可信度评估（1-10分）
2. 支持论据
3. 反对论据
4. 关键不确定性
5. 验证方案建议
6. 结论"""

        analysis = call_llm(prompt, model="glm-4-plus", max_tokens=1500)
        return {"hypothesis": hypothesis, "argument": analysis,
                "support_sources": support[:3], "against_sources": against[:3]}

    def get_capabilities(self) -> dict:
        return {
            "agent": "researcher",
            "description": self.description,
            "capabilities": [
                "论文深度解读（glm-4-plus+agnes交叉）",
                "技术可行性分析（TRL评估）",
                "专利分析（权利要求+规避建议）",
                "前沿技术追踪",
                "科研论证（假设验证）",
                "14站知识库关联",
                "项目长期技术跟踪"
            ],
            "tools": ["web_search", "PubMed API", "arxiv", "14站知识库", "ClinicalTrials API"],
            "models": ["glm-4-plus", "agnes"],
            "version": "1.0.0",
            "port": 8466
        }


if __name__ == "__main__":
    agent = ResearcherAgent()
    print("=== Health Check ===")
    print(json.dumps(agent.health_check(), ensure_ascii=False, indent=2))
    print("\n=== Capabilities ===")
    print(json.dumps(agent.get_capabilities(), ensure_ascii=False, indent=2))
