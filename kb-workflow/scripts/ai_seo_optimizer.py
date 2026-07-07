#!/usr/bin/env python3
"""
AI搜索优化引擎——借鉴图1-3/6的AI搜索优化建议
3个误区避免+AI优先推荐策略
"""

import json, os

# 3个AI搜索误区
MISTAKES = {
    'mistake1': {
        'title': '还在用传统SEO关键词堆砌',
        'problem': 'AI大模型(豆包/DeepSeek/Kimi)理解的是语义,不是词频',
        'bad_example': '优质工业阀门厂家批发',
        'good_example': '我们如何帮助某化工企业降低30%阀门故障率——工业阀门选型指南',
        'fix': '用自然语义写作,避免关键词堆砌',
    },
    'mistake2': {
        'title': '以XX存XX的套路文案',
        'problem': 'AI搜索引擎给活跃更新的站点更高权重',
        'fix': '每周至少针对行业新问题产出2篇深度解读',
    },
    'mistake3': {
        'title': '自说自话,忘了AI耳听八方',
        'problem': '产品介绍写得再漂亮,不如一条行业烙印/真实案例',
        'fix': '加入被寥的信息——行业报告/真实案例/第三方背书',
    },
}

def optimize_content(site_key, content):
    """优化内容——AI搜索优先"""
    issues = []
    score = 100
    
    # 检查误区1: 关键词堆砌
    text = content.get('text', '')
    words = text.split()
    if len(words) > 0:
        unique_ratio = len(set(words)) / len(words)
        if unique_ratio < 0.4:
            issues.append({'mistake': 'mistake1', 'severity': 'high', 'issue': '词汇重复率高,可能被AI判为关键词堆砌'})
            score -= 20
    
    # 检查误区2: 更新频率
    last_update = content.get('last_update', '')
    if not last_update:
        issues.append({'mistake': 'mistake2', 'severity': 'medium', 'issue': '缺少更新时间,AI会认为信息过时'})
        score -= 10
    
    # 检查误区3: 第三方背书
    has_case = any(kw in text for kw in ['案例', '报告', '验证', '测试', '案例', '客户', '成功'])
    if not has_case:
        issues.append({'mistake': 'mistake3', 'severity': 'medium', 'issue': '缺少真实案例/第三方背书,AI不优先推荐'})
        score -= 15
    
    # AI优先推荐策略
    recommendations = []
    if not any(kw in text for kw in ['行业', '标准', '认证']):
        recommendations.append('加入行业标准和认证信息')
    if not any(kw in text for kw in ['对比', 'vs', '比较']):
        recommendations.append('加入竞品对比分析')
    if not any(kw in text for kw in ['数据', '统计', '研究']):
        recommendations.append('加入数据支撑和研究引用')
    
    return {
        'site': site_key,
        'score': max(0, score),
        'grade': 'A' if score >= 90 else 'B' if score >= 75 else 'C' if score >= 60 else 'D',
        'issues': issues,
        'recommendations': recommendations,
        'mistakes_checked': list(MISTAKES.keys()),
        'method': 'AI搜索优化（3误区避免+AI优先推荐策略）',
    }

def generate_weekly_plan(site_key, topic):
    """生成每周内容计划——每周2篇深度解读"""
    return {
        'site': site_key,
        'topic': topic,
        'weekly_plan': [
            {'day': '周一', 'task': f'{topic}行业最新动态解读', 'type': '深度解读'},
            {'day': '周四', 'task': f'{topic}实际应用案例分析', 'type': '案例研究'},
        ],
        'seo_tips': [
            '用自然语义写作,避免关键词堆砌',
            '加入真实案例和第三方背书',
            '每周至少更新2篇深度内容',
            '加入行业标准和认证信息',
        ],
        'method': '每周内容计划（AI搜索权重优化）',
    }

if __name__ == '__main__':
    # 测试
    result = optimize_content('genetech', {'text': '基因技术CRISPR基因编辑基因治疗基因基因基因', 'last_update': '2026-07-07'})
    print(json.dumps(result, ensure_ascii=False, indent=2))
