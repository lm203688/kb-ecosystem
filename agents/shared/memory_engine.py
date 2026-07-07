"""
Agent记忆推理引擎——借鉴M-Flow
不是搜索得更准，而是想得更对
用Cone Graph(锥形图谱)分层结构组织记忆
"""

import json, os, time, hashlib
from typing import Dict, List, Optional

class MemoryEngine:
    """Agent记忆引擎——推理而非搜索"""
    
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.memory_dir = os.path.join(os.path.dirname(__file__), '..', agent_name, 'db', 'memory')
        os.makedirs(self.memory_dir, exist_ok=True)
        self.memories = self._load()
    
    def _load(self) -> List[dict]:
        """加载记忆"""
        mem_file = os.path.join(self.memory_dir, 'memories.json')
        if os.path.exists(mem_file):
            return json.load(open(mem_file))
        return []
    
    def _save(self):
        """保存记忆"""
        mem_file = os.path.join(self.memory_dir, 'memories.json')
        json.dump(self.memories, open(mem_file, 'w'), ensure_ascii=False, indent=2)
    
    def remember(self, event: str, context: dict = None, insight: str = '') -> dict:
        """记住一个事件+推理insight"""
        memory = {
            'id': hashlib.md5(f'{event}{time.time()}'.encode()).hexdigest()[:12],
            'event': event,
            'context': context or {},
            'insight': insight,  # 推理结论——M-Flow核心
            'timestamp': time.time(),
            'layer': self._classify_layer(event, insight),
            'connections': self._find_connections(event, insight),
        }
        self.memories.append(memory)
        self._save()
        return memory
    
    def recall(self, query: str, top_k: int = 5) -> List[dict]:
        """回忆——不是搜索而是推理关联"""
        # 1. 简单关键词匹配
        scored = []
        for mem in self.memories:
            score = 0
            query_lower = query.lower()
            if query_lower in mem['event'].lower():
                score += 3
            if mem.get('insight') and query_lower in mem['insight'].lower():
                score += 5  # insight匹配权重更高——M-Flow理念
            # 上下文匹配
            for v in mem.get('context', {}).values():
                if isinstance(v, str) and query_lower in v.lower():
                    score += 2
            # 连接匹配——通过关联记忆推理
            for conn_id in mem.get('connections', []):
                conn_mem = next((m for m in self.memories if m['id'] == conn_id), None)
                if conn_mem and query_lower in conn_mem['event'].lower():
                    score += 1  # 关联记忆加分
            if score > 0:
                scored.append((score, mem))
        
        scored.sort(key=lambda x: -x[0])
        return [m for _, m in scored[:top_k]]
    
    def reason(self, query: str) -> dict:
        """推理——M-Flow核心：想而非搜"""
        related = self.recall(query, top_k=3)
        
        if not related:
            return {
                'answer': '无相关记忆',
                'confidence': 0,
                'method': 'M-Flow推理（无记忆）'
            }
        
        # 综合推理
        insights = [m.get('insight', '') for m in related if m.get('insight')]
        events = [m.get('event', '') for m in related]
        
        # 推理链：事件→insight→结论
        reasoning_chain = []
        for m in related:
            reasoning_chain.append(f"事件: {m['event']} → 推理: {m.get('insight', '无')}")
        
        return {
            'answer': insights[0] if insights else events[0],
            'confidence': min(1.0, len(related) / 5),
            'related_memories': len(related),
            'reasoning_chain': reasoning_chain,
            'method': 'M-Flow推理（想而非搜）',
        }
    
    def _classify_layer(self, event: str, insight: str) -> str:
        """锥形图谱分层——M-Flow的Cone Graph"""
        if insight and len(insight) > 50:
            return 'deep'  # 深层推理
        elif insight:
            return 'middle'  # 中层关联
        else:
            return 'surface'  # 表层事件
    
    def _find_connections(self, event: str, insight: str) -> List[str]:
        """找关联记忆——M-Flow的图拓扑"""
        connections = []
        for mem in self.memories[-20:]:  # 最近20条记忆
            if mem.get('insight') and insight:
                # 简单关键词重叠
                words1 = set(insight.split())
                words2 = set(mem['insight'].split())
                if len(words1 & words2) > 2:
                    connections.append(mem['id'])
        return connections
    
    def stats(self) -> dict:
        """记忆统计"""
        layers = {'surface': 0, 'middle': 0, 'deep': 0}
        for m in self.memories:
            layers[m.get('layer', 'surface')] += 1
        return {
            'total': len(self.memories),
            'layers': layers,
            'with_insight': sum(1 for m in self.memories if m.get('insight')),
            'connections': sum(len(m.get('connections', [])) for m in self.memories),
        }
