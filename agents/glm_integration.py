#!/usr/bin/env python3
"""
GLM-5.1集成——给专业Agent增加AI能力
智谱AI免费2000万tokens
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

try:
    from glm_config import GLM_CONFIG, is_configured, get_glm_client
    from glm_client import GLMClient
except ImportError:
    GLM_CONFIG = {'api_key': ''}
    def is_configured(): return False
    def get_glm_client(): return None

class AgentWithGLM:
    """带GLM-5.1能力的Agent基类"""
    
    def __init__(self, agent_name):
        self.agent_name = agent_name
        self.glm = get_glm_client() if is_configured() else None
        self.model = 'glm-5.1'
    
    def ask_glm(self, prompt, system_prompt=None, max_tokens=4000):
        """调用GLM-5.1"""
        if not self.glm:
            return {
                'error': 'GLM未配置',
                'hint': '注册智谱账号获取免费2000万tokens: https://www.bigmodel.cn',
                'fallback': '使用本地规则引擎降级',
            }
        
        messages = []
        if system_prompt:
            messages.append({'role': 'system', 'content': system_prompt})
        messages.append({'role': 'user', 'content': prompt})
        
        return self.glm.chat(messages, model=self.model, max_tokens=max_tokens)
    
    def analyze(self, data, task='analyze'):
        """通用分析接口"""
        return self.ask_glm(
            f"分析以下数据:\n{data}",
            system_prompt=f"你是{self.agent_name}，擅长数据分析。"
        )
    
    def status(self):
        """Agent状态"""
        return {
            'agent_name': self.agent_name,
            'glm_enabled': self.glm is not None,
            'model': self.model if self.glm else 'none',
            'glm_configured': is_configured(),
        }


if __name__ == '__main__':
    agent = AgentWithGLM('test_agent')
    print(f'GLM状态: {agent.status()}')
