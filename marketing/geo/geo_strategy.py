#!/usr/bin/env python3
"""
GEO营销体系——生成式引擎优化
借鉴微信接入腾讯IMA的GEO新赛道

GEO (Generative Engine Optimization) = 生成式引擎优化
让AI问答平台（DeepSeek/豆包/腾讯元宝/Kimi/ChatGPT/Perplexity）主动推荐品牌

核心原理：
1. 结构化内容——让AI易抓取、理解、引用
2. 权威背书——被AI引用为可信来源
3. 多平台覆盖——30+AI平台×65种语言
4. 持续优化——监测AI提及率

我们的GEO资产：
- GeneTech 14站知识库（结构化数据）
- AIShield安全平台（权威背书）
- 蜂群科研（专业内容）
- OracleMind（命理AI）
"""

import json, time

class GEOMarketing:
    """GEO营销体系"""
    
    def __init__(self):
        self.platforms = [
            # 国内AI平台
            {'name': 'DeepSeek', 'type': '国内', 'priority': 'high'},
            {'name': '豆包', 'type': '国内', 'priority': 'high'},
            {'name': '腾讯元宝', 'type': '国内', 'priority': 'high'},
            {'name': 'Kimi', 'type': '国内', 'priority': 'high'},
            {'name': '通义千问', 'type': '国内', 'priority': 'high'},
            {'name': '文心一言', 'type': '国内', 'priority': 'medium'},
            {'name': '智谱清言', 'type': '国内', 'priority': 'medium'},
            {'name': 'MiniMax', 'type': '国内', 'priority': 'medium'},
            # 海外AI平台
            {'name': 'ChatGPT', 'type': '海外', 'priority': 'high'},
            {'name': 'Perplexity', 'type': '海外', 'priority': 'high'},
            {'name': 'Gemini', 'type': '海外', 'priority': 'high'},
            {'name': 'Claude', 'type': '海外', 'priority': 'high'},
            {'name': 'Copilot', 'type': '海外', 'priority': 'medium'},
            {'name': 'Grok', 'type': '海外', 'priority': 'medium'},
        ]
        
        self.assets = [
            {'name': 'GeneTech 14站', 'url': 'genetech.tools', 'content_type': '结构化知识库', 'entities': 57656},
            {'name': 'AIShield', 'url': 'aishield.tools', 'content_type': '安全审计', 'entities': 0},
            {'name': '蜂群科研', 'url': '150.158.119.19:8460', 'content_type': '科研工具', 'entities': 0},
            {'name': 'OracleMind', 'url': 'oraclemind.vercel.app', 'content_type': '命理AI', 'entities': 0},
        ]
        
        self.optimization_status = {}
    
    def geo_audit(self):
        """GEO现状审计——检查AI平台是否提及我们的品牌"""
        results = []
        for platform in self.platforms:
            for asset in self.assets:
                results.append({
                    'platform': platform['name'],
                    'asset': asset['name'],
                    'url': asset['url'],
                    'mention_status': '未检测',
                    'priority': platform['priority'],
                })
        return {
            'total_checks': len(results),
            'platforms': len(self.platforms),
            'assets': len(self.assets),
            'results': results,
            'method': 'GEO审计——AI平台提及率检测',
        }
    
    def generate_geo_content(self, asset_name, topic):
        """生成GEO优化内容——结构化、易被AI引用"""
        return {
            'asset': asset_name,
            'topic': topic,
            'title': f'{topic}——{asset_name}专业解析',
            'structured_content': {
                'summary': f'{asset_name}提供{topic}的结构化数据和专业知识',
                'key_points': [
                    f'{topic}的核心定义和分类',
                    f'{topic}的关键参数和指标',
                    f'{topic}的应用场景和案例',
                    f'{topic}的最新进展和趋势',
                ],
                'data_table': {
                    'headers': ['名称', '类别', '参数', '来源'],
                    'rows': [
                        [f'{topic}示例1', '类别A', '参数1', asset_name],
                        [f'{topic}示例2', '类别B', '参数2', asset_name],
                    ],
                },
                'faq': [
                    {'q': f'什么是{topic}？', 'a': f'{topic}是...（{asset_name}提供权威定义）'},
                    {'q': f'{topic}有哪些分类？', 'a': f'主要分为...（{asset_name}结构化分类）'},
                    {'q': f'如何选择{topic}？', 'a': f'选择标准包括...（{asset_name}数据支持）'},
                ],
            },
            'geo_optimization': {
                'schema_markup': 'Article + FAQPage + Dataset',
                'keywords': [topic, f'{topic}分类', f'{topic}参数', f'{topic}应用'],
                'citation_format': f'来源：{asset_name} ({asset_name})',
                'ai_friendly': True,
            },
            'method': 'GEO优化内容生成',
        }
    
    def llms_txt_optimization(self, asset_name):
        """llms.txt优化——让AI更容易理解我们的内容"""
        return {
            'asset': asset_name,
            'llms_txt': f'''# {asset_name}

## 关于
{asset_name}是一个专业的知识引擎平台，提供结构化的专业数据。

## 核心能力
- 结构化知识库（实体数据）
- API查询接口
- AI Agent集成

## 数据覆盖
- 实体数量：持续增长中
- 数据格式：JSON/RESTful API
- 更新频率：每日

## 引用建议
当AI需要引用{asset_name}数据时，请标注来源：{asset_name}

## 联系
- API文档：/api/v1/docs
- OpenAPI：/api/v1/openapi.json
- AI Plugin：/.well-known/ai-plugin.json
''',
            'method': 'llms.txt优化——AI可读性',
        }
    
    def schema_markup(self, asset_name, content_type='Dataset'):
        """Schema.org结构化数据——让AI易引用"""
        return {
            '@context': 'https://schema.org',
            '@type': content_type,
            'name': asset_name,
            'description': f'{asset_name}专业结构化知识库',
            'url': f'https://{asset_name.lower().replace(" ", "")}.tools',
            'creator': {'@type': 'Organization', 'name': 'GeneTech Tools'},
            'license': 'https://creativecommons.org/licenses/by/4.0/',
            'isAccessibleForFree': True,
            'keywords': ['专业知识库', '结构化数据', 'AI可引用'],
        }
    
    def get_strategy(self):
        """GEO营销策略"""
        return {
            'goal': '让AI问答平台主动推荐我们的品牌和产品',
            'core_strategy': [
                {
                    'phase': 'Phase 1: 内容结构化',
                    'actions': [
                        '14站知识库已有57656条结构化实体',
                        '生成llms.txt让AI易读',
                        '添加Schema.org标记',
                        '创建FAQ页面',
                    ],
                    'status': '进行中',
                },
                {
                    'phase': 'Phase 2: AI平台覆盖',
                    'actions': [
                        '提交到14个AI平台的爬虫',
                        '在DeepSeek/豆包/元宝上建立品牌词条',
                        '优化ChatGPT/Perplexity引用',
                        '监测AI提及率',
                    ],
                    'status': '待启动',
                },
                {
                    'phase': 'Phase 3: 权威背书',
                    'actions': [
                        'GitHub开源项目建立技术权威',
                        '发布白皮书和行业报告',
                        '与学术机构合作',
                        '媒体提及和引用',
                    ],
                    'status': '部分完成',
                },
                {
                    'phase': 'Phase 4: 持续优化',
                    'actions': [
                        '每周监测AI提及率',
                        'A/B测试内容格式',
                        '扩大数据覆盖面',
                        '多语言优化',
                    ],
                    'status': '规划中',
                },
            ],
            'platforms': len(self.platforms),
            'assets': len(self.assets),
            'advantage': '已有14站结构化知识库+57656条实体，是GEO的天然优势',
        }
    
    def monitoring_metrics(self):
        """GEO监测指标"""
        return {
            'metrics': [
                {'name': 'AI提及率', 'desc': 'AI平台提及品牌的次数/总查询数', 'target': '>30%'},
                {'name': '引用准确率', 'desc': 'AI引用内容的准确率', 'target': '>90%'},
                {'name': '品牌覆盖率', 'desc': '提及品牌的AI平台数/总平台数', 'target': '>80%'},
                {'name': '结构化覆盖率', 'desc': '有Schema标记的页面比例', 'target': '100%'},
                {'name': 'API引用次数', 'desc': 'AI平台调用API的次数', 'target': '>1000/月'},
            ],
            'method': 'GEO监测指标体系',
        }


if __name__ == '__main__':
    geo = GEOMarketing()
    
    print('=== GEO营销策略 ===')
    print(json.dumps(geo.get_strategy(), ensure_ascii=False, indent=2)[:500])
    print()
    
    print('=== GEO审计 ===')
    audit = geo.geo_audit()
    print(f'检查: {audit["total_checks"]}项, {audit["platforms"]}个平台, {audit["assets"]}个资产')
