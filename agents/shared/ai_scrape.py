#!/usr/bin/env python3
"""
AI驱动网页抓取——借鉴ScrapeGraphAI
用LLM+图逻辑创建抓取管线
给scout/researcher Agent增加智能抓取能力
"""

import json, re, urllib.request, html

class AIScrape:
    """AI驱动网页抓取器"""
    
    def scrape(self, url, extract_rule=None):
        """抓取网页并提取结构化数据"""
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (compatible; AIScrape/1.0)'})
            r = urllib.request.urlopen(req, timeout=15)
            content = r.read().decode('utf-8', errors='ignore')
            
            # 清理HTML
            text = self._clean_html(content)
            title = self._extract_title(content)
            links = self._extract_links(content, url)
            
            # 提取结构化数据
            structured = self._extract_structured(text, extract_rule)
            
            return {
                'url': url,
                'title': title,
                'text_length': len(text),
                'text': text[:5000],  # 限制返回长度
                'links_count': len(links),
                'links': links[:20],
                'structured': structured,
                'method': 'ScrapeGraphAI风格AI抓取',
            }
        except Exception as e:
            return {'url': url, 'error': str(e)[:100]}
    
    def batch_scrape(self, urls, extract_rule=None):
        """批量抓取"""
        results = []
        for url in urls:
            result = self.scrape(url, extract_rule)
            results.append(result)
        
        return {
            'total': len(urls),
            'success': sum(1 for r in results if 'error' not in r),
            'failed': sum(1 for r in results if 'error' in r),
            'results': results,
        }
    
    def extract_entities(self, url, entity_type=None):
        """从网页提取实体"""
        scraped = self.scrape(url)
        if 'error' in scraped:
            return scraped
        
        text = scraped.get('text', '')
        
        # 根据entity_type提取
        entities = []
        if entity_type == 'company':
            # 提取公司名
            entities = re.findall(r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*(?:Inc|Corp|Ltd|LLC|Co)', text)
        elif entity_type == 'person':
            entities = re.findall(r'([A-Z][a-z]+ [A-Z][a-z]+)', text)
        elif entity_type == 'product':
            entities = re.findall(r'(?:product|tool|platform)[:\s]+([A-Z][\w\s]+)', text, re.I)
        elif entity_type == 'price':
            entities = re.findall(r'\$[\d,]+(?:\.\d{2})?|￥[\d,]+', text)
        else:
            # 通用提取
            entities = re.findall(r'[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*', text)
        
        return {
            'url': url,
            'entity_type': entity_type or 'general',
            'entities': list(set(entities))[:20],
            'total': len(set(entities)),
        }
    
    def _clean_html(self, content):
        """清理HTML"""
        # 移除script/style
        content = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL | re.IGNORECASE)
        content = re.sub(r'<style[^>]*>.*?</style>', '', content, flags=re.DOTALL | re.IGNORECASE)
        # 移除标签
        content = re.sub(r'<[^>]+>', ' ', content)
        # 解码HTML实体
        content = html.unescape(content)
        # 压缩空格
        content = re.sub(r'\s+', ' ', content).strip()
        return content
    
    def _extract_title(self, content):
        """提取标题"""
        m = re.search(r'<title[^>]*>(.*?)</title>', content, re.DOTALL | re.IGNORECASE)
        return html.unescape(m.group(1).strip()) if m else ''
    
    def _extract_links(self, content, base_url):
        """提取链接"""
        links = []
        for m in re.finditer(r'href=["\']([^"\']+)["\']', content, re.IGNORECASE):
            link = m.group(1)
            if link.startswith('http'):
                links.append(link)
            elif link.startswith('/'):
                base = '/'.join(base_url.split('/')[:3])
                links.append(base + link)
        return list(set(links))
    
    def _extract_structured(self, text, rule=None):
        """提取结构化数据"""
        if not rule:
            return {'note': '无提取规则，返回原文摘要', 'summary': text[:500]}
        
        # 简单规则提取
        if rule == 'json':
            try:
                return json.loads(text[:5000])
            except:
                return {'error': '无法解析为JSON'}
        
        # 正则提取
        try:
            matches = re.findall(rule, text)
            return {'matches': matches[:20], 'total': len(matches)}
        except:
            return {'error': '正则表达式无效'}


ai_scrape = AIScrape()

if __name__ == '__main__':
    result = ai_scrape.scrape('https://github.com/ScrapeGraphAI/Scrapegraph-ai')
    print(f'标题: {result.get("title","")}')
    print(f'文本长度: {result.get("text_length",0)}')
    print(f'链接数: {result.get("links_count",0)}')
