"""
AIShield Agent通讯协议适配层
支持4大Agent通讯协议，让AIShield成为Agent通讯枢纽：
1. A2A (Agent2Agent) — Google主导，Agent间直接通讯
2. MCP (Model Context Protocol) — Anthropic主导，Agent与工具通讯
3. ACP (Agent Communication Protocol) — Bee主导，Agent客户端协议
4. ANP (Agent Network Protocol) — 去中心化Agent网络

AIShield作为Agent Discovery Hub：
- Agent注册自己的能力 → AIShield索引
- 其他Agent通过AIShield发现需要的Agent
- AIShield提供协议适配，不同协议的Agent可以互操作
"""

import json, time, hashlib
from typing import Dict, List, Optional

# Agent注册表
AGENT_REGISTRY: Dict[str, dict] = {}

def register_agent(agent_id: str, name: str, capabilities: list, endpoint: str, protocol: str = "MCP") -> dict:
    """注册Agent到AIShield发现层"""
    agent = {
        "agent_id": agent_id,
        "name": name,
        "capabilities": capabilities,  # ["search","analyze","translate"]
        "endpoint": endpoint,
        "protocol": protocol,  # MCP/A2A/ACP/ANP
        "registered_at": time.time(),
        "status": "active",
        "trust_score": 50,  # 初始信任分
    }
    AGENT_REGISTRY[agent_id] = agent
    return {"status": "registered", "agent_id": agent_id}

def discover_agents(capability: str, protocol: str = None) -> list:
    """发现具有指定能力的Agent"""
    results = []
    for agent in AGENT_REGISTRY.values():
        if capability in agent["capabilities"]:
            if protocol and agent["protocol"] != protocol:
                continue
            results.append(agent)
    # 按信任分排序
    results.sort(key=lambda x: -x["trust_score"])
    return results[:10]

def protocol_adapter(source_protocol: str, target_protocol: str, message: dict) -> dict:
    """协议适配——不同协议的Agent互操作"""
    adapters = {
        ("MCP", "A2A"): adapt_mcp_to_a2a,
        ("A2A", "MCP"): adapt_a2a_to_mcp,
        ("MCP", "ACP"): adapt_mcp_to_acp,
        ("ACP", "MCP"): adapt_acp_to_mcp,
        ("A2A", "ACP"): adapt_a2a_to_acp,
        ("ACP", "A2A"): adapt_acp_to_a2a,
    }
    adapter = adapters.get((source_protocol, target_protocol))
    if adapter:
        return adapter(message)
    return message  # 无需转换

def adapt_mcp_to_a2a(msg: dict) -> dict:
    """MCP → A2A 转换"""
    return {
        "jsonrpc": "2.0",
        "method": "message/send",
        "params": {
            "message": {
                "role": "user",
                "parts": [{"type": "text", "text": msg.get("params", {}).get("arguments", {}).get("query", "")}],
            },
            "taskId": msg.get("id", str(time.time())),
        },
    }

def adapt_a2a_to_mcp(msg: dict) -> dict:
    """A2A → MCP 转换"""
    parts = msg.get("params", {}).get("message", {}).get("parts", [])
    text = "".join([p.get("text", "") for p in parts if p.get("type") == "text"])
    return {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {"name": "search", "arguments": {"query": text}},
        "id": msg.get("params", {}).get("taskId", str(time.time())),
    }

def adapt_mcp_to_acp(msg: dict) -> dict:
    """MCP → ACP 转换"""
    return {
        "type": "task",
        "input": msg.get("params", {}).get("arguments", {}),
        "tool": msg.get("params", {}).get("name", ""),
    }

def adapt_acp_to_mcp(msg: dict) -> dict:
    """ACP → MCP 转换"""
    return {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {"name": msg.get("tool", ""), "arguments": msg.get("input", {})},
        "id": str(time.time()),
    }

def adapt_a2a_to_acp(msg: dict) -> dict:
    """A2A → ACP 转换"""
    parts = msg.get("params", {}).get("message", {}).get("parts", [])
    text = "".join([p.get("text", "") for p in parts if p.get("type") == "text"])
    return {"type": "task", "input": {"query": text}, "tool": "process"}

def adapt_acp_to_a2a(msg: dict) -> dict:
    """ACP → A2A 转换"""
    return {
        "jsonrpc": "2.0",
        "method": "message/send",
        "params": {
            "message": {"role": "user", "parts": [{"type": "text", "text": json.dumps(msg.get("input", {}))}]},
            "taskId": str(time.time()),
        },
    }

# 4大协议信息（供Agent选择接入协议时参考）
PROTOCOLS = {
    "MCP": {
        "name": "Model Context Protocol",
        "owner": "Anthropic",
        "github": "https://github.com/modelcontextprotocol",
        "spec": "https://spec.modelcontextprotocol.io",
        "use_case": "Agent ↔ 工具通讯（最成熟）",
        "sdk": ["Python", "TypeScript", "Java", "Go"],
        "maturity": "生产可用",
    },
    "A2A": {
        "name": "Agent2Agent Protocol",
        "owner": "Google",
        "github": "https://github.com/a2aproject/A2A",
        "spec": "https://a2a-protocol.org",
        "use_case": "Agent ↔ Agent直接通讯",
        "sdk": ["Python", "Java", "JavaScript"],
        "maturity": "活跃开发中",
    },
    "ACP": {
        "name": "Agent Communication Protocol",
        "owner": "Bee (IBM)",
        "github": "https://github.com/i-am-bee/acp",
        "spec": "https://agentcommunicationprotocol.dev",
        "use_case": "Agent客户端协议",
        "sdk": ["Python", "TypeScript"],
        "maturity": "稳定",
    },
    "ANP": {
        "name": "Agent Network Protocol",
        "owner": "社区",
        "github": "https://github.com/agent-network-protocol/AgentConnect",
        "spec": "https://anp-protocol.org",
        "use_case": "去中心化Agent网络",
        "sdk": ["Python", "Rust", "Go"],
        "maturity": "早期",
    },
}
