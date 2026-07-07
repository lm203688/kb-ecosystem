# AIShield Agent原生分发 — 提交清单

## ✅ 已完成（代码层面）

| 产出 | 状态 | 位置 |
|------|------|------|
| npm包 aishield-mcp | ✅ 代码就绪 | distrib/npm-package/ |
| npm包 aishield-guardrail | ✅ 代码就绪 | distrib/guardrail-mcp/ |
| PyPI包 aishield SDK | ✅ 代码就绪 | distrib/pypi-package/ |
| Claude Skill | ✅ 代码就绪 | distrib/claude-skill/ |
| GitHub Action v2 | ✅ 代码就绪 | distrib/public-repo/github-action/ |
| MCP远程模式 | ✅ 已集成 | mcp/server.py |
| 批量扫描脚本 | ✅ 代码就绪 | distrib/batch-scanner/ |
| 公开repo完整结构 | ✅ 代码就绪 | distrib/public-repo/ |
| OpenAPI文档 | ✅ 代码就绪 | distrib/public-repo/docs/openapi.yaml |

## ⏳ 需要账号/凭证才能完成的提交

### npm发布 (2个包)
```bash
# 1. 登录npm (需要npm账号)
npm login

# 2. 发布 aishield-mcp
cd distrib/npm-package
npm publish --access public

# 3. 发布 aishield-guardrail
cd ../guardrail-mcp
npm publish --access public
```

### PyPI发布
```bash
# 1. 安装构建工具
pip install build twine

# 2. 构建
cd distrib/pypi-package
python -m build

# 3. 发布 (需要PyPI账号)
twine upload dist/*
```

### GitHub公开Repo创建
```bash
# 需要GitHub PAT (已有: [从环境变量GITHUB_TOKEN获取])
# 创建 repo: aishield-ai/aishield
# 推送 distrib/public-repo/ 内容
```

### 7个MCP Registry提交

#### 1. MCP官方Registry
- URL: https://registry.modelcontextprotocol.io
- 方式: 提交server.json
- 前提: 公开GitHub repo + 可访问的MCP server

#### 2. Smithery
- URL: https://smithery.ai/new
- 方式: 提交GitHub repo URL
- 前提: 公开repo + smithery.json

#### 3. Glama
- URL: https://glama.ai/mcp-servers
- 方式: 提交GitHub repo
- 前提: 公开repo

#### 4. mcp.so
- URL: https://mcp.so
- 方式: GitHub issue提交
- 前提: 公开repo

#### 5. MCPMarket
- URL: https://mcpmarket.com/submit
- 方式: 表单提交
- 前提: 公开repo

#### 6. PulseMCP
- URL: https://pulsemcp.com
- 方式: 自动爬取GitHub
- 前提: repo有mcp关键词

#### 7. ToolPlex
- URL: https://toolplex.dev
- 方式: 注册提交
- 前提: 公开repo

### GitHub Action Marketplace
- URL: https://github.com/marketplace/actions
- 方式: 在公开repo的action.yml页面点击"Publish to Marketplace"
- 前提: 公开repo + action.yml

### Claude Skill Registry
- URL: 待定（Claude Code插件生态）
- 方式: 提交plugin.json
- 前提: 公开repo

## 📋 执行顺序

1. **创建GitHub公开repo** → 推送代码
2. **发布npm包** (aishield-mcp + aishield-guardrail)
3. **发布PyPI包** (aishield)
4. **提交7个Registry**
5. **GitHub Action上架Marketplace**
6. **批量扫描100个工具** (积累数据)
7. **Agent调用量监控** (核心指标)
