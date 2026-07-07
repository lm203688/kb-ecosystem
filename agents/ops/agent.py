"""
Agent 7: 运营财务官（Operator+Finance）— 项目运营+财务顾问
职责：日常监控、告警、数据统计、成本控制、收入追踪、利润分析、ROI评估
模型：cron脚本 + glm-4-flash（报告润色）
端口：8465
"""

import sys, os, json, time, traceback, urllib.request
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shared.base_agent import BaseAgent
from shared.llm_client import call_llm
from shared.project_db import check_ecs_services, check_pages_sites


class OperatorAgent(BaseAgent):
    def __init__(self):
        super().__init__("operator", "项目运营+财务顾问", 8465)

    def execute(self, task: str, params: dict) -> dict:
        start = time.time()
        project_id = params.get("project_id", "default")
        try:
            handlers = {
                "daily_monitor": self._daily_monitor,
                "incident_response": self._incident_response,
                "monthly_report": self._monthly_report,
                "income_check": self._income_check,
                "cost_analysis": self._cost_analysis,
                "profit_analysis": self._profit_analysis,
                "multi_perspective_ops": self._multi_perspective_ops,
                "pricing_advice": self._pricing_advice,
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

    def _daily_monitor(self, params: dict) -> dict:
        """日常监控 — 复用cron逻辑"""
        ecs = check_ecs_services()
        pages = check_pages_sites()

        issues = []
        for name, status in ecs.items():
            if status not in (200,):
                issues.append(f"⚠️ ECS服务 {name} 异常: {status}")
        for site, status in pages.items():
            if status not in (200,):
                issues.append(f"⚠️ 14站 {site} 异常: {status}")

        # Creem产品状态
        creem_status = self._check_creem()

        # 生成简报
        if issues:
            prompt = f"""生成运维告警简报：
异常项：{json.dumps(issues, ensure_ascii=False)}
请简洁说明每个异常的严重程度和建议操作。"""
            brief = call_llm(prompt, model="glm-4-flash", max_tokens=500)
        else:
            brief = "所有服务正常运行"

        return {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "ecs_services": ecs,
            "pages_sites": pages,
            "creem_products": creem_status,
            "issues": issues,
            "brief": brief,
            "all_healthy": len(issues) == 0
        }

    def _check_creem(self) -> dict:
        """检查Creem 6产品状态"""
        pids = [
            "prod_22YhSbYonX9hiC0OppnXTn", "prod_4EpFVQGKm5vWXChbRiFdbE",
            "prod_pny43rzDa0mmBaj7d9k4w", "prod_5IooNCEQoCyqp758oeVPGT",
            "prod_5OFcAcJeXzfTMkDDt6woBh", "prod_44o1TOBce0Zt00X4E5ACET"
        ]
        results = {}
        for pid in pids:
            try:
                req = urllib.request.Request(
                    f"https://api.creem.io/v1/products?product_id={pid}",
                    headers={"x-api-key": "creem_4yM8aDDK17QiHjWdiWgQEA"}
                )
                with urllib.request.urlopen(req, timeout=10) as resp:
                    data = json.loads(resp.read().decode())
                    results[data.get("name", "?")[:30]] = data.get("status", "?")
            except:
                results[pid] = "error"
        return results

    def _incident_response(self, params: dict) -> dict:
        """故障响应"""
        incident = params.get("incident", "")
        severity = params.get("severity", "medium")

        prompt = f"""你是运维专家。分析以下故障并给出响应方案：

故障：{incident}
严重程度：{severity}

请输出：
1. 影响范围评估
2. 根因分析方向
3. 立即处理步骤
4. 恢复方案
5. 事后复盘要点
6. 预防措施"""

        response = call_llm(prompt, model="glm-4-plus", max_tokens=1000)
        return {"incident": incident, "severity": severity, "response_plan": response}

    def _monthly_report(self, params: dict) -> dict:
        """月度运营报告"""
        ecs = check_ecs_services()
        pages = check_pages_sites()
        creem = self._check_creem()

        prompt = f"""生成月度运营报告：

ECS服务状态：{json.dumps(ecs, ensure_ascii=False)}
14站状态：{json.dumps(pages, ensure_ascii=False)}
Creem产品状态：{json.dumps(creem, ensure_ascii=False)}

请输出：
1. 服务可用性总结
2. 异常事件统计
3. 收入概况
4. 成本概况
5. 下月建议"""

        report = call_llm(prompt, model="glm-4-plus", max_tokens=1500)
        return {"month": time.strftime("%Y-%m"), "report": report}

    def _income_check(self, params: dict) -> dict:
        """收入检查"""
        creem = self._check_creem()
        return {
            "creem_products": creem,
            "note": "Creem API不支持查询交易历史，需登录Dashboard查看"
        }

    def _cost_analysis(self, params: dict) -> dict:
        """成本分析"""
        costs = params.get("costs", {
            "ecs": 200,  # 腾讯云ECS月费
            "domains": 30,  # 域名年均
            "cf_pages": 0,  # Cloudflare Pages免费
            "creem": 0,  # Creem无月费
            "z_ai_sdk": 0,  # z-ai SDK免费
            "agnes": 0,  # agnes免费
        })

        total_monthly = sum(costs.values())
        prompt = f"""分析项目成本：

月度成本明细：{json.dumps(costs, ensure_ascii=False)}
月总成本：¥{total_monthly}

请输出：
1. 成本结构分析
2. 可优化项
3. 成本趋势预测
4. 建议"""

        analysis = call_llm(prompt, model="glm-4-plus", max_tokens=800)
        return {"monthly_cost": total_monthly, "breakdown": costs, "analysis": analysis}

    def _profit_analysis(self, params: dict) -> dict:
        """利润分析"""
        monthly_revenue = params.get("monthly_revenue", 0)
        monthly_cost = params.get("monthly_cost", 200)

        profit = monthly_revenue - monthly_cost
        margin = (profit / monthly_revenue * 100) if monthly_revenue > 0 else 0

        return {
            "monthly_revenue": monthly_revenue,
            "monthly_cost": monthly_cost,
            "profit": profit,
            "margin": f"{margin:.1f}%",
            "status": "盈利" if profit > 0 else "亏损" if profit < 0 else "持平"
        }

    def _multi_perspective_ops(self, params: dict) -> dict:
        """多视角运营分析 — 借鉴ai-berkshire多Agent投资分析模式
        4个视角并行分析运营决策：增长/风控/成本/竞争
        """
        topic = params.get('topic', '')
        if not topic:
            return {'error': '请提供分析主题'}
        
        perspectives = [
            {'name': '增长视角', 'prompt': f'从增长角度分析"{topic}"：如何提升用户量/收入/市场份额？给出3个具体建议'},
            {'name': '风控视角', 'prompt': f'从风控角度分析"{topic}"：有哪些风险？如何规避？给出3个建议'},
            {'name': '成本视角', 'prompt': f'从成本角度分析"{topic}"：如何降低运营成本？给出3个建议'},
            {'name': '竞争视角', 'prompt': f'从竞争角度分析"{topic}"：竞品在做什么？如何差异化？给出3个建议'},
        ]
        
        results = []
        for p in perspectives:
            try:
                analysis = call_llm(p['prompt'], model='glm-4-flash', max_tokens=300)
                results.append({'perspective': p['name'], 'analysis': analysis[:500]})
            except:
                results.append({'perspective': p['name'], 'analysis': '分析失败'})
        
        # 综合结论
        perspectives_text = chr(10).join([r['perspective']+':'+r['analysis'][:100] for r in results])
        synthesis = call_llm(
            f'综合以下4个视角的运营分析，给出平衡结论和优先行动项：\n{perspectives_text}',
            model='glm-4-flash', max_tokens=300
        )
        
        return {
            'topic': topic,
            'perspectives': results,
            'synthesis': synthesis[:500],
            'method': '多视角并行分析(增长/风控/成本/竞争)+综合'
        }
    
    def _pricing_advice(self, params: dict) -> dict:
        """定价建议（基于成本+市场）"""
        cost = params.get("cost", 0)
        competitors = params.get("competitors", [])

        prompt = f"""基于成本和市场给出定价建议：

成本：¥{cost}
竞品：{json.dumps(competitors, ensure_ascii=False)}

请输出：
1. 成本加成定价
2. 市场导向定价
3. 建议价格档位
4. 盈亏平衡分析
5. 利润预期"""

        advice = call_llm(prompt, model="glm-4-plus", max_tokens=1000)
        return {"pricing_advice": advice}

    def get_capabilities(self) -> dict:
        return {
            "agent": "operator",
            "description": self.description,
            "capabilities": [
                "日常监控（ECS+14站+Creem）",
                "故障响应",
                "月度运营报告",
                "收入检查（Creem 6产品）",
                "成本分析（ECS/域名/工具）",
                "利润分析",
                "定价建议（成本+市场）",
                "项目长期运营跟踪"
            ],
            "tools": ["cron", "Bark推送", "Creem API", "ECS健康检查", "14站状态检查"],
            "models": ["glm-4-plus", "glm-4-flash"],
            "version": "1.0.0",
            "port": 8465
        }


if __name__ == "__main__":
    agent = OperatorAgent()
    print("=== Health Check ===")
    print(json.dumps(agent.health_check(), ensure_ascii=False, indent=2))
    print("\n=== Capabilities ===")
    print(json.dumps(agent.get_capabilities(), ensure_ascii=False, indent=2))
    print("\n=== Daily Monitor ===")
    print(json.dumps(agent.execute("daily_monitor", {}), ensure_ascii=False, indent=2))
