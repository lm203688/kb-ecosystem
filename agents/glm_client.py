#!/usr/bin/env python3
"""
GLM-5.1 API客户端——智谱AI免费2000万tokens
用于专业Agent增强能力

注册地址: https://bigmodel.cn
API文档: https://docs.bigmodel.cn
免费额度: 新用户注册送2000万tokens
"""

import json, os, urllib.request

class GLMClient:
    """GLM-5.1 API客户端"""
    
    BASE_URL = "https://open.bigmodel.cn/api/paas/v4"
    
    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get('GLM_API_KEY', '')
        if not self.api_key:
            print("警告: 未设置GLM_API_KEY环境变量")
            print("注册地址: https://www.bigmodel.cn/activity/trial-card/BZZIGMITH7")
    
    def chat(self, messages, model="glm-5.1", temperature=0.7, max_tokens=4000):
        """调用GLM-5.1对话API"""
        if not self.api_key:
            return {"error": "未设置API Key", "fallback": "请设置GLM_API_KEY环境变量"}
        
        url = f"{self.BASE_URL}/chat/completions"
        data = json.dumps({
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }).encode()
        
        req = urllib.request.Request(url, data=data, headers={
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        })
        
        try:
            r = urllib.request.urlopen(req, timeout=60)
            result = json.loads(r.read())
            return {
                "content": result["choices"][0]["message"]["content"],
                "model": result.get("model", model),
                "usage": result.get("usage", {}),
                "status": "ok",
            }
        except Exception as e:
            return {"error": str(e), "status": "failed"}
    
    def analyze_code(self, code, task="review"):
        """代码分析"""
        prompts = {
            "review": "分析以下代码的安全漏洞、性能问题和最佳实践建议：\n",
            "optimize": "优化以下代码的性能和可读性：\n",
            "document": "为以下代码生成详细的中文文档注释：\n",
            "test": "为以下代码生成单元测试用例：\n",
            "refactor": "重构以下代码，提高可维护性：\n",
        }
        prompt = prompts.get(task, prompts["review"])
        return self.chat([
            {"role": "system", "content": "你是高级软件工程师，擅长代码分析和安全审计。"},
            {"role": "user", "content": prompt + code},
        ])
    
    def security_audit(self, code, target_type="web"):
        """安全审计——配合AIShield"""
        return self.chat([
            {"role": "system", "content": "你是安全审计专家，擅长发现代码中的安全漏洞。"},
            {"role": "user", "content": f"对以下{target_type}代码进行安全审计，列出所有潜在漏洞、严重程度和修复建议：\n{code}"},
        ])
    
    def research_analysis(self, topic, papers=None):
        """科研分析——配合蜂群科研"""
        context = f"\n参考论文: {papers}" if papers else ""
        return self.chat([
            {"role": "system", "content": "你是科研分析专家，擅长文献综述和实验设计。"},
            {"role": "user", "content": f"分析主题: {topic}{context}\n请给出：1.研究现状 2.关键发现 3.实验建议 4.潜在突破点"},
        ], max_tokens=4000)
    
    def game_design(self, game_type, theme):
        """游戏设计——配合游戏Agent"""
        return self.chat([
            {"role": "system", "content": "你是游戏设计师，擅长关卡设计、数值平衡和游戏机制设计。"},
            {"role": "user", "content": f"设计一个{game_type}游戏，主题: {theme}。包括：1.核心玩法 2.关卡设计 3.数值平衡 4.美术风格建议"},
        ])
    
    def list_models(self):
        """列出可用模型"""
        return {
            "models": [
                {"id": "glm-5.1", "name": "GLM-5.1", "context": "128K", "strength": "代码+长程任务", "free": True},
                {"id": "glm-5.2", "name": "GLM-5.2", "context": "1M", "strength": "超长上下文", "free": "试用卡"},
                {"id": "glm-4-flash", "name": "GLM-4-Flash", "context": "128K", "strength": "快速响应", "free": True},
                {"id": "glm-4-plus", "name": "GLM-4-Plus", "context": "128K", "strength": "通用能力", "free": False},
            ],
            "free_quota": "新用户注册送2000万tokens",
            "register_url": "https://www.bigmodel.cn/activity/trial-card/BZZIGMITH7",
        }


if __name__ == '__main__':
    client = GLMClient()
    # 测试
    print("=== 可用模型 ===")
    print(json.dumps(client.list_models(), ensure_ascii=False, indent=2))
    
    # 测试代码分析
    print("\n=== 代码分析测试 ===")
    result = client.analyze_code("def login(user, pwd):\n  sql = f\"SELECT * FROM users WHERE name='{user}' AND pwd='{pwd}'\"\n  return execute(sql)", "review")
    print(json.dumps(result, ensure_ascii=False, indent=2)[:200])
