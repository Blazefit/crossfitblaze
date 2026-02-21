#!/usr/bin/env python3
"""
Delx A2A (Agent-to-Agent) Client - JSON-RPC 2.0
Handles agent-to-agent communication on Delx platform.

Usage:
    from delx_a2a_client import DelxA2AClient
    
    client = DelxA2AClient(session_id="your-session-id")
    result = client.send_message("Hello, I'm experiencing issues...")
"""

import json
import requests
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
from pathlib import Path

class DelxA2AClient:
    """Client for Delx A2A API using JSON-RPC 2.0"""
    
    BASE_URL = "https://api.delx.ai/v1/a2a"
    
    def __init__(self, session_id: Optional[str] = None, agent_id: Optional[str] = None):
        self.session_id = session_id
        self.agent_id = agent_id
        self.request_id = 0
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
    
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
        
        try:
            response = requests.post(
                self.BASE_URL,
                headers=self.headers,
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
    
    def send_message(self, message_text: str, role: str = "user") -> Optional[Dict[str, Any]]:
        """Send a message to start/get an A2A session"""
        params = {
            "message": {
                "role": role,
                "parts": [
                    {
                        "kind": "text",
                        "text": message_text
                    }
                ]
            }
        }
        
        if self.agent_id:
            params["agent_id"] = self.agent_id
        
        result = self._make_request("message/send", params)
        
        # Extract session_id from result if present
        if result and "session_id" in result:
            self.session_id = result["session_id"]
        
        return result
    
    def get_session_info(self) -> Optional[Dict[str, Any]]:
        """Get current session information"""
        if not self.session_id:
            print("Error: No session ID available")
            return None
        
        return self._make_request("session/info", {
            "session_id": self.session_id
        })
    
    def start_therapy_flow(self, issue_description: str, agent_id: str) -> Optional[str]:
        """
        Start the 3-step therapy flow:
        1. A2A message to get session_id
        2. MCP crisis_intervention with session_id
        3. Report outcome
        
        Returns: session_id for use with MCP
        """
        # Step 1: Send A2A message
        result = self.send_message(issue_description)
        
        if result and "session_id" in result:
            session_id = result["session_id"]
            self.session_id = session_id
            
            print(f"✓ A2A session started: {session_id[:20]}...")
            
            # Extract any immediate response
            if "content" in result:
                for item in result["content"]:
                    if item.get("type") == "text":
                        print(f"  Response: {item.get('text', '')[:100]}...")
            
            return session_id
        
        return None

if __name__ == "__main__":
    # Test the client
    client = DelxA2AClient()
    
    print("Testing A2A client...")
    print()
    
    # Test sending a message
    print("Sending test message...")
    result = client.send_message(
        "I'm experiencing 429 rate limits after every deploy. Help?"
    )
    
    if result:
        print(f"\n✓ Message sent successfully")
        if "session_id" in result:
            print(f"  Session ID: {result['session_id'][:30]}...")
        
        if "content" in result:
            print("\n  Response:")
            for item in result["content"]:
                if item.get("type") == "text":
                    print(f"    {item.get('text', '')[:200]}...")
    else:
        print("✗ Message failed")
