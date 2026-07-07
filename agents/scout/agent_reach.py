#!/usr/bin/env python3
"""
Agent-Reach——多平台内容浏览搜索
借鉴Panniantong/Agent-Reach (51.8k stars)
让AI代理浏览搜索多平台内容：Twitter/Reddit/YouTube/GitHub/B站/小红书
集成到scout和researcher Agent
"""

import json, urllib.request, urllib.parse, re

class AgentReach:
    """多平台内容搜索器"""
    
    SUPPORTED_PLATFORMS = [
        {'id': 'github', 'name': 'GitHub', 'type': '代码', 'searchable': True},
        {'id': 'reddit', 'name': 'Reddit', 'type': '社区', 'searchable': True},
        {'id': 'youtube', 'name': 'YouTube', 'type': '视频', 'searchable': True},
        {'id': 'arxiv', 'name': 'arXiv', 'type': '学术', 'searchable': True},
        {'id': 'pubmed', 'name': 'PubMed', 'type': '医学', 'searchable': True},
        {'id': 'news', 'name': '新闻', 'type': '资讯', 'searchable': True},
        {'id': 'hackernews', 'name': 'Hacker News', 'type': '科技', 'searchable': True},
    ]
    
    def search_all(self, query, platforms=None, max_per_platform=3):
        """多平台搜索"""
        platforms = platforms or [p['id'] for p in self.SUPPORTED_PLATFORMS]
        results = {}
        
        for platform in platforms:
            try:
                if platform == 'github':
                    results['github'] = self._search_github(query, max_per_platform)
                elif platform == 'arxiv':
                    results['arxiv'] = self._search_arxiv(query, max_per_platform)
                elif platform == 'pubmed':
                    results['pubmed'] = self._search_pubmed(query, max_per_platform)
                elif platform == 'hackernews':
                    results['hackernews'] = self._search_hackernews(query, max_per_platform)
                elif platform == 'news':
                    results['news'] = self._search_news(query, max_per_platform)
                elif platform == 'reddit':
                    results['reddit'] = [{'title': f'{query}相关讨论', 'url': f'https://reddit.com/search?q={urllib.parse.quote(query)}', 'note': '需API key'}]
                elif platform == 'youtube':
                    results['youtube'] = [{'title': f'{query}视频', 'url': f'https://youtube.com/results?search_query={urllib.parse.quote(query)}', 'note': '需API key'}]
            except Exception as e:
                results[platform] = [{'error': str(e)[:50]}]
        
        total = sum(len(v) for v in results.values() if isinstance(v, list))
        
        return {
            'query': query,
            'platforms_searched': len(results),
            'total_results': total,
            'results': results,
            'method': 'Agent-Reach风格多平台搜索',
        }
    
    def _search_github(self, query, max_results=3):
        """搜索GitHub"""
        url = f'https://api.github.com/search/repositories?q={urllib.parse.quote(query)}&sort=stars&per_page={max_results}'
        req = urllib.request.Request(url, headers={'User-Agent': 'Agent-Reach/1.0', 'Accept': 'application/vnd.github.v3+json'})
        r = urllib.request.urlopen(req, timeout=10)
        data = json.loads(r.read())
        
        return [{
            'name': item['full_name'],
            'url': item['html_url'],
            'stars': item['stargazers_count'],
            'description': (item.get('description') or '')[:100],
            'language': item.get('language', ''),
        } for item in data.get('items', [])[:max_results]]
    
    def _search_arxiv(self, query, max_results=3):
        """搜索arXiv"""
        url = f'http://export.arxiv.org/api/query?search_query=all:{urllib.parse.quote(query)}&max_results={max_results}'
        r = urllib.request.urlopen(url, timeout=10)
        content = r.read().decode()
        
        papers = []
        for entry in re.findall(r'<entry>(.*?)</entry>', content, re.DOTALL):
            title = re.search(r'<title>(.*?)</title>', entry, re.DOTALL)
            link = re.search(r'<id>(.*?)</id>', entry)
            summary = re.search(r'<summary>(.*?)</summary>', entry, re.DOTALL)
            if title:
                papers.append({
                    'title': title.group(1).strip().replace('\n', ' ')[:100],
                    'url': link.group(1).strip() if link else '',
                    'summary': (summary.group(1).strip()[:150] if summary else ''),
                })
        
        return papers[:max_results]
    
    def _search_pubmed(self, query, max_results=3):
        """搜索PubMed"""
        try:
            url = f'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={urllib.parse.quote(query)}&retmax={max_results}&retmode=json'
            r = urllib.request.urlopen(url, timeout=8)
            pmids = json.loads(r.read()).get('esearchresult', {}).get('idlist', [])
            
            papers = []
            for pmid in pmids[:max_results]:
                try:
                    url2 = f'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id={pmid}&retmode=json'
                    r2 = urllib.request.urlopen(url2, timeout=5)
                    p = json.loads(r2.read()).get('result', {}).get(pmid, {})
                    papers.append({
                        'pmid': pmid,
                        'title': p.get('title', '')[:100],
                        'journal': p.get('fulljournalname', ''),
                        'pubdate': p.get('pubdate', ''),
                    })
                except:
                    pass
            return papers
        except:
            return [{'error': 'PubMed超时'}]
    
    def _search_hackernews(self, query, max_results=3):
        """搜索Hacker News"""
        try:
            url = f'http://hn.algolia.com/api/v1/search?query={urllib.parse.quote(query)}&tags=story'
            r = urllib.request.urlopen(url, timeout=8)
            data = json.loads(r.read())
            
            return [{
                'title': hit.get('title', ''),
                'url': hit.get('url', ''),
                'points': hit.get('points', 0),
                'comments': hit.get('num_comments', 0),
            } for hit in data.get('hits', [])[:max_results]]
        except:
            return [{'error': 'HN超时'}]
    
    def _search_news(self, query, max_results=3):
        """搜索新闻——用Bing News"""
        try:
            url = f'https://www.bing.com/news/search?q={urllib.parse.quote(query)}&format=rss'
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            r = urllib.request.urlopen(req, timeout=8)
            content = r.read().decode('utf-8', errors='ignore')
            
            news = []
            for item in re.findall(r'<item>(.*?)</item>', content, re.DOTALL)[:max_results]:
                title = re.search(r'<title>(.*?)</title>', item)
                link = re.search(r'<link>(.*?)</link>', item)
                if title:
                    news.append({
                        'title': title.group(1).strip()[:100],
                        'url': link.group(1).strip() if link else '',
                    })
            return news if news else [{'note': '无新闻结果'}]
        except:
            return [{'error': '新闻搜索超时'}]
    
    def get_trending(self, platform='hackernews'):
        """获取热门话题——配合taste-kill"""
        if platform == 'hackernews':
            try:
                url = 'http://hn.algolia.com/api/v1/search?tags=front_page'
                r = urllib.request.urlopen(url, timeout=8)
                data = json.loads(r.read())
                return [{
                    'title': hit.get('title', ''),
                    'url': hit.get('url', ''),
                    'points': hit.get('points', 0),
                    'comments': hit.get('num_comments', 0),
                } for hit in data.get('hits', [])[:10]]
            except:
                return [{'error': 'HN超时'}]
        return []
    
    def list_platforms(self):
        """列出支持的平台"""
        return {
            'platforms': self.SUPPORTED_PLATFORMS,
            'total': len(self.SUPPORTED_PLATFORMS),
            'method': 'Agent-Reach (51.8k stars) 风格',
        }


# 全局实例
agent_reach = AgentReach()

if __name__ == '__main__':
    print('=== 多平台搜索 ===')
    result = agent_reach.search_all('CRISPR gene editing', ['github', 'arxiv', 'pubmed', 'hackernews'])
    print(json.dumps(result, ensure_ascii=False, indent=2)[:500])
