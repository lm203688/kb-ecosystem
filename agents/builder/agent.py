"""
Agent 2: 工程师（Builder）— 项目技术顾问
职责：代码审查、部署、bug修复、架构设计、技术债评估
模型：glm-4-plus（分析）+ 小乌（执行）
端口：8461
"""

import sys, os, json, time, traceback
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shared.base_agent import BaseAgent
from shared.llm_client import call_llm, call_llm_multi, synthesize
from shared.project_db import check_ecs_services, check_pages_sites


class BuilderAgent(BaseAgent):
    def __init__(self):
        super().__init__("builder", "项目技术顾问", 8461)

    def execute(self, task: str, params: dict) -> dict:
        """执行任务"""
        start = time.time()
        project_id = params.get("project_id", "default")
        try:
            handlers = {
                "code_review": self._code_review,
                "deploy_check": self._deploy_check,
                "tech_audit": self._tech_audit,
                "architecture_advice": self._architecture_advice,
                "bug_diagnose": self._bug_diagnose,
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
            self.log_growth("failure", f"Task {task} failed: {err}", "检查参数和依赖")
            return {"error": str(e), "traceback": err}

    def _code_review(self, params: dict) -> dict:
        """代码审查 — glm-4-plus分析"""
        code = params.get("code", "")
        language = params.get("language", "auto")
        context = params.get("context", "")

        if not code:
            return {"error": "Missing 'code' parameter"}

        prompt = f"""你是资深代码审查工程师。请审查以下代码，输出JSON格式：
{{
    "quality_score": 1-10,
    "issues": [{{"severity": "critical|warning|info", "line": "行号或位置", "issue": "问题描述", "fix": "修复建议"}}],
    "security": ["安全风险点"],
    "performance": ["性能优化建议"],
    "summary": "总体评价"
}}

代码语言：{language}
项目上下文：{context}

代码：
```
{code[:5000]}
```"""

        result = call_llm(prompt, model="glm-4-plus", max_tokens=2000)
        return {"review": result, "model": "glm-4-plus"}

    def _deploy_check(self, params: dict) -> dict:
        """部署状态检查"""
        ecs = check_ecs_services()
        pages = check_pages_sites()
        all_ok = all(v == 200 for v in ecs.values()) and all(v == 200 for v in pages.values())

        issues = []
        for name, status in ecs.items():
            if status != 200:
                issues.append(f"ECS服务 {name} 异常: {status}")
        for name, status in pages.items():
            if status != 200:
                issues.append(f"Pages站点 {name} 异常: {status}")

        return {
            "ecs_services": ecs,
            "pages_sites": pages,
            "all_healthy": all_ok,
            "issues": issues if issues else ["全部正常"]
        }

    def _tech_audit(self, params: dict) -> dict:
        """技术债评估"""
        project_id = params.get("project_id", "default")
        context = self.get_project_context(project_id)
        profile = context.get("profile", "") or params.get("project_description", "")

        prompt = f"""你是技术架构师。请评估以下项目的技术债，输出JSON：
{{
    "tech_stack": "推测的技术栈",
    "debt_items": [{{"category": "代码|架构|部署|测试|安全", "item": "问题描述", "severity": "高|中|低", "effort": "修复工时估算"}}],
    "recommendations": ["优先修复建议"],
    "health_score": 1-10
}}

项目信息：{profile}
历史决策：{json.dumps(context.get('recent_decisions', []), ensure_ascii=False)[:1000]}"""

        result = call_llm(prompt, model="glm-4-plus", max_tokens=2000)
        return {"audit": result, "project_id": project_id}

    def _architecture_advice(self, params: dict) -> dict:
        """架构建议 — 三模型交叉"""
        requirement = params.get("requirement", "")
        constraints = params.get("constraints", "")

        prompt = f"""你是系统架构师。针对以下需求给出架构建议：

需求：{requirement}
约束：{constraints}

请输出：
1. 推荐架构方案
2. 技术选型建议
3. 潜在风险
4. 分阶段实施计划"""

        results = call_llm_multi(prompt, models=["glm-4-flash", "glm-4-plus", "agnes"], max_tokens=1500)
        final = synthesize(results, requirement)
        return {"architecture_advice": final, "models_used": list(results.keys())}

    def _continuous_quality(self, params: dict) -> dict:
        """代码质量持续监控 — 借鉴SonarQube DataCenter"""
        project = params.get('project', '')
        # 统计代码质量指标
        import os, glob
        code_dir = params.get('code_dir', '/home/z/my-project')
        
        metrics = {'total_files': 0, 'total_lines': 0, 'todo_count': 0, 'error_count': 0, 'quality_gate': 'passed'}
        
        for ext in ['*.py', '*.ts', '*.tsx', '*.js']:
            for f_path in glob.glob(os.path.join(code_dir, '**', ext), recursive=True):
                if 'node_modules' in f_path or '.git' in f_path:
                    continue
                metrics['total_files'] += 1
                try:
                    lines = open(f_path, errors='replace').readlines()
                    metrics['total_lines'] += len(lines)
                    for line in lines:
                        if 'TODO' in line or 'FIXME' in line:
                            metrics['todo_count'] += 1
                        if 'eval(' in line or 'exec(' in line:
                            metrics['error_count'] += 1
                except:
                    pass
        
        # Quality Gate
        if metrics['error_count'] > 5:
            metrics['quality_gate'] = 'failed'
        elif metrics['todo_count'] > 20:
            metrics['quality_gate'] = 'warning'
        
        metrics['quality_score'] = max(0, 100 - metrics['error_count'] * 10 - metrics['todo_count'])
        
        return {
            'project': project,
            'metrics': metrics,
            'summary': f"文件{metrics['total_files']}个/代码{metrics['total_lines']}行/TODO {metrics['todo_count']}个/危险{metrics['error_count']}个/质量门{metrics['quality_gate']}",
            'method': '代码质量持续监控(文件扫描+TODO+危险函数+质量门)'
        }
    
    def _bug_diagnose(self, params: dict) -> dict:
        """Bug诊断"""
        error_msg = params.get("error", "")
        context = params.get("context", "")
        code = params.get("code", "")

        prompt = f"""你是debug专家。请诊断以下错误：

错误信息：
{error_msg}

相关代码：
{code[:3000]}

上下文：
{context}

请输出：
1. 可能的根因（列出2-3个）
2. 排查步骤
3. 修复方案
4. 预防措施"""

        result = call_llm(prompt, model="glm-4-plus", max_tokens=1500)
        return {"diagnosis": result}

    def get_capabilities(self) -> dict:
        return {
            "agent": "builder",
            "description": self.description,
            "capabilities": [
                "代码审查（多语言）",
                "部署状态检查（ECS+CF Pages）",
                "技术债评估",
                "架构建议（三模型交叉）",
                "Bug诊断",
                "项目长期技术跟踪"
            ],
            "tools": ["glm-4-plus", "glm-4-flash", "agnes", "ECS API", "CF Pages API"],
            "models": ["glm-4-plus", "glm-4-flash", "agnes"],
            "version": "1.0.0",
            "port": 8461
        }


if __name__ == "__main__":
    agent = BuilderAgent()
    # 自测
    print("=== Health Check ===")
    print(json.dumps(agent.health_check(), ensure_ascii=False, indent=2))
    print("\n=== Capabilities ===")
    print(json.dumps(agent.get_capabilities(), ensure_ascii=False, indent=2))
    print("\n=== Deploy Check ===")
    print(json.dumps(agent.execute("deploy_check", {}), ensure_ascii=False, indent=2))
