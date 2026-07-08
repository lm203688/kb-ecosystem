#!/usr/bin/env python3
"""
专业Agent团队协作能力——借鉴PMTSoul
给每支团队24x7在岗的AI能力
"""

import json, os, time

class AgentTeam:
    """AI Agent团队——组织知识/业务流程/权限/定计"""
    
    def __init__(self, team_name):
        self.team_name = team_name
        self.members = {}  # agent_id -> role
        self.knowledge_base = {}  # 组织知识
        self.workflows = {}  # 业务流程
        self.permissions = {}  # 权限树
        self.schedule = {}  # 定计
    
    def add_member(self, agent_id, role, capabilities):
        """添加团队成员"""
        self.members[agent_id] = {
            'role': role,
            'capabilities': capabilities,
            'status': 'active',
            'joined_at': time.time(),
        }
    
    def add_knowledge(self, key, content, category='general'):
        """添加组织知识"""
        if category not in self.knowledge_base:
            self.knowledge_base[category] = {}
        self.knowledge_base[category][key] = {
            'content': content,
            'updated_at': time.time(),
        }
    
    def define_workflow(self, name, steps, trigger='manual'):
        """定义业务流程"""
        self.workflows[name] = {
            'steps': steps,
            'trigger': trigger,
            'status': 'active',
        }
    
    def set_permission(self, agent_id, resource, level='read'):
        """设置权限"""
        if agent_id not in self.permissions:
            self.permissions[agent_id] = {}
        self.permissions[agent_id][resource] = level
    
    def schedule_task(self, task_name, cron, agent_id, action):
        """定计任务"""
        self.schedule[task_name] = {
            'cron': cron,
            'agent_id': agent_id,
            'action': action,
            'last_run': None,
        }
    
    def get_team_status(self):
        """团队状态"""
        return {
            'team_name': self.team_name,
            'members': len(self.members),
            'active_members': sum(1 for m in self.members.values() if m['status'] == 'active'),
            'knowledge_items': sum(len(v) for v in self.knowledge_base.values()),
            'workflows': len(self.workflows),
            'scheduled_tasks': len(self.schedule),
            'capabilities': list(set(c for m in self.members.values() for c in m['capabilities'])),
        }

# 预定义团队
TEAMS = {
    'engineering': AgentTeam('工程团队'),
    'security': AgentTeam('安全团队'),
    'research': AgentTeam('研究团队'),
    'operations': AgentTeam('运营团队'),
}

# 初始化团队成员
TEAMS['engineering'].add_member('builder', '工程师', ['code_review', 'deploy', 'debug'])
TEAMS['engineering'].add_member('guardian', '安全审计', ['audit', 'scan', 'compliance'])

TEAMS['security'].add_member('guardian', '安全官', ['vuln_scan', 'skill_scan', 'prompt_check'])

TEAMS['research'].add_member('researcher', '研究员', ['lit_review', 'experiment', 'analysis'])
TEAMS['research'].add_member('scout', '情报员', ['search', 'trending', 'collect'])

TEAMS['operations'].add_member('ops', '运营官', ['monitor', 'report', 'optimize'])
TEAMS['operations'].add_member('strategist', '战略家', ['plan', 'analyze', 'decide'])
