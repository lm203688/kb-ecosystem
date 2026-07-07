"""
Agent 5: 审计师（Guardian）— 项目安全顾问
职责：违禁词检测、MCP安全扫描、合规审计、法律风险预警
模型：AIShield规则引擎 + glm-4-plus
端口：8450（复用AIShield 8450）
"""

import sys, os, json, time, traceback, urllib.request
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shared.base_agent import BaseAgent
from shared.llm_client import call_llm
from shared.project_db import check_ecs_services


class GuardianAgent(BaseAgent):
    def __init__(self):
        super().__init__("guardian", "项目安全顾问", 8450)

    def execute(self, task: str, params: dict) -> dict:
        start = time.time()
        project_id = params.get("project_id", "default")
        try:
            handlers = {
                "content_scan": self._content_scan,
                "mcp_security_scan": self._mcp_security_scan,
                "compliance_audit": self._compliance_audit,
                "vulnerability_check": self._vulnerability_check,
                "legal_risk_assessment": self._legal_risk_assessment,
                "aishield_status": self._aishield_status,
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

    def _call_aishield(self, endpoint: str, data: dict = None) -> dict:
        """调用AIShield 8450服务"""
        url = f"http://150.158.119.19:8450{endpoint}"
        try:
            if data:
                req = urllib.request.Request(url, data=json.dumps(data).encode(),
                                            headers={"Content-Type": "application/json"})
            else:
                req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=15) as resp:
                return json.loads(resp.read().decode())
        except Exception as e:
            return {"error": str(e)}

    def _content_scan(self, params: dict) -> dict:
        """违禁词检测"""
        content = params.get("content", "")

        # 调用AIShield违禁词检测
        result = self._call_aishield("/api/v1/audit", {"content": content, "type": "text"})

        # LLM深度分析
        if not result.get("error"):
            prompt = f"""分析以下内容的安全风险：

内容：{content[:2000]}

初筛结果：{json.dumps(result, ensure_ascii=False)}

请输出：
1. 风险等级（高/中/低/安全）
2. 具体风险点
3. 修改建议
4. 相关法规依据"""
            analysis = call_llm(prompt, model="glm-4-plus", max_tokens=1000)
            result["deep_analysis"] = analysis

        return result

    def _mcp_security_scan(self, params: dict) -> dict:
        """MCP工具安全扫描"""
        mcp_url = params.get("mcp_url", "")
        result = self._call_aishield("/api/v1/tools/scan", {"url": mcp_url})
        return {"mcp_url": mcp_url, "scan_result": result}

    def _compliance_audit(self, params: dict) -> dict:
        """合规审计"""
        project_id = params.get("project_id", "default")
        audit_type = params.get("type", "general")  # general/data_privacy/ai_content
        materials = params.get("materials", "")

        # AIShield合规检查
        aishield_result = self._call_aishield("/api/v1/stats")

        prompt = f"""你是合规审计专家。进行{audit_type}类型审计：

项目ID：{project_id}
审计材料：{materials[:2000]}

AIShield状态：{json.dumps(aishield_result, ensure_ascii=False)}

请输出：
1. 合规检查清单
2. 发现的合规问题
3. 风险等级
4. 整改建议（按优先级）
5. 法规依据（GDPR/数据安全法/AI法案等）"""

        analysis = call_llm(prompt, model="glm-4-plus", max_tokens=1500)
        return {"audit_type": audit_type, "analysis": analysis, "aishield_stats": aishield_result}

    def _vulnerability_check(self, params: dict) -> dict:
        """漏洞检查"""
        url = params.get("url", "")

        prompt = f"""对以下目标进行安全漏洞评估：

目标：{url}

请按OWASP Top 10输出：
1. 注入风险
2. 认证失效
3. 敏感数据泄露
4. XML外部实体
5. 访问控制失效
6. 安全配置错误
7. XSS
8. 反序列化
9. 已知漏洞组件
10. 日志监控不足

每项给出：风险等级+检查建议"""

        analysis = call_llm(prompt, model="glm-4-plus", max_tokens=1500)
        return {"url": url, "owasp_assessment": analysis}

    def _legal_risk_assessment(self, params: dict) -> dict:
        """法律风险评估"""
        scenario = params.get("scenario", "")

        prompt = f"""你是法律顾问。评估以下场景的法律风险：

场景：{scenario}

请输出：
1. 涉及的法律法规
2. 风险等级（高/中/低）
3. 合规建议
4. 需要的资质/许可
5. 用户协议/隐私政策要点"""

        analysis = call_llm(prompt, model="glm-4-plus", max_tokens=1000)
        return {"legal_assessment": analysis}

    def _auto_pentest(self, params: dict) -> dict:
        """AI渗透测试 — 借鉴strix的自动漏洞扫描+修复建议"""
        target = params.get('target', '')
        if not target:
            return {'error': '请提供目标URL'}
        
        import urllib.request, ssl, json
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        
        findings = []
        
        # 1. HTTP头安全检查
        try:
            req = urllib.request.Request(target, headers={'User-Agent': 'StrixAgent/1.0'})
            resp = urllib.request.urlopen(req, timeout=10, context=ctx)
            headers = dict(resp.headers)
            
            security_headers = {
                'X-Content-Type-Options': '防MIME嗅探',
                'X-Frame-Options': '防点击劫持',
                'Strict-Transport-Security': 'HSTS强制HTTPS',
                'Content-Security-Policy': 'CSP内容安全策略',
                'X-XSS-Protection': 'XSS过滤',
            }
            for h, desc in security_headers.items():
                if h not in headers:
                    findings.append({'severity': 'medium', 'issue': f'缺失{h}', 'fix': f'添加{h}头：{desc}'})
        except Exception as e:
            findings.append({'severity': 'info', 'issue': f'连接异常: {str(e)[:50]}'})
        
        # 2. 常见路径扫描
        common_paths = ['/admin', '/.env', '/.git/config', '/wp-admin', '/api/v1/users', '/debug']
        for path in common_paths:
            try:
                url = target.rstrip('/') + path
                req = urllib.request.Request(url, headers={'User-Agent': 'StrixAgent/1.0'})
                resp = urllib.request.urlopen(req, timeout=5, context=ctx)
                if resp.status == 200:
                    findings.append({'severity': 'high', 'issue': f'{path}可公开访问', 'fix': f'限制{path}的访问权限'})
            except:
                pass
        
        # 3. 生成修复PR建议
        fixes = [f for f in findings if f.get('fix')]
        summary = f'扫描{len(common_paths)+1}项，发现{len(findings)}个问题({len([f for f in findings if f["severity"]=="high"])}高危)'
        
        return {
            'target': target,
            'findings': findings,
            'fixes': fixes,
            'summary': summary,
            'method': 'AI渗透测试(HTTP头+路径扫描+修复建议)'
        }
    
    def _code_quality_scan(self, params: dict) -> dict:
        """代码质量持续监控 — 借鉴SonarQube"""
        code = params.get('code', '')
        if not code:
            return {'error': '请提供代码'}
        
        issues = []
        # 简化版代码质量检查
        lines = code.split('\n')
        for i, line in enumerate(lines):
            # 长行
            if len(line) > 120:
                issues.append({'line': i+1, 'severity': 'minor', 'rule': '行过长(>120字符)', 'fix': '拆分长行'})
            # TODO/FIXME
            if 'TODO' in line or 'FIXME' in line:
                issues.append({'line': i+1, 'severity': 'major', 'rule': '未完成代码', 'fix': '处理TODO/FIXME'})
            # 硬编码密码
            if any(k in line.lower() for k in ['password=', 'passwd=', 'secret=']):
                issues.append({'line': i+1, 'severity': 'critical', 'rule': '硬编码密码', 'fix': '使用环境变量'})
            # eval/exec
            if 'eval(' in line or 'exec(' in line:
                issues.append({'line': i+1, 'severity': 'critical', 'rule': '危险函数(eval/exec)', 'fix': '避免使用eval/exec'})
        
        metrics = {
            'lines': len(lines),
            'issues': len(issues),
            'critical': len([i for i in issues if i['severity'] == 'critical']),
            'major': len([i for i in issues if i['severity'] == 'major']),
            'minor': len([i for i in issues if i['severity'] == 'minor']),
            'quality_score': max(0, 100 - len(issues) * 5),
        }
        
        return {
            'metrics': metrics,
            'issues': issues[:20],
            'summary': f"代码质量{metrics['quality_score']}/100, {metrics['issues']}个问题({metrics['critical']}严重)",
            'method': '代码质量扫描(长行/TODO/硬编码/危险函数)'
        }
    
    def _aishield_status(self, params: dict) -> dict:
        """AIShield服务状态"""
        stats = self._call_aishield("/api/v1/stats")
        health = self._call_aishield("/api/v1/health")
        tools = self._call_aishield("/api/v1/tools")

        return {
            "stats": stats,
            "health": health,
            "tools": tools if isinstance(tools, list) else [tools]
        }

    def get_capabilities(self) -> dict:
        return {
            "agent": "guardian",
            "description": self.description,
            "capabilities": [
                "违禁词检测（AIShield 119规则）",
                "MCP工具安全扫描",
                "合规审计（GDPR/数据安全法/AI法案）",
                "漏洞检查（OWASP Top 10）",
                "法律风险评估",
                "AIShield服务状态监控",
                "项目长期安全跟踪"
            ],
            "tools": ["AIShield 8450服务", "119规则引擎", "21审计工具", "glm-4-plus"],
            "models": ["glm-4-plus"],
            "version": "1.0.0",
            "port": 8450,
            "aishield_integration": "直接复用AIShield 8450端口服务"
        }


if __name__ == "__main__":
    agent = GuardianAgent()
    print("=== Health Check ===")
    print(json.dumps(agent.health_check(), ensure_ascii=False, indent=2))
    print("\n=== Capabilities ===")
    print(json.dumps(agent.get_capabilities(), ensure_ascii=False, indent=2))
    print("\n=== AIShield Status ===")
    print(json.dumps(agent.execute("aishield_status", {}), ensure_ascii=False, indent=2))
