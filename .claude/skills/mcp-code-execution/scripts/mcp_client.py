#!/usr/bin/env python3
"""
Generic MCP Client

Provides a Python interface for interacting with MCP servers.
"""

import json
import subprocess
from typing import Any, Dict, List, Optional


class MCPClient:
    """Client for interacting with MCP servers"""

    def __init__(self, server_command: str, env: Optional[Dict[str, str]] = None):
        """
        Initialize MCP client

        Args:
            server_command: Command to start MCP server (e.g., "mcp-k8s-server")
            env: Optional environment variables for the server
        """
        self.server_command = server_command
        self.env = env or {}
        self.process = None
        self.request_id = 0

    def __enter__(self):
        """Start MCP server as context manager"""
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Stop MCP server"""
        self.stop()

    def start(self):
        """Start the MCP server process"""
        import os

        env = os.environ.copy()
        env.update(self.env)

        self.process = subprocess.Popen(
            self.server_command.split(),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=env
        )

    def stop(self):
        """Stop the MCP server process"""
        if self.process:
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
                self.process.wait()

    def _send_request(self, method: str, params: Dict[str, Any]) -> Any:
        """Send JSON-RPC request to MCP server"""
        if not self.process:
            raise Exception("MCP server not started")

        self.request_id += 1

        request = {
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": method,
            "params": params
        }

        # Send request
        request_json = json.dumps(request) + "\n"
        self.process.stdin.write(request_json)
        self.process.stdin.flush()

        # Read response
        response_line = self.process.stdout.readline()
        if not response_line:
            raise Exception("No response from MCP server")

        response = json.loads(response_line)

        # Check for errors
        if "error" in response:
            error = response["error"]
            raise Exception(f"MCP error: {error.get('message', 'Unknown error')}")

        return response.get("result")

    def list_tools(self) -> List[Dict[str, Any]]:
        """List available tools from the MCP server"""
        return self._send_request("tools/list", {})

    def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """
        Call an MCP tool

        Args:
            tool_name: Name of the tool to call
            arguments: Tool arguments

        Returns:
            Tool result
        """
        return self._send_request("tools/call", {
            "name": tool_name,
            "arguments": arguments
        })

    def get_prompts(self) -> List[Dict[str, Any]]:
        """Get available prompts from the MCP server"""
        return self._send_request("prompts/list", {})

    def get_prompt(self, prompt_name: str, arguments: Dict[str, Any] = None) -> str:
        """Get a specific prompt"""
        return self._send_request("prompts/get", {
            "name": prompt_name,
            "arguments": arguments or {}
        })


def test_connection(server_command: str) -> bool:
    """Test connection to an MCP server"""
    try:
        with MCPClient(server_command) as client:
            tools = client.list_tools()
            print(f"✓ Connected to MCP server")
            print(f"  Available tools: {len(tools)}")
            for tool in tools[:5]:  # Show first 5
                print(f"    - {tool.get('name', 'unknown')}")
            return True
    except Exception as e:
        print(f"✗ Connection failed: {e}")
        return False


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python mcp_client.py <server-command>")
        print("Example: python mcp_client.py mcp-k8s-server")
        sys.exit(1)

    server_cmd = sys.argv[1]
    success = test_connection(server_cmd)
    sys.exit(0 if success else 1)
