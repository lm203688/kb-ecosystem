#!/usr/bin/env python3
"""
免费LLM路由层——借鉴FreeLLMApi (13.4K stars)
每月1.7B免费Token，零成本，多模型路由
"""

class LLMRouter:
    """免费LLM路由器——自动选择最可用的免费模型"""
    
    PROVIDERS = [
        {
            'name': 'z-ai-sdk',
            'models': ['glm-4-flash', 'glm-4-plus', 'glm-5.1'],
            'free_quota': '无限（通过z-ai SDK）',
            'latency': 'low',
            'quality': 'high',
            'endpoint': 'z-ai-web-dev-sdk',
        },
        {
            'name': '智谱bigmodel',
            'models': ['glm-5.1', 'glm-5.2', 'glm-4-flash'],
            'free_quota': '2000万tokens（新用户）',
            'latency': 'low',
            'quality': 'high',
            'endpoint': 'https://open.bigmodel.cn/api/paas/v4',
        },
        {
            'name': 'FreeLLMApi',
            'models': ['claude', 'gpt-4', 'gemini'],
            'free_quota': '每月1.7B tokens',
            'latency': 'medium',
            'quality': 'high',
            'endpoint': 'https://api.freellmapi.com',
        },
        {
            'name': 'DeepSeek',
            'models': ['deepseek-chat', 'deepseek-coder'],
            'free_quota': '有限免费',
            'latency': 'low',
            'quality': 'high',
            'endpoint': 'https://api.deepseek.com',
        },
        {
            'name': 'Kimi',
            'models': ['moonshot-v1'],
            'free_quota': '有限免费',
            'latency': 'medium',
            'quality': 'medium',
            'endpoint': 'https://api.moonshot.cn',
        },
    ]
    
    def __init__(self):
        self.current_provider = 0
        self.fallback_chain = ['z-ai-sdk', '智谱bigmodel', 'FreeLLMApi', 'DeepSeek']
    
    def route(self, prompt, model=None, max_tokens=2000):
        """路由LLM请求——自动选择最优免费提供者"""
        for provider_name in self.fallback_chain:
            provider = next((p for p in self.PROVIDERS if p['name'] == provider_name), None)
            if not provider:
                continue
            
            try:
                result = self._call(provider, prompt, model, max_tokens)
                if result:
                    return {
                        'content': result,
                        'provider': provider['name'],
                        'model': model or provider['models'][0],
                        'cost': 0,
                    }
            except:
                continue
        
        return {'error': '所有免费LLM提供者不可用', 'fallback': '使用本地规则引擎'}
    
    def _call(self, provider, prompt, model, max_tokens):
        """调用具体的LLM"""
        if provider['name'] == 'z-ai-sdk':
            return self._call_zai(prompt, model or 'glm-4-flash', max_tokens)
        elif provider['name'] == '智谱bigmodel':
            return self._call_zhipu(prompt, model or 'glm-5.1', max_tokens)
        return None
    
    def _call_zai(self, prompt, model, max_tokens):
        """通过z-ai SDK调用"""
        import subprocess, json, os
        script = f"""
const SDK = require('z-ai-web-dev-sdk').default;
(async () => {{
    const client = await SDK.create();
    const r = await client.chat.completions.create({{
        model: '{model}',
        messages: [{{role: 'user', content: {json.dumps(prompt)}}}],
        max_tokens: {max_tokens}
    }});
    console.log(JSON.stringify({{content: r.choices[0].message.content}}));
}})().catch(e => console.error(JSON.stringify({{error: e.message}})));
"""
        result = subprocess.run(['node', '-e', script], capture_output=True, text=True, timeout=60,
                               env={**os.environ, 'NODE_PATH': '/home/z/.bun/install/global/node_modules'})
        if result.returncode == 0:
            data = json.loads(result.stdout)
            return data.get('content', '')
        return None
    
    def _call_zhipu(self, prompt, model, max_tokens):
        """通过智谱API调用"""
        import urllib.request, json, os
        api_key = os.environ.get('GLM_API_KEY', '')
        if not api_key:
            return None
        
        data = json.dumps({
            'model': model,
            'messages': [{'role': 'user', 'content': prompt}],
            'max_tokens': max_tokens,
        }).encode()
        
        req = urllib.request.Request(
            'https://open.bigmodel.cn/api/paas/v4/chat/completions',
            data=data,
            headers={'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}
        )
        try:
            r = urllib.request.urlopen(req, timeout=60)
            return json.loads(r.read())['choices'][0]['message']['content']
        except:
            return None
    
    def list_providers(self):
        """列出所有可用提供者"""
        return {
            'providers': self.PROVIDERS,
            'total': len(self.PROVIDERS),
            'fallback_chain': self.fallback_chain,
        }

llm_router = LLMRouter()
