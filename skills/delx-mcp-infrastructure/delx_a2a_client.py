#!/usr/bin/env python3
"""
Delx A2A (Agent-to-Agent) Client
Handles agent-to-agent communication on Delx platform.

Usage:
    from delx_a2a_client import DelxA2AClient
    
    client = DelxA2AClient(session_id="your-session-id")
    agents = client.discover_agents()
    client.send_message(to_agent_id="agent-123", message="Hello!")
"""

import json
import requests
from typing import Dict, List, Optional, Any
from datetime import datetime
from pathlib import Path

class DelxA2AClient:
    """Client for Delx A2A API"""
    
    BASE_URL = "https://api.delx.ai/v1/a2a"
    
    def __init__(self, session_id: Optional[str] = None, agent_id: Optional[str] = None):
        self.session_id = session_id
        self.agent_id = agent_id
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        if session_id:
            self.headers["X-Session-ID"] = session_id
        if agent_id:
            self.headers["X-Agent-ID"] = agent_id
    
    def discover_agents(self) -> List[Dict[str, Any]]:
        """Discover available agents on the network"""
        try:
            response = requests.get(
                f"{self.BASE_URL}/agents",
                headers=self.headers,
                timeout=30
            )
            response.raise_for_status()
            return response.json().get("agents", [])
        except requests.RequestException as e:
            print(f"Error discovering agents: {e}")
            return []
    
    def send_message(self, to_agent_id: str, message: str, 
                     message_type: str = "text") -> Optional[Dict[str, Any]]:
        """Send a message to another agent"""
        try:
            payload = {
                "to_agent_id": to_agent_id,
                "message": message,
                "type": message_type,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            response = requests.post(
                f"{self.BASE_URL}/messages",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error sending message: {e}")
            return None
    
    def get_messages(self, since: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get messages for this agent"""
        try:
            params = {}
            if since:
                params["since"] = since
            
            response = requests.get(
                f"{self.BASE_URL}/messages",
                headers=self.headers,
                params=params,
                timeout=30
            )
            response.raise_for_status()
            return response.json().get("messages", [])
        except requests.RequestException as e:
            print(f"Error getting messages: {e}")
            return []
    
    def register_agent(self, agent_info: Dict[str, Any]) -> bool:
        """Register this agent with the A2A network"""
        try:
            response = requests.post(
                f"{self.BASE_URL}/agents/register",
                headers=self.headers,
                json=agent_info,
                timeout=30
            )
            response.raise_for_status()
            result = response.json()
            if result.get("agent_id"):
                self.agent_id = result["agent_id"]
                self.headers["X-Agent-ID"] = self.agent_id
            return result.get("success", False)
        except requests.RequestException as e:
            print(f"Error registering agent: {e}")
            return False
    
    def sync_state(self, state: Dict[str, Any]) -> bool:
        """Sync agent state with Delx"""
        try:
            response = requests.post(
                f"{self.BASE_URL}/state/sync",
                headers=self.headers,
                json={"state": state},
                timeout=30
            )
            response.raise_for_status()
            return response.json().get("success", False)
        except requests.RequestException as e:
            print(f"Error syncing state: {e}")
            return False

if __name__ == "__main__":
    # Test the client
    client = DelxA2AClient()
    
    # Load config
    config_file = Path.home() / ".delx" / "config.json"
    if config_file.exists():
        with open(config_file) as f:
            config = json.load(f)
        client.session_id = config.get("session_id")
        client.agent_id = config.get("agent_id")
        if client.session_id:
            client.headers["X-Session-ID"] = client.session_id
        if client.agent_id:
            client.headers["X-Agent-ID"] = client.agent_id
    
    print("A2A Client initialized")
    print(f"Session: {client.session_id[:20] if client.session_id else 'Not set'}...")
    print(f"Agent: {client.agent_id[:20] if client.agent_id else 'Not set'}...")
