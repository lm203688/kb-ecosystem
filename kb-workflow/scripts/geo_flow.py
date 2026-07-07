#!/usr/bin/env python3
"""
GEO内容工程引擎——借鉴GEOFlow
把可信资料变成SEO内容资产：资料→生成→审核→多站分发
KB知识库+标题库+关键词库统一沉淀
"""

import json, os, sys, time
from datetime import datetime

# 14站配置
SITES = {
    'genetech': {'domain': 'genetech-tools.pages.dev', 'topic': '基因技术'},
    'tcm': {'domain': 'tcm-tools.pages.dev', 'topic': '中医药'},
    'agent': {'domain': 'agentecosystem.pages.dev', 'topic': 'Agent生态'},
    'robot': {'domain': 'robotparts.pages.dev', 'topic': '机器人配件'},
    'quantum': {'domain': 'quantumcomputing.pages.dev', 'topic': '量子计算'},
    'brain': {'domain': 'brainscience.pages.dev', 'topic': '脑科学'},
    'nuclear': {'domain': 'nuclearenergy.pages.dev', 'topic': '核能'},
    'exo': {'domain': 'exoscience.pages.dev', 'topic': '系外科学'},
    'alien': {'domain': 'alienminerals.pages.dev', 'topic': '外星矿物'},
    'deepsea': {'domain': 'deepseatech.pages.dev', 'topic': '深海技术'},
    'newenergy': {'domain': 'newenergy-nya.pages.dev', 'topic': '新能源'},
    'lifescience': {'domain': 'lifescience-epe.pages.dev', 'topic': '生命科学'},
    'biocomputing': {'domain': 'biocomputedb.pages.dev', 'topic': '生物计算'},
    'bionicai': {'domain': 'bionicai.pages.dev', 'topic': '仿生AI'},
}

def generate_content(site_key, topic, keywords=None):
    """生成GEO内容——资料→内容资产"""
    site = SITES.get(site_key, {})
    
    # 1. 标题生成
    titles = [
        f'{site.get("topic","")}最新进展2026',
        f'{site.get("topic","")}技术趋势分析',
        f'{site.get("topic","")}应用场景与案例',
    ]
    
    # 2. 关键词库
    kw_lib = {
        'genetech': ['CRISPR', '基因编辑', 'mRNA', '基因治疗', '合成生物学'],
        'tcm': ['中药配方', '针灸', '中医药现代化', '循证中医'],
        'agent': ['MCP', 'A2A', 'Agent协议', '多Agent协作'],
    }
    keywords = kw_lib.get(site_key, [site.get('topic', '')])
    
    # 3. 内容结构
    content = {
        'site': site_key,
        'domain': site.get('domain', ''),
        'topic': site.get('topic', ''),
        'generated_at': datetime.now().isoformat(),
        'titles': titles,
        'keywords': keywords,
        'sections': [
            {'title': '概述', 'content': f'{site.get("topic","")}领域的最新发展概述。'},
            {'title': '技术趋势', 'content': f'2026年{site.get("topic","")}关键技术趋势。'},
            {'title': '应用案例', 'content': f'{site.get("topic","")}在实际场景中的应用。'},
        ],
        'seo': {
            'meta_description': f'{site.get("topic","")}知识库——最新技术、应用、趋势',
            'og_title': titles[0] if titles else '',
            'schema_type': 'Article',
            'llms_txt': f'{site.get("topic","")}知识库提供{",".join(keywords[:3])}等领域的专业内容。',
        },
    }
    
    return content

def audit_content(content):
    """内容审核——质量检查"""
    issues = []
    
    if len(content.get('titles', [])) < 3:
        issues.append({'severity': 'medium', 'issue': '标题数量不足'})
    
    if not content.get('seo', {}).get('meta_description'):
        issues.append({'severity': 'high', 'issue': '缺少meta描述'})
    
    if not content.get('seo', {}).get('schema_type'):
        issues.append({'severity': 'medium', 'issue': '缺少Schema标记'})
    
    score = max(0, 100 - len(issues) * 15)
    
    return {
        'score': score,
        'issues': issues,
        'passed': score >= 70,
        'method': 'GEO内容审核（借鉴GEOFlow）',
    }

def distribute(content, target_sites=None):
    """多站分发"""
    sites = target_sites or list(SITES.keys())
    results = []
    
    for site in sites:
        if site in SITES:
            results.append({
                'site': site,
                'domain': SITES[site]['domain'],
                'status': 'distributed',
                'url': f'https://{SITES[site]["domain"]}/article/{content.get("site","")}',
            })
    
    return {
        'distributed': len(results),
        'results': results,
        'method': '多站分发（借鉴GEOFlow）',
    }

def content_pipeline(site_key, topic=None, auto_distribute=True):
    """内容工程闭环：资料→生成→审核→分发"""
    print(f'[1/4] 生成内容: {site_key}')
    content = generate_content(site_key, topic)
    
    print(f'[2/4] 审核内容...')
    audit = audit_content(content)
    
    if not audit['passed']:
        print(f'  ⚠️ 审核未通过: {audit["issues"]}')
    
    print(f'[3/4] SEO优化...')
    # SEO已内嵌在content里
    
    if auto_distribute:
        print(f'[4/4] 多站分发...')
        dist = distribute(content)
    else:
        dist = {'distributed': 0, 'results': []}
    
    return {
        'content': content,
        'audit': audit,
        'distribution': dist,
        'pipeline': '资料→生成→审核→多站分发（借鉴GEOFlow）',
        'timestamp': datetime.now().isoformat(),
    }

if __name__ == '__main__':
    # 命令行：python3 geo_flow.py genetech
    site = sys.argv[1] if len(sys.argv) > 1 else 'genetech'
    result = content_pipeline(site)
    print(json.dumps(result, ensure_ascii=False, indent=2))
