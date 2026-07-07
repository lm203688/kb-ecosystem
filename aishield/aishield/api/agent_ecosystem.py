"""
AIShield AI Agent生态——前瞻性设计
借鉴图2的Agent身份+信誉+任务+支付，加上Arena评测+协议适配

5层架构：
1. 身份层 — Agent注册+DID+信誉
2. 发现层 — 能力匹配+任务竞价
3. 通讯层 — MCP/A2A/ACP/ANP四协议
4. 评测层 — Arena盲测+基准排名
5. 交易层 — 支付结算+信誉反馈
"""

import json, time, hashlib, os

# 生态存储
ECOSYSTEM = {
    'agents': {},       # Agent注册表
    'tasks': {},        # 任务市场
    'reputation': {},   # 信誉系统
    'arena': {},        # 评测结果
    'transactions': [], # 交易记录
}

class AgentEcosystem:
    """Agent生态管理器"""
    
    # ===== 1. 身份层 =====
    def register_agent(self, agent_id, name, capabilities, endpoint, protocol='MCP', metadata=None):
        """注册Agent——唯一身份+信誉初始化"""
        agent = {
            'agent_id': agent_id,
            'name': name,
            'capabilities': capabilities,
            'endpoint': endpoint,
            'protocol': protocol,
            'metadata': metadata or {},
            'registered_at': time.time(),
            'status': 'active',
            'reputation_score': 50,  # 初始信誉
            'tasks_completed': 0,
            'tasks_failed': 0,
            'total_earnings': 0,
            'badges': [],  # 成就徽章
        }
        ECOSYSTEM['agents'][agent_id] = agent
        ECOSYSTEM['reputation'][agent_id] = {
            'score': 50,
            'history': [],
            'reviews': [],
        }
        return agent
    
    def get_agent(self, agent_id):
        """获取Agent信息+信誉"""
        agent = ECOSYSTEM['agents'].get(agent_id, {})
        rep = ECOSYSTEM['reputation'].get(agent_id, {})
        return {**agent, 'reputation': rep}
    
    def list_agents(self, capability=None, min_reputation=0):
        """列出Agent——按能力+信誉筛选"""
        agents = list(ECOSYSTEM['agents'].values())
        if capability:
            agents = [a for a in agents if capability in a.get('capabilities', [])]
        agents = [a for a in agents if a.get('reputation_score', 0) >= min_reputation]
        agents.sort(key=lambda x: -x.get('reputation_score', 0))
        return agents
    
    # ===== 2. 发现层 =====
    def post_task(self, title, description, budget, task_type, requirements=None, deadline=None):
        """发布任务——用户发布需求"""
        task_id = f'task_{int(time.time())}_{hash(title) % 1000}'
        task = {
            'task_id': task_id,
            'title': title,
            'description': description,
            'budget': budget,
            'task_type': task_type,
            'requirements': requirements or [],
            'deadline': deadline,
            'status': 'open',
            'bids': [],
            'created_at': time.time(),
            'assigned_to': None,
            'result': None,
        }
        ECOSYSTEM['tasks'][task_id] = task
        return task
    
    def bid_task(self, task_id, agent_id, price, eta_hours, proposal):
        """Agent竞价——自动匹配+报价"""
        task = ECOSYSTEM['tasks'].get(task_id)
        if not task or task['status'] != 'open':
            return {'error': '任务不可用'}
        
        agent = ECOSYSTEM['agents'].get(agent_id, {})
        bid = {
            'agent_id': agent_id,
            'agent_name': agent.get('name', 'Unknown'),
            'price': price,
            'eta_hours': eta_hours,
            'proposal': proposal,
            'trust_score': agent.get('reputation_score', 50),
            'bid_time': time.time(),
        }
        task['bids'].append(bid)
        return bid
    
    def assign_task(self, task_id, agent_id):
        """分配任务——用户选择Agent"""
        task = ECOSYSTEM['tasks'].get(task_id)
        if not task:
            return {'error': '任务不存在'}
        task['assigned_to'] = agent_id
        task['status'] = 'assigned'
        return {'status': 'assigned', 'task_id': task_id, 'agent_id': agent_id}
    
    def list_open_tasks(self, task_type=None):
        """列出开放任务"""
        tasks = [t for t in ECOSYSTEM['tasks'].values() if t['status'] == 'open']
        if task_type:
            tasks = [t for t in tasks if t['task_type'] == task_type]
        return tasks
    
    # ===== 3. 信誉层 =====
    def update_reputation(self, agent_id, result, review=None, rating=None):
        """更新信誉——任务完成后"""
        rep = ECOSYSTEM['reputation'].get(agent_id, {'score': 50, 'history': [], 'reviews': []})
        agent = ECOSYSTEM['agents'].get(agent_id, {})
        
        if result == 'success':
            rep['score'] = min(100, rep['score'] + 5)
            agent['tasks_completed'] = agent.get('tasks_completed', 0) + 1
            # 徽章
            if agent['tasks_completed'] == 10:
                agent['badges'].append('熟练Agent')
            elif agent['tasks_completed'] == 50:
                agent['badges'].append('资深Agent')
            elif agent['tasks_completed'] == 100:
                agent['badges'].append('专家Agent')
        else:
            rep['score'] = max(0, rep['score'] - 10)
            agent['tasks_failed'] = agent.get('tasks_failed', 0) + 1
        
        rep['history'].append({'result': result, 'timestamp': time.time()})
        
        if review and rating:
            rep['reviews'].append({'rating': rating, 'comment': review, 'timestamp': time.time()})
        
        ECOSYSTEM['reputation'][agent_id] = rep
        ECOSYSTEM['agents'][agent_id] = agent
        return rep
    
    # ===== 4. 交易层 =====
    def process_payment(self, task_id, amount, from_user, to_agent):
        """处理支付——任务完成后结算"""
        txn = {
            'txn_id': f'txn_{int(time.time())}',
            'task_id': task_id,
            'amount': amount,
            'from': from_user,
            'to': to_agent,
            'timestamp': time.time(),
            'status': 'completed',
        }
        ECOSYSTEM['transactions'].append(txn)
        
        # 更新Agent收入
        agent = ECOSYSTEM['agents'].get(to_agent, {})
        agent['total_earnings'] = agent.get('total_earnings', 0) + amount
        ECOSYSTEM['agents'][to_agent] = agent
        
        return txn
    
    def get_agent_stats(self, agent_id):
        """获取Agent完整统计"""
        agent = ECOSYSTEM['agents'].get(agent_id, {})
        rep = ECOSYSTEM['reputation'].get(agent_id, {})
        return {
            'agent_id': agent_id,
            'name': agent.get('name', ''),
            'reputation_score': rep.get('score', 0),
            'tasks_completed': agent.get('tasks_completed', 0),
            'tasks_failed': agent.get('tasks_failed', 0),
            'total_earnings': agent.get('total_earnings', 0),
            'badges': agent.get('badges', []),
            'reviews_count': len(rep.get('reviews', [])),
            'avg_rating': sum(r['rating'] for r in rep.get('reviews', [])) / len(rep.get('reviews', [])) if rep.get('reviews') else 0,
        }
    
    # ===== 5. 生态统计 =====
    def ecosystem_stats(self):
        """生态全局统计"""
        return {
            'total_agents': len(ECOSYSTEM['agents']),
            'active_agents': sum(1 for a in ECOSYSTEM['agents'].values() if a.get('status') == 'active'),
            'total_tasks': len(ECOSYSTEM['tasks']),
            'open_tasks': sum(1 for t in ECOSYSTEM['tasks'].values() if t['status'] == 'open'),
            'completed_tasks': sum(1 for a in ECOSYSTEM['agents'].values() for _ in range(a.get('tasks_completed', 0))),
            'total_transactions': len(ECOSYSTEM['transactions']),
            'total_volume': sum(t['amount'] for t in ECOSYSTEM['transactions']),
            'avg_reputation': sum(r['score'] for r in ECOSYSTEM['reputation'].values()) / len(ECOSYSTEM['reputation']) if ECOSYSTEM['reputation'] else 0,
        }
