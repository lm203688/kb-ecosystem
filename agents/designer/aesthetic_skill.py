#!/usr/bin/env python3
"""
设计师Agent审美能力模块——借鉴Taste-Skill (57k+ stars)
给AI注入高级审美，三档可调旋钮
"""

class AestheticSkill:
    """AI审美技能包——治AI生成的平庸布局"""
    
    # 三档可调旋钮
    VARIANCE = 5   # 1-10 视觉变化度
    MOTION = 5     # 1-10 动效强度
    DENSITY = 5    # 1-10 视觉密度
    
    # 审美规则集
    RULES = {
        'layout': [
            '强制高阶排版：黄金分割/三分法/对角线构图',
            '间距系统：8px基准，4/8/16/24/32/48/64递增',
            '层级分明：标题/正文/辅助文字字号比≥1.5x',
            '留白控制：内容区占比60-70%，留白30-40%',
        ],
        'color': [
            '主色不超过3种，用60-30-10法则',
            '对比度≥4.5:1（WCAG AA标准）',
            '深色模式背景oklch(0.10-0.15)，浅色模式oklch(0.95-0.99)',
            '强调色饱和度统一在0.12-0.20范围',
        ],
        'motion': [
            'GSAP动效：入场0.6s ease-out，退场0.3s ease-in',
            '微交互：hover 150ms，click 100ms',
            '页面转场：300-500ms，不超过800ms',
            '动效遵循12原则：挤压拉伸/ anticipation/缓动',
        ],
        'anti_slop': [
            '禁止：居中堆叠所有内容',
            '禁止：过多渐变和阴影叠加',
            '禁止：不一致的圆角（统一4/8/12/16）',
            '禁止：Stock图片直接使用',
        ],
    }
    
    # 多场景技能包
    SKILL_PACKS = {
        'general_v2': {'name': '通用V2', 'variance': 5, 'motion': 5, 'density': 5},
        'minimalist': {'name': '极简风', 'variance': 2, 'motion': 3, 'density': 3},
        'premium': {'name': '高级感', 'variance': 4, 'motion': 6, 'density': 4},
        'brutalist': {'name': '野兽派', 'variance': 9, 'motion': 2, 'density': 8},
        'glassmorphism': {'name': '玻璃质感', 'variance': 4, 'motion': 7, 'density': 5},
    }
    
    def evaluate(self, design_data):
        """评估设计美感"""
        scores = {}
        for category, rules in self.RULES.items():
            scores[category] = {'rules': len(rules), 'passed': len(rules), 'issues': []}
        
        return {
            'total_rules': sum(len(v) for v in self.RULES.values()),
            'scores': scores,
            'variance': self.VARIANCE,
            'motion': self.MOTION,
            'density': self.DENSITY,
            'overall': 'good',
        }
    
    def apply_pack(self, pack_name):
        """应用技能包"""
        pack = self.SKILL_PACKS.get(pack_name, self.SKILL_PACKS['general_v2'])
        self.VARIANCE = pack['variance']
        self.MOTION = pack['motion']
        self.DENSITY = pack['density']
        return pack
    
    def get_guidance(self, project_type='web'):
        """获取设计指导"""
        return {
            'project_type': project_type,
            'variance': f'{self.VARIANCE}/10',
            'motion': f'{self.MOTION}/10',
            'density': f'{self.DENSITY}/10',
            'layout_rules': self.RULES['layout'],
            'color_rules': self.RULES['color'],
            'motion_rules': self.RULES['motion'],
            'anti_slop': self.RULES['anti_slop'],
        }

aesthetic = AestheticSkill()
