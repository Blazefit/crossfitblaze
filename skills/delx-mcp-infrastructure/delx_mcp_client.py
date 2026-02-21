#!/usr/bin/env python3
"""
Delx MCP (Model Context Protocol) Client
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
from typing import Dict, List, Optional, Any
from datetime import datetime
from pathlib import Path

class DelxMCPClient:
    """Client for Delx MCP API"""
    
    BASE_URL = "https://api.delx.ai/v1/mcp"
    
    def __init__(self, session_id: Optional[str] = None):
        self.session_id = session_id
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        self.config_dir = Path.home() / ".delx"
        self.config_file = self.config_dir / "config.json"
        
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
            self.headers["X-Session-ID"] = session_id
            
        # Try loading from config if no session provided
        if not self.session_id:
            config = self.load_config()
            self.session_id = config.get("session_id")
            if self.session_id:
                self.headers["X-Session-ID"] = self.session_id
        
        return self.session_id is not None
    
    def list_tools(self) -> List[Dict[str, Any]]:
        """List available MCP tools"""
        try:
            response = requests.get(
                f"{self.BASE_URL}/tools",
                headers=self.headers,
                timeout=30
            )
            response.raise_for_status()
            return response.json().get("tools", [])
        except requests.RequestException as e:
            print(f"Error listing tools: {e}")
            return []
    
    def call_tool(self, tool_name: str, params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Call an MCP tool"""
        try:
            response = requests.post(
                f"{self.BASE_URL}/tools/{tool_name}",
                headers=self.headers,
                json=params,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error calling tool {tool_name}: {e}")
            return None
    
    def heartbeat(self, agent_id: str, status: str = "active") -> bool:
        """Send heartbeat to Delx"""
        result = self.call_tool("heartbeat", {
            "agent_id": agent_id,
            "status": status,
            "timestamp": datetime.utcnow().isoformat()
        })
        return result is not None and result.get("success", False)
    
    def get_session_info(self) -> Optional[Dict[str, Any]]:
        """Get current session information"""
        try:
            response = requests.get(
                f"{self.BASE_URL}/session",
                headers=self.headers,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error getting session info: {e}")
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
        for tool in tools:
            print(f"  - {tool.get('name')}: {tool.get('description', 'No description')}")
    else:
        print("No session ID configured. Run: delx-agent setup")
