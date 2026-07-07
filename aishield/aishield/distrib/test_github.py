import os
#!/usr/bin/env python3
"""Test GitHub API access"""
import urllib.request
import json
import ssl

PAT = "ghp_yAIvslr9l6lW5ruT7m2WqGH0GSCfUp2bDtVo"

def test_github():
    ctx = ssl.create_default_context()
    req = urllib.request.Request('https://api.github.com/user', headers={
        'Authorization': f'token {PAT}',
        'User-Agent': 'AIShield'
    })
    try:
        with urllib.request.urlopen(req, timeout=10, context=ctx) as r:
            d = json.loads(r.read())
            print(f"GITHUB OK: user={d.get('login')}, name={d.get('name')}")
            return d
    except Exception as e:
        print(f"GITHUB ERR: {type(e).__name__}: {e}")
        return None

def create_repo():
    """Create aishield-ai/aishield public repo"""
    ctx = ssl.create_default_context()
    # First check if org exists
    req = urllib.request.Request('https://api.github.com/orgs/aishield-ai', headers={
        'Authorization': f'token {PAT}',
        'User-Agent': 'AIShield'
    })
    try:
        with urllib.request.urlopen(req, timeout=10, context=ctx) as r:
            d = json.loads(r.read())
            print(f"ORG OK: {d.get('login')}")
    except Exception as e:
        print(f"ORG check: {e}")
        # Try create under personal account
        pass
    
    # Create repo under personal account
    data = json.dumps({
        "name": "aishield",
        "description": "Agent-native AI tool security scanner. Scan MCP/Skill/GPT/Prompt for security risks.",
        "private": False,
        "has_issues": True,
        "has_projects": True,
        "has_wiki": True,
        "license_template": "mit"
    }).encode()
    
    req = urllib.request.Request('https://api.github.com/user/repos', data=data, headers={
        'Authorization': f'token {PAT}',
        'User-Agent': 'AIShield',
        'Content-Type': 'application/json'
    }, method='POST')
    
    try:
        with urllib.request.urlopen(req, timeout=10, context=ctx) as r:
            d = json.loads(r.read())
            print(f"REPO CREATED: {d.get('full_name')}")
            print(f"URL: {d.get('html_url')}")
            return d
    except Exception as e:
        print(f"REPO CREATE ERR: {e}")
        return None

if __name__ == '__main__':
    user = test_github()
    if user:
        create_repo()
