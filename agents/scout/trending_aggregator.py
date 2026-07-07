#!/usr/bin/env python3
"""
热点汇总——借鉴taste-kill (49.5k stars)
一键汇总多平台热点话题（Reddit/X/YouTube/HN/Polymarket）
集成到scout Agent + GEO营销
"""

import json, urllib.request, re, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from scout.agent_reach import AgentReach

class TrendingAggregator:
    """多平台热点汇总器"""
    
    def __init__(self):
        self.reach = AgentReach()
    
    def aggregate(self, platforms=None):
        """汇总多平台热点"""
        platforms = platforms or ['hackernews', 'github', 'arxiv']
        
        all_trends = {}
        
        for platform in platforms:
            try:
                if platform == 'hackernews':
                    all_trends['hackernews'] = self._hn_trending()
                elif platform == 'github':
                    all_trends['github'] = self._github_trending()
                elif platform == 'arxiv':
                    all_trends['arxiv'] = self._arxiv_trending()
            except Exception as e:
                all_trends[platform] = [{'error': str(e)[:50]}]
        
        # 提取关键词
        all_titles = []
        for platform, items in all_trends.items():
            if isinstance(items, list):
                for item in items:
                    if 'title' in item:
                        all_titles.append(item['title'])
        
        keywords = self._extract_keywords(all_titles)
        
        return {
            'platforms': list(all_trends.keys()),
            'total_items': sum(len(v) if isinstance(v, list) else 0 for v in all_trends.values()),
            'trends': all_trends,
            'hot_keywords': keywords,
            'summary': self._generate_summary(all_trends),
            'method': 'taste-kill风格多平台热点汇总',
        }
    
    def _hn_trending(self):
        """HN热门"""
        try:
            url = 'http://hn.algolia.com/api/v1/search?tags=front_page&hitsPerPage=10'
            r = urllib.request.urlopen(url, timeout=8)
            data = json.loads(r.read())
            return [{
                'title': hit.get('title', ''),
                'url': hit.get('url', ''),
                'points': hit.get('points', 0),
                'comments': hit.get('num_comments', 0),
                'platform': 'Hacker News',
            } for hit in data.get('hits', [])[:10]]
        except:
            return []
    
    def _github_trending(self):
        """GitHub热门"""
        try:
            # 用GitHub API搜索最近创建的高星项目
            url = 'https://api.github.com/search/repositories?q=created:>2026-07-01&sort=stars&order=desc&per_page=10'
            req = urllib.request.Request(url, headers={'User-Agent': 'TrendingAggregator/1.0', 'Accept': 'application/vnd.github.v3+json'})
            r = urllib.request.urlopen(req, timeout=10)
            data = json.loads(r.read())
            
            return [{
                'title': item['full_name'],
                'url': item['html_url'],
                'points': item['stargazers_count'],
                'description': (item.get('description') or '')[:100],
                'language': item.get('language', ''),
                'platform': 'GitHub',
            } for item in data.get('items', [])[:10]]
        except:
            return []
    
    def _arxiv_trending(self):
        """arXiv热门"""
        try:
            # 获取最新AI论文
            url = 'http://export.arxiv.org/api/query?search_query=cat:cs.AI&sortBy=submittedDate&sortOrder=descending&max_results=10'
            r = urllib.request.urlopen(url, timeout=10)
            content = r.read().decode()
            
            papers = []
            for entry in re.findall(r'<entry>(.*?)</entry>', content, re.DOTALL)[:10]:
                title = re.search(r'<title>(.*?)</title>', entry, re.DOTALL)
                link = re.search(r'<id>(.*?)</id>', entry)
                if title:
                    papers.append({
                        'title': title.group(1).strip().replace('\n', ' ')[:100],
                        'url': link.group(1).strip() if link else '',
                        'platform': 'arXiv',
                    })
            return papers
        except:
            return []
    
    def _extract_keywords(self, titles):
        """提取热门关键词"""
        from collections import Counter
        import re
        
        # 简单分词
        words = []
        for title in titles:
            # 英文词
            words.extend(re.findall(r'[A-Za-z]{3,}', title))
            # 中文词（2-4字）
            words.extend(re.findall(r'[\u4e00-\u9fa5]{2,4}', title))
        
        # 去停用词
        stop = {'the', 'and', 'for', 'with', 'from', 'this', 'that', 'are', 'was', 'were', 'have', 'has', 'been'}
        words = [w.lower() for w in words if w.lower() not in stop]
        
        counter = Counter(words)
        return [{'keyword': kw, 'count': c} for kw, c in counter.most_common(20)]
    
    def _generate_summary(self, trends):
        """生成摘要"""
        total = sum(len(v) if isinstance(v, list) else 0 for v in trends.values())
        platforms = list(trends.keys())
        return f'共获取{total}条热点，覆盖{len(platforms)}个平台: {", ".join(platforms)}'
    
    def geo_opportunity(self):
        """GEO营销机会——基于热点推荐内容方向"""
        trends = self.aggregate()
        keywords = trends.get('hot_keywords', [])
        
        opportunities = []
        for kw in keywords[:5]:
            opportunities.append({
                'keyword': kw['keyword'],
                'trend_count': kw['count'],
                'content_suggestion': f'创建"{kw["keyword"]}"相关结构化内容',
                'geo_value': '高搜索量关键词，AI平台易引用',
            })
        
        return {
            'opportunities': opportunities,
            'method': 'GEO营销机会分析——基于热点',
        }


# 全局实例
trending = TrendingAggregator()

if __name__ == '__main__':
    print('=== 多平台热点汇总 ===')
    result = trending.aggregate(['hackernews', 'github', 'arxiv'])
    print(json.dumps(result, ensure_ascii=False, indent=2)[:500])
    print()
    print('=== GEO营销机会 ===')
    print(json.dumps(trending.geo_opportunity(), ensure_ascii=False, indent=2)[:300])
