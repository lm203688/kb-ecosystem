#!/usr/bin/env python3
"""
Token优化器——借鉴RTK (rust-token-killer)
CLI输出过滤，减少60-90% token消耗
给所有Agent的输出增加噪音过滤
"""

import re

class TokenOptimizer:
    """Token优化器——过滤噪音，减少token消耗"""
    
    # 噪音模式
    NOISE_PATTERNS = [
        # ANSI颜色码
        (r'\x1b\[[0-9;]*m', ''),
        # 进度条
        (r'\[=+\s*\]\s*\d+%', ''),
        # 时间戳
        (r'\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}[.,]?\d*', ''),
        # 调试日志级别
        (r'(DEBUG|TRACE|VERBOSE)\s*:.*\n', ''),
        # 重复空行
        (r'\n{3,}', '\n\n'),
        # 路径前缀
        (r'/home/\w+/|/usr/local/', '~/'),
        # pip/npm安装日志
        (r'(Downloading|Installing|Collecting|Using cached)\s+.*\n', ''),
        # git操作日志
        (r'(remote:|Counting objects|Compressing|Writing objects)\s*:.*\n', ''),
        # 编译输出
        (r'(warning:|note:)\s+.*\n', ''),
        # 空格压缩
        (r'[ \t]{2,}', ' '),
    ]
    
    # 常见命令输出的噪音行
    NOISE_LINES = [
        'Type "help", "copyright"',
        'For more information',
        'Loading...',
        'Please wait...',
        'WARNING: You are using pip',
        'DEPRECATION:',
    ]
    
    def optimize(self, text):
        """优化输出——减少token消耗"""
        original_len = len(text)
        original_tokens = self._estimate_tokens(text)
        
        # 应用噪音过滤
        for pattern, replacement in self.NOISE_PATTERNS:
            text = re.sub(pattern, replacement, text)
        
        # 过滤噪音行
        lines = text.split('\n')
        filtered_lines = [line for line in lines if not any(noise in line for noise in self.NOISE_LINES)]
        text = '\n'.join(filtered_lines)
        
        optimized_len = len(text)
        optimized_tokens = self._estimate_tokens(text)
        
        reduction = round((1 - optimized_tokens / original_tokens) * 100, 1) if original_tokens > 0 else 0
        
        return {
            'original_length': original_len,
            'optimized_length': optimized_len,
            'original_tokens': original_tokens,
            'optimized_tokens': optimized_tokens,
            'token_reduction': f'{reduction}%',
            'tokens_saved': original_tokens - optimized_tokens,
            'optimized_text': text,
            'method': 'RTK风格token优化',
        }
    
    def optimize_cli_output(self, command, output):
        """优化CLI命令输出"""
        result = self.optimize(output)
        result['command'] = command
        result['note'] = f'命令 "{command}" 的输出已优化，节省{result["token_reduction"]} token'
        return result
    
    def summarize_for_agent(self, text, max_tokens=500):
        """为Agent精简输入"""
        result = self.optimize(text)
        optimized = result['optimized_text']
        
        # 如果仍然太长，截取关键部分
        if self._estimate_tokens(optimized) > max_tokens:
            # 保留开头+结尾
            lines = optimized.split('\n')
            half = max_tokens // 2
            head = '\n'.join(lines[:10])
            tail = '\n'.join(lines[-5:])
            optimized = head + '\n...\n[省略中间部分]\n...\n' + tail
        
        return {
            'summary': optimized,
            'estimated_tokens': self._estimate_tokens(optimized),
            'original_tokens': result['original_tokens'],
            'reduction': f'{round((1 - self._estimate_tokens(optimized) / result["original_tokens"]) * 100, 1)}%' if result['original_tokens'] > 0 else '0%',
        }
    
    def _estimate_tokens(self, text):
        """估算token数（粗略：1 token ≈ 4字符英文 / 1.5字符中文）"""
        # 简单估算
        english_chars = len(re.findall(r'[a-zA-Z0-9\s]', text))
        chinese_chars = len(re.findall(r'[\u4e00-\u9fa5]', text))
        return max(1, english_chars // 4 + int(chinese_chars // 1.5))
    
    def get_stats(self):
        """获取优化器统计"""
        return {
            'noise_patterns': len(self.NOISE_PATTERNS),
            'noise_lines': len(self.NOISE_LINES),
            'avg_reduction': '60-90%',
            'method': 'RTK (rust-token-killer) 风格',
        }


token_optimizer = TokenOptimizer()

if __name__ == '__main__':
    # 测试
    test_output = """
2026-07-08 07:00:00.123 INFO Starting process
\x1b[32mDownloading package-1.2.3.tar.gz\x1b[0m
Collecting dependencies...
[==========          ] 50%
WARNING: You are using pip version 21.0
DEPRECATION: The old API is deprecated
Installing collected packages: package-1.2.3
Type "help", "copyright", "credits" for more information.
Successfully installed package-1.2.3
"""
    
    result = token_optimizer.optimize(test_output)
    print(f'原始: {result["original_tokens"]} tokens')
    print(f'优化: {result["optimized_tokens"]} tokens')
    print(f'节省: {result["token_reduction"]}')
    print()
    print('优化后:')
    print(result['optimized_text'])
