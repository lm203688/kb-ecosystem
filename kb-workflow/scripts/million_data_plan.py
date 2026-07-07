#!/usr/bin/env python3
"""
知识引擎百万数据目标——数据收集加速器
14站×百万数据=1400万条目标
"""

import json, os, time

# 14站数据目标
SITE_TARGETS = {
    'genetech': {'target': 100000, 'current': 1516, 'topic': '基因技术', 'sources': ['PubMed', 'ChEMBL', 'PubChem']},
    'tcm': {'target': 100000, 'current': 820, 'topic': '中医药', 'sources': ['中医药数据库', 'PubMed']},
    'agent': {'target': 50000, 'current': 450, 'topic': 'Agent生态', 'sources': ['GitHub', 'MCP']},
    'robot': {'target': 50000, 'current': 380, 'topic': '机器人配件', 'sources': ['Robotis', '制造商']},
    'quantum': {'target': 50000, 'current': 290, 'topic': '量子计算', 'sources': ['arXiv', 'IBM Quantum']},
    'brain': {'target': 50000, 'current': 520, 'topic': '脑科学', 'sources': ['PubMed', 'NeuroMorpho']},
    'nuclear': {'target': 50000, 'current': 340, 'topic': '核能', 'sources': ['IAEA', '科学期刊']},
    'exo': {'target': 50000, 'current': 280, 'topic': '系外科学', 'sources': ['NASA', 'arXiv']},
    'alien': {'target': 50000, 'current': 310, 'topic': '外星矿物', 'sources': ['Mindat', '研究论文']},
    'deepsea': {'target': 50000, 'current': 260, 'topic': '深海技术', 'sources': ['NOAA', '研究论文']},
    'newenergy': {'target': 50000, 'current': 350, 'topic': '新能源', 'sources': ['DOE', '专利']},
    'lifescience': {'target': 100000, 'current': 480, 'topic': '生命科学', 'sources': ['PubMed', 'ClinicalTrials']},
    'biocomputing': {'target': 50000, 'current': 220, 'topic': '生物计算', 'sources': ['arXiv', 'GitHub']},
    'bionicai': {'target': 50000, 'current': 190, 'topic': '仿生AI', 'sources': ['IEEE', '研究论文']},
}

def get_progress():
    """获取14站数据进度"""
    total_target = sum(s['target'] for s in SITE_TARGETS.values())
    total_current = sum(s['current'] for s in SITE_TARGETS.values())
    
    sites = []
    for key, s in SITE_TARGETS.items():
        pct = round(s['current'] / s['target'] * 100, 2)
        sites.append({
            'site': key,
            'topic': s['topic'],
            'current': s['current'],
            'target': s['target'],
            'progress': pct,
            'sources': s['sources'],
            'eta_days': round((s['target'] - s['current']) / 100, 1),  # 每天100条
        })
    
    return {
        'total_target': total_target,
        'total_current': total_current,
        'total_progress': round(total_current / total_target * 100, 2),
        'sites': sites,
        'method': '百万数据目标计划——14站×百万',
    }

def generate_collection_plan(site_key, batch_size=100):
    """生成数据收集计划"""
    site = SITE_TARGETS.get(site_key, {})
    if not site:
        return {'error': '站点不存在'}
    
    remaining = site['target'] - site['current']
    batches = remaining // batch_size
    
    plan = {
        'site': site_key,
        'topic': site['topic'],
        'current': site['current'],
        'target': site['target'],
        'remaining': remaining,
        'batch_size': batch_size,
        'total_batches': batches,
        'estimated_days': round(batches / 10, 1),  # 每天10批
        'sources': site['sources'],
        'plan': [
            {'batch': i+1, 'source': site['sources'][i % len(site['sources'])], 'count': batch_size}
            for i in range(min(batches, 20))  # 显示前20批
        ],
        'method': '数据收集加速计划',
    }
    return plan

if __name__ == '__main__':
    import sys
    site = sys.argv[1] if len(sys.argv) > 1 else None
    
    if site:
        result = generate_collection_plan(site)
    else:
        result = get_progress()
    
    print(json.dumps(result, ensure_ascii=False, indent=2))
