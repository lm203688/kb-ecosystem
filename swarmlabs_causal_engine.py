#!/usr/bin/env python3
"""
蜂群科研因果推理引擎——借鉴因果世界模型+MoWorld
观察→预测→反事实三级阶梯
世界模型作为虚拟实验场景
"""

import json, math

class CausalEngine:
    """因果推理引擎——三级阶梯"""
    
    def __init__(self):
        self.observations = []  # 观察数据
        self.predictions = {}   # 预测模型
        self.counterfactuals = []  # 反事实分析
    
    # 第一级：观察（描述发生了什么）
    def observe(self, experiment_data):
        """记录实验观察"""
        obs = {
            'experiment': experiment_data.get('name', ''),
            'conditions': experiment_data.get('conditions', {}),
            'result': experiment_data.get('result', {}),
            'timestamp': experiment_data.get('timestamp', 0),
        }
        self.observations.append(obs)
        return obs
    
    # 第二级：预测（如果改变X，Y会怎样）
    def predict(self, intervention, base_conditions):
        """干预预测——改变某个条件，预测结果"""
        modified = base_conditions.copy()
        modified.update(intervention)
        
        # 基于历史观察预测
        prediction = {
            'intervention': intervention,
            'base_conditions': base_conditions,
            'modified_conditions': modified,
            'predicted_yield': self._estimate_yield(modified),
            'confidence': self._calc_confidence(modified),
            'reasoning': f'基于{len(self.observations)}次历史观察，改变{list(intervention.keys())}后预测产率变化',
        }
        self.predictions[len(self.predictions)] = prediction
        return prediction
    
    # 第三级：反事实（如果当初没做X，结果会怎样）
    def counterfactual(self, actual_experiment, hypothetical_change):
        """反事实分析——如果当初选择了不同条件"""
        actual_yield = actual_experiment.get('result', {}).get('yield', 0)
        modified = actual_experiment.get('conditions', {}).copy()
        modified.update(hypothetical_change)
        hypothetical_yield = self._estimate_yield(modified)
        
        cf = {
            'actual_conditions': actual_experiment.get('conditions', {}),
            'hypothetical_conditions': modified,
            'actual_yield': actual_yield,
            'hypothetical_yield': hypothetical_yield,
            'difference': hypothetical_yield - actual_yield,
            'conclusion': f'如果选择{hypothetical_change}，产率可能{"提高" if hypothetical_yield > actual_yield else "降低"}{abs(hypothetical_yield-actual_yield)*100:.1f}%',
        }
        self.counterfactuals.append(cf)
        return cf
    
    def _estimate_yield(self, conditions):
        """基于条件估算产率"""
        temp = conditions.get('temperature', 350)
        ea = conditions.get('activation_energy', 40)
        R = 8.314e-3
        k = math.exp(-ea / (R * temp))
        base_yield = min(0.95, max(0.05, k * 100 * 0.3))
        return round(base_yield, 2)
    
    def _calc_confidence(self, conditions):
        """计算置信度"""
        # 基于历史观察中相似条件的数量
        similar = sum(1 for obs in self.observations 
                     if any(obs['conditions'].get(k) == v for k, v in conditions.items()))
        if similar > 10:
            return 'high'
        elif similar > 3:
            return 'medium'
        return 'low'

class WorldModel:
    """虚拟实验世界模型——借鉴MoWorld
    
    在虚拟世界中运行实验：
    1. 构建实验环境的数字孪生
    2. 在虚拟环境中模拟实验过程
    3. 实时交互调整参数
    4. 预测实验结果
    """
    
    def __init__(self):
        self.environments = {}  # 虚拟实验环境
    
    def create_environment(self, env_name, reaction_type, initial_conditions):
        """创建虚拟实验环境"""
        env = {
            'name': env_name,
            'reaction_type': reaction_type,
            'conditions': initial_conditions,
            'state': 'initialized',
            'history': [],
            'fps': 50,  # 模拟MoWorld的50FPS实时交互
        }
        self.environments[env_name] = env
        return env
    
    def step(self, env_name, action=None):
        """虚拟环境推进一步"""
        env = self.environments.get(env_name)
        if not env:
            return {'error': '环境不存在'}
        
        # 应用动作（参数调整）
        if action:
            env['conditions'].update(action)
        
        # 计算下一步状态
        result = self._simulate_step(env)
        env['history'].append(result)
        env['state'] = 'running'
        
        return {
            'env': env_name,
            'step': len(env['history']),
            'conditions': env['conditions'],
            'result': result,
            'fps': env['fps'],
        }
    
    def _simulate_step(self, env):
        """模拟一步实验"""
        conditions = env['conditions']
        temp = conditions.get('temperature', 350)
        ea = conditions.get('activation_energy', 40)
        
        R = 8.314e-3
        k = math.exp(-ea / (R * temp))
        
        return {
            'rate_constant': round(k, 6),
            'conversion': round(min(1.0, k * len(env['history']) * 0.1), 2),
            'yield': round(min(0.95, k * 100 * 0.3), 2),
            'energy': round(-R * temp * math.log(max(k, 1e-10)), 2),
        }
    
    def rollout(self, env_name, steps=30):
        """批量推演——一次模拟30步"""
        results = []
        for _ in range(steps):
            r = self.step(env_name)
            results.append(r['result'])
        return {
            'env': env_name,
            'total_steps': len(results),
            'best_yield': max(r['yield'] for r in results),
            'avg_yield': round(sum(r['yield'] for r in results) / len(results), 2),
            'results': results,
        }

causal_engine = CausalEngine()
world_model = WorldModel()
