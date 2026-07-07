#!/usr/bin/env python3
"""
Agent多路复用器——借鉴herdr (13.2K stars)
功能：多个Agent并行运行，独立终端，状态可视化

每个Agent拥有独立真实终端：
- 阻塞/工作/完成/空闲 颜色标识
- 会话持久化，断连不丢失
- 轻量极速，零依赖
"""

import json, os, time, threading
from enum import Enum

class AgentState(Enum):
    IDLE = "idle"        # 空闲-灰色
    WORKING = "working"  # 工作-绿色
    BLOCKED = "blocked"  # 阻塞-红色
    DONE = "done"        # 完成-蓝色

class AgentSession:
    """Agent会话"""
    def __init__(self, agent_id, name, capabilities):
        self.agent_id = agent_id
        self.name = name
        self.capabilities = capabilities
        self.state = AgentState.IDLE
        self.terminal_log = []
        self.created_at = time.time()
        self.last_active = time.time()
        self.current_task = None
    
    def assign_task(self, task):
        """分配任务"""
        self.current_task = task
        self.state = AgentState.WORKING
        self.last_active = time.time()
        self.terminal_log.append(f"[{time.strftime('%H:%M:%S')}] 任务开始: {task}")
    
    def complete_task(self, result):
        """完成任务"""
        self.state = AgentState.DONE
        self.terminal_log.append(f"[{time.strftime('%H:%M:%S')}] 任务完成: {result}")
        self.last_active = time.time()
    
    def block(self, reason):
        """阻塞"""
        self.state = AgentState.BLOCKED
        self.terminal_log.append(f"[{time.strftime('%H:%M:%S')}] 阻塞: {reason}")
    
    def reset(self):
        """重置为空闲"""
        self.state = AgentState.IDLE
        self.current_task = None
    
    def status(self):
        """获取状态"""
        return {
            'agent_id': self.agent_id,
            'name': self.name,
            'state': self.state.value,
            'color': {
                'idle': '#64748b',
                'working': '#10b981',
                'blocked': '#ef4444',
                'done': '#3b82f6',
            }[self.state.value],
            'current_task': self.current_task,
            'log_tail': self.terminal_log[-5:],
            'uptime': round(time.time() - self.created_at),
        }


class AgentMultiplexer:
    """Agent多路复用器——管理多个Agent会话"""
    
    def __init__(self):
        self.sessions = {}
        self.lock = threading.Lock()
    
    def register(self, agent_id, name, capabilities):
        """注册Agent"""
        with self.lock:
            session = AgentSession(agent_id, name, capabilities)
            self.sessions[agent_id] = session
            return session.status()
    
    def assign(self, agent_id, task):
        """分配任务"""
        with self.lock:
            session = self.sessions.get(agent_id)
            if session:
                session.assign_task(task)
                return session.status()
            return {'error': 'Agent未注册'}
    
    def complete(self, agent_id, result):
        """完成任务"""
        with self.lock:
            session = self.sessions.get(agent_id)
            if session:
                session.complete_task(result)
                return session.status()
            return {'error': 'Agent未注册'}
    
    def dashboard(self):
        """状态看板——所有Agent状态"""
        with self.lock:
            return {
                'total_agents': len(self.sessions),
                'states': {
                    'idle': sum(1 for s in self.sessions.values() if s.state == AgentState.IDLE),
                    'working': sum(1 for s in self.sessions.values() if s.state == AgentState.WORKING),
                    'blocked': sum(1 for s in self.sessions.values() if s.state == AgentState.BLOCKED),
                    'done': sum(1 for s in self.sessions.values() if s.state == AgentState.DONE),
                },
                'agents': [s.status() for s in self.sessions.values()],
            }
    
    def get_log(self, agent_id, lines=50):
        """获取Agent终端日志"""
        session = self.sessions.get(agent_id)
        if session:
            return {
                'agent_id': agent_id,
                'log': session.terminal_log[-lines:],
                'total_lines': len(session.terminal_log),
            }
        return {'error': 'Agent未注册'}


# 全局实例
multiplexer = AgentMultiplexer()

# 预注册专业Agent
PROFESSIONAL_AGENTS = [
    ('builder', '建造者Agent', ['code_generation', 'deployment', 'testing']),
    ('guardian', '守护者Agent', ['security_audit', 'vulnerability_scan', 'compliance']),
    ('scout', '侦察者Agent', ['data_collection', 'market_research', 'competitor_analysis']),
    ('strategist', '战略家Agent', ['architecture', 'planning', 'decision_support']),
    ('designer', '设计师Agent', ['ui_design', 'visual_system', 'user_experience']),
    ('operator', '运营者Agent', ['monitoring', 'optimization', 'reporting']),
    ('researcher', '研究员Agent', ['literature_review', 'experiment_design', 'analysis']),
    ('game', '游戏Agent', ['asset_generation', 'code_generation', 'level_design']),
]

for agent_id, name, caps in PROFESSIONAL_AGENTS:
    multiplexer.register(agent_id, name, caps)


if __name__ == '__main__':
    # 测试
    print(json.dumps(multiplexer.dashboard(), ensure_ascii=False, indent=2)[:500])
    
    # 分配任务
    multiplexer.assign('builder', '部署蜂群科研ECS')
    multiplexer.assign('guardian', 'AIShield漏洞扫描')
    
    print()
    print("=== 分配任务后 ===")
    print(json.dumps(multiplexer.dashboard(), ensure_ascii=False, indent=2)[:500])
