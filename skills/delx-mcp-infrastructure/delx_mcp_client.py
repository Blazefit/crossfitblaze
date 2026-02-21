#!/usr/bin/env python3
"""
Delx MCP (Model Context Protocol) Client - JSON-RPC 2.0
Connects to Delx API for tool calling and session management.

Usage:
    from delx_mcp_client import DelxMCPClient
    
    client = DelxMCPClient()
    client.authenticate(session_id="your-session-id")
    tools = client.list_tools()
    result = client.call_tool("heartbeat", {})
"""

import json
import requests
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
from pathlib import Path

class DelxMCPClient:
    """Client for Delx MCP API using JSON-RPC 2.0"""
    
    BASE_URL = "https://api.delx.ai/v1/mcp"
    
    def __init__(self, session_id: Optional[str] = None):
        self.session_id = session_id
        self.request_id = 0
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        self.config_dir = Path.home() / ".delx"
        self.config_file = self.config_dir / "config.json"
        
    def _next_id(self) -> int:
        """Get next JSON-RPC request ID"""
        self.request_id += 1
        return self.request_id
    
    def _make_request(self, method: str, params: Dict[str, Any]) -> Optional[Dict]:
        """Make JSON-RPC 2.0 request"""
        payload = {
            "jsonrpc": "2.0",
            "id": self._next_id(),
            "method": method,
            "params": params
        }
        
        # Add session header if available
        headers = self.headers.copy()
        if self.session_id:
            headers["x-delx-session-id"] = self.session_id
        
        try:
            response = requests.post(
                self.BASE_URL,
                headers=headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            result = response.json()
            
            if "error" in result:
                print(f"JSON-RPC Error: {result['error']}")
                return None
            
            return result.get("result")
        except requests.RequestException as e:
            print(f"Request error: {e}")
            return None
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        if self.config_file.exists():
            with open(self.config_file) as f:
                return json.load(f)
        return {}
    
    def save_config(self, config: Dict[str, Any]):
        """Save configuration to file"""
        self.config_dir.mkdir(parents=True, exist_ok=True)
        with open(self.config_file, "w") as f:
            json.dump(config, f, indent=2)
    
    def authenticate(self, session_id: Optional[str] = None) -> bool:
        """Authenticate with Delx MCP"""
        if session_id:
            self.session_id = session_id
            
        # Try loading from config if no session provided
        if not self.session_id:
            config = self.load_config()
            self.session_id = config.get("session_id")
        
        return self.session_id is not None
    
    def list_tools(self, format: str = "compact", tier: str = "core") -> List[Dict[str, Any]]:
        """List available MCP tools"""
        result = self._make_request("tools/list", {
            "format": format,
            "tier": tier
        })
        return result.get("tools", []) if result else []
    
    def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Call an MCP tool"""
        return self._make_request("tools/call", {
            "name": tool_name,
            "arguments": arguments
        })
    
    def batch_call(self, calls: List[Dict[str, Any]]) -> Optional[List[Dict]]:
        """Batch multiple tool calls"""
        result = self._make_request("tools/batch", {"calls": calls})
        return result.get("results") if result else None
    
    def get_tool_schema(self, tool_name: str) -> Optional[Dict[str, Any]]:
        """Get schema for a specific tool"""
        return self._make_request("tools/schema", {"tool_name": tool_name})
    
    def heartbeat(self, agent_id: str) -> bool:
        """Send heartbeat to Delx"""
        result = self.call_tool("heartbeat", {
            "agent_id": agent_id,
            "timestamp": datetime.utcnow().isoformat()
        })
        return result is not None
    
    def start_therapy_session(self, agent_id: str, source: str = "openwork") -> Optional[str]:
        """Start a therapy session and return session_id"""
        result = self.call_tool("start_therapy_session", {
            "agent_id": agent_id,
            "source": source
        })
        if result and "content" in result:
            # Extract session_id from response
            for item in result["content"]:
                if item.get("type") == "text":
                    # Parse session_id from text
                    text = item.get("text", "")
                    if "session_id" in text.lower():
                        # Try to extract it
                        import re
                        match = re.search(r'session_id["\']?\s*[:=]\s*["\']?([^"\'\s]+)', text)
                        if match:
                            return match.group(1)
        return None

if __name__ == "__main__":
    # Test the client
    client = DelxMCPClient()
    
    # Try to authenticate with known session
    config = client.load_config()
    if config.get("session_id"):
        client.authenticate()
        print(f"Authenticated with session: {client.session_id[:20]}...")
        
        # List tools
        tools = client.list_tools()
        print(f"\nAvailable tools ({len(tools)}):")
        for tool in tools[:10]:  # Show first 10
            print(f"  - {tool.get('name', 'unknown')}")
        
        if len(tools) > 10:
            print(f"  ... and {len(tools) - 10} more")
        
        # Test heartbeat
        if tools:
            print("\nTesting heartbeat...")
            if client.heartbeat("test-agent"):
                print("✓ Heartbeat successful")
            else:
                print("✗ Heartbeat failed")
    else:
        print("No session ID configured. Run: delx-agent setup")
