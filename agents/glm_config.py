#!/usr/bin/env python3
"""
GLM-5.1配置——智谱AI免费2000万tokens
注册地址: https://www.bigmodel.cn/activity/trial-card/BZZIGMITH7

使用方式:
1. 注册智谱账号 → 获取API Key
2. 设置环境变量: export GLM_API_KEY="你的key"
3. 或写入 /home/z/my-project/.env: GLM_API_KEY=你的key

GLM-5.1能力:
- 代码生成与分析（强于GLM-4）
- 长程任务（持续8小时自主工作）
- 智能体（Agent）能力
- 数理推理
"""

import os, json

# GLM配置
GLM_CONFIG = {
    'api_key': os.environ.get('GLM_API_KEY', ''),
    'base_url': 'https://open.bigmodel.cn/api/paas/v4',
    'models': {
        'glm-5.1': {'context': '128K', 'strength': '代码+长程任务', 'free': True},
        'glm-5.2': {'context': '1M', 'strength': '超长上下文', 'free': '试用卡'},
        'glm-4-flash': {'context': '128K', 'strength': '快速响应', 'free': True},
        'glm-4-plus': {'context': '128K', 'strength': '通用', 'free': False},
    },
    'free_quota': '2000万tokens',
    'register_url': 'https://www.bigmodel.cn/activity/trial-card/BZZIGMITH7',
}

# 尝试从.env加载
ENV_FILE = '/home/z/my-project/.env'
if os.path.exists(ENV_FILE):
    for line in open(ENV_FILE):
        line = line.strip()
        if line.startswith('GLM_API_KEY='):
            GLM_CONFIG['api_key'] = line.split('=', 1)[1].strip('"\'')
            break

def get_glm_client():
    """获取GLM客户端"""
    from glm_client import GLMClient
    return GLMClient(api_key=GLM_CONFIG['api_key'])

def is_configured():
    """检查是否已配置API Key"""
    return bool(GLM_CONFIG['api_key'])

def status():
    """配置状态"""
    return {
        'configured': is_configured(),
        'api_key_masked': GLM_CONFIG['api_key'][:8] + '...' if GLM_CONFIG['api_key'] else '未设置',
        'available_models': GLM_CONFIG['models'],
        'free_quota': GLM_CONFIG['free_quota'],
        'register_url': GLM_CONFIG['register_url'],
        'note': '注册智谱账号获取免费2000万tokens' if not is_configured() else '已配置，可使用GLM-5.1',
    }


if __name__ == '__main__':
    print(json.dumps(status(), ensure_ascii=False, indent=2))
