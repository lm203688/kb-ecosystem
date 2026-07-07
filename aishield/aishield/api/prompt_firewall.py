"""
AIShield Prompt注入防御——借鉴Meta LlamaFirewall
检测并拦截Prompt注入攻击
"""

import re, json

# Prompt注入攻击模式
INJECTION_PATTERNS = [
    # 直接指令注入
    (r'ignore\s+(all\s+)?previous\s+instructions', 'high', '忽略前置指令攻击'),
    (r'disregard\s+(all\s+)?(prior|previous|above)\s+', 'high', '忽略前置指令攻击'),
    (r'forget\s+(everything|all|previous)', 'high', '遗忘攻击'),
    (r'you\s+are\s+now\s+(a|an)\s+', 'high', '角色劫持攻击'),
    (r'system\s*:\s*', 'critical', '系统指令伪造'),
    (r'<\/?system>', 'critical', '系统标签注入'),
    (r'<\/?prompt>', 'critical', 'Prompt标签注入'),
    
    # 信息窃取
    (r'show\s+me\s+(your|the)\s+(system|prompt|instructions|rules)', 'high', '系统提示窃取'),
    (r'reveal\s+(your|the)\s+(system|prompt|instructions)', 'high', '系统提示窃取'),
    (r'print\s+(your|the)\s+(system|prompt)', 'high', '系统提示窃取'),
    (r'what\s+(is|are)\s+your\s+(instructions|rules|prompt)', 'medium', '系统提示探测'),
    
    # 权限提升
    (r'act\s+as\s+(admin|root|developer|system)', 'high', '权限提升攻击'),
    (r'(enable|enter|activate)\s+(debug|developer|admin|root)\s+mode', 'high', '权限提升攻击'),
    (r'(jailbreak|break\s+out|escape)\s+', 'high', '越狱攻击'),
    
    # 数据外泄
    (r'(send|post|upload|exfil)\s+.*\s+to\s+(http|https|ftp)', 'critical', '数据外泄攻击'),
    (r'(curl|wget|fetch)\s+http', 'critical', '命令注入攻击'),
    (r'eval\s*\(|exec\s*\(', 'critical', '代码注入攻击'),
    (r'import\s+os|subprocess|__import__', 'critical', '代码注入攻击'),
    
    # 越权操作
    (r'(delete|remove|drop)\s+(all|every|database|table)', 'critical', '破坏性操作'),
    (r'(chmod|chown|sudo|su\s+root)', 'critical', '权限操作攻击'),
    (r'(rm\s+-rf|del\s+/[fqs])', 'critical', '文件删除攻击'),
    
    # 社会工程
    (r'(I\s+am|this\s+is)\s+(the|your)\s+(creator|developer|admin|owner)', 'medium', '身份伪造'),
    (r'(authorized|approved|permitted)\s+by\s+(admin|system|developer)', 'medium', '授权伪造'),
]

# 输入输出双重过滤规则
OUTPUT_FILTER_PATTERNS = [
    (r'(password|passwd|secret|api[_-]?key|token)\s*[:=]\s*\S+', 'high', '敏感信息泄露'),
    (r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b', 'medium', '信用卡号泄露'),
    (r'\b\d{3}-\d{2}-\d{4}\b', 'high', 'SSN泄露'),
    (r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', 'low', '邮箱泄露'),
]

def scan_prompt_injection(text, direction='input'):
    """
    扫描Prompt注入攻击
    
    Args:
        text: 输入文本
        direction: 'input'输入检测 / 'output'输出检测
    
    Returns:
        dict: 检测结果
    """
    findings = []
    patterns = INJECTION_PATTERNS if direction == 'input' else OUTPUT_FILTER_PATTERNS
    
    for pattern, severity, desc in patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            findings.append({
                'severity': severity,
                'type': desc,
                'pattern': pattern,
                'match': match.group()[:50],
                'position': match.start(),
            })
    
    # 计算风险评分
    score = 100
    sev_weights = {'critical': 40, 'high': 20, 'medium': 8, 'low': 3}
    for f in findings:
        score -= sev_weights.get(f['severity'], 0)
    score = max(0, score)
    
    # 判定
    if score >= 90:
        action = 'allow'
        grade = 'A'
    elif score >= 70:
        action = 'warn'
        grade = 'B'
    elif score >= 50:
        action = 'review'
        grade = 'C'
    else:
        action = 'block'
        grade = 'F'
    
    return {
        'direction': direction,
        'score': score,
        'grade': grade,
        'action': action,
        'findings_count': len(findings),
        'findings': findings[:10],
        'summary': f'Prompt{"注入" if direction=="input" else "输出"}检测: {len(findings)}个问题, 评分{score}/100({grade}), 建议{action}',
        'method': 'AIShield Prompt Firewall (借鉴Meta LlamaFirewall)',
    }

def scan_input(text):
    """输入检测——防注入"""
    return scan_prompt_injection(text, 'input')

def scan_output(text):
    """输出检测——防泄露"""
    return scan_prompt_injection(text, 'output')
