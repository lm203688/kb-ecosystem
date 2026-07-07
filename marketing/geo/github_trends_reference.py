#!/usr/bin/env python3
"""
GitHub月榜项目参考——给所有项目和专业Agent借鉴
2026年7月精选6个增长最快项目
"""

import json

PROJECTS = [
    {
        'name': 'Agent-Reach',
        'github': 'Panniantong/Agent-Reach',
        'stars': '51.8k',
        'growth': '+30.0k',
        'description': '让AI代理浏览搜索多平台内容（Twitter/Reddit/YouTube/GitHub/B站/小红书）',
        'our_application': {
            'scout_agent': '侦察者Agent集成——多平台数据采集',
            'researcher_agent': '研究员Agent——跨平台文献搜索',
            'geneTech': '14站知识引擎——多源数据采集',
            'aishield': '安全情报——多平台安全资讯',
        },
        'action': '集成到scout和researcher Agent',
    },
    {
        'name': 'OpenMontage',
        'github': 'calesthio/OpenMontage',
        'stars': '34.1k',
        'growth': '+29.2k',
        'description': 'AI助手变专业视频制作工作室，12条管线52个工具',
        'our_application': {
            'game_agent': '游戏Agent——游戏宣传视频自动生成',
            'geneTech': '知识引擎——科普视频自动制作',
            'swarmlabs': '蜂群科研——实验过程视频记录',
        },
        'action': '集成到game_agent和营销体系',
    },
    {
        'name': 'codebase-memory-mcp',
        'github': 'DeusData/codebase-memory-mcp',
        'stars': '27.1k',
        'growth': '+23.6k',
        'description': '极速构建代码知识库，秒级查询代码信息',
        'our_application': {
            'builder_agent': '建造者Agent——代码审查和生成',
            'aishield': '安全扫描——代码漏洞检测加速',
            'all_projects': '所有项目的代码知识库',
        },
        'action': '集成到builder和guardian Agent',
    },
    {
        'name': 'taste-kill',
        'github': 'anhorn/tast3e!KiLLL',
        'stars': '49.5k',
        'growth': '+21.4k',
        'description': '一键汇总多平台热点话题（Reddit/X/YouTube/HN/Polymarket）',
        'our_application': {
            'scout_agent': '侦察者——热点话题追踪',
            'marketing': 'GEO营销——热点内容借势',
            'geneTech': '知识引擎——前沿趋势捕捉',
        },
        'action': '集成到scout和GEO营销',
    },
    {
        'name': 'SKILLSpector',
        'github': 'NVIDIA/SKILLSpector',
        'stars': '12.1k',
        'growth': '+10.9k',
        'description': '检查AI代理技能的安全漏洞，检测恶意模式',
        'our_application': {
            'aishield': '直接核心能力——Agent技能安全扫描',
            'guardian_agent': '守护者Agent——技能安装前安全检查',
            'all_agents': '所有专业Agent——安全自检',
        },
        'action': '集成到AIShield核心功能',
    },
    {
        'name': 'pm-skills',
        'github': 'phuryn/pm-skills',
        'stars': '22.7k',
        'growth': '+410.7k',
        'description': '产品经理全流程1004+实用技能工具',
        'our_application': {
            'strategist_agent': '战略家Agent——产品规划',
            'designer_agent': '设计师Agent——产品设计',
            'all_projects': '所有项目——产品管理最佳实践',
        },
        'action': '集成到strategist和designer Agent',
    },
]

def get_reference_report():
    """生成参考报告"""
    return {
        'total_projects': len(PROJECTS),
        'total_stars': sum(float(p['stars'].replace('k','')) for p in PROJECTS),
        'projects': PROJECTS,
        'summary': '这6个项目代表了AI Agent生态的最新趋势：多平台搜索、视频制作、代码知识库、热点追踪、安全扫描、技能市场',
        'our_advantage': '我们已有14站知识库+AIShield安全平台+8个专业Agent，可以快速借鉴这些项目的能力',
    }

def get_integration_plan():
    """集成计划"""
    return {
        'phase1_immediate': [
            'SKILLSpector → AIShield（安全扫描是核心能力）',
            'codebase-memory-mcp → builder/guardian Agent',
        ],
        'phase2_week': [
            'Agent-Reach → scout/researcher Agent',
            'taste-kill → scout Agent + GEO营销',
        ],
        'phase3_month': [
            'OpenMontage → game_agent + 营销视频',
            'pm-skills → strategist/designer Agent',
        ],
    }


if __name__ == '__main__':
    report = get_reference_report()
    print(f'参考项目: {report["total_projects"]}个, 总星数: {report["total_stars"]}k')
    print()
    for p in PROJECTS:
        print(f'### {p["name"]} ({p["stars"]}, {p["growth"]})')
        print(f'  描述: {p["description"]}')
        print(f'  我们的应用: {list(p["our_application"].keys())}')
        print(f'  行动: {p["action"]}')
        print()
    
    plan = get_integration_plan()
    print('=== 集成计划 ===')
    for phase, items in plan.items():
        print(f'{phase}:')
        for item in items:
            print(f'  - {item}')
