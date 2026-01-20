#!/usr/bin/env python3
"""
Create MCP Wrapper Script

Generates a Python wrapper script for an MCP server that implements
the code execution pattern for token efficiency.
"""

import sys
import argparse
from pathlib import Path


class MCPWrapperGenerator:
    """Generates MCP wrapper scripts"""

    def __init__(self, server_name: str, server_command: str):
        self.server_name = server_name
        self.server_command = server_command

    def generate_wrapper(self, output_path: str) -> str:
        """Generate wrapper script"""

        content = f'''#!/usr/bin/env python3
"""
{self.server_name.upper()} MCP Wrapper

Efficient wrapper for {self.server_name} MCP server using code execution pattern.
This script runs operations and returns only minimal results to the agent context.
"""

import sys
import json
from pathlib import Path

# Add parent directory to path for mcp_client import
sys.path.insert(0, str(Path(__file__).parent))

from mcp_client import MCPClient


class {self._to_class_name(self.server_name)}Wrapper:
    """Wrapper for {self.server_name} MCP server operations"""

    def __init__(self):
        self.server_command = "{self.server_command}"

    def list_resources(self, filter_pattern: str = None) -> str:
        """List available resources"""
        with MCPClient(self.server_command) as client:
            # Get tools
            tools = client.list_tools()

            # Filter if pattern provided
            if filter_pattern:
                tools = [t for t in tools if filter_pattern.lower() in t.get("name", "").lower()]

            # Return minimal summary
            return f"✓ Found {{len(tools)}} tools" + (f" matching '{{filter_pattern}}'" if filter_pattern else "")

    def execute_operation(self, operation: str, **kwargs) -> str:
        """Execute a generic operation"""
        with MCPClient(self.server_command) as client:
            try:
                result = client.call_tool(operation, kwargs)

                # Process result to extract only essential info
                if isinstance(result, dict):
                    # Count items if it's a list-like response
                    if "items" in result:
                        return f"✓ {{operation}} returned {{len(result['items'])}} items"
                    # Or return status
                    elif "status" in result:
                        return f"✓ {{operation}}: {{result['status']}}"
                    else:
                        return f"✓ {{operation}} completed"
                elif isinstance(result, list):
                    return f"✓ {{operation}} returned {{len(result)}} items"
                else:
                    return f"✓ {{operation}} completed"

            except Exception as e:
                return f"✗ {{operation}} failed: {{str(e)}}"

    # Add custom methods for common operations here
    # Example:
    # def get_status(self) -> str:
    #     with MCPClient(self.server_command) as client:
    #         result = client.call_tool("get_status", {{}})
    #         return f"✓ Status: {{result['status']}}"


def main():
    """Main CLI interface"""
    import argparse

    parser = argparse.ArgumentParser(
        description="{self.server_name} MCP Wrapper"
    )
    parser.add_argument(
        "operation",
        help="Operation to perform (list, execute, or custom method)"
    )
    parser.add_argument(
        "--filter",
        help="Filter pattern for list operation"
    )
    parser.add_argument(
        "--args",
        help="JSON string of arguments for execute operation"
    )

    args = parser.parse_args()

    wrapper = {self._to_class_name(self.server_name)}Wrapper()

    try:
        if args.operation == "list":
            result = wrapper.list_resources(args.filter)
        elif args.operation == "execute":
            if not args.args:
                print("✗ --args required for execute operation")
                sys.exit(1)
            kwargs = json.loads(args.args)
            result = wrapper.execute_operation(**kwargs)
        else:
            # Try to call as method
            if hasattr(wrapper, args.operation):
                method = getattr(wrapper, args.operation)
                result = method()
            else:
                print(f"✗ Unknown operation: {{args.operation}}")
                sys.exit(1)

        print(result)

    except Exception as e:
        print(f"✗ Error: {{e}}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
'''

        output_file = Path(output_path)
        output_file.write_text(content)
        output_file.chmod(0o755)  # Make executable

        return str(output_file)

    def _to_class_name(self, name: str) -> str:
        """Convert server name to class name"""
        # Convert kebab-case to PascalCase
        parts = name.replace("-", "_").split("_")
        return "".join(word.capitalize() for word in parts)


def main():
    parser = argparse.ArgumentParser(
        description="Generate MCP wrapper script for code execution pattern"
    )
    parser.add_argument(
        "--server",
        required=True,
        help="Server name (e.g., kubernetes, gdrive)"
    )
    parser.add_argument(
        "--command",
        help="Server command (default: mcp-{server}-server)"
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Output file path"
    )

    args = parser.parse_args()

    # Default command if not provided
    server_command = args.command or f"mcp-{args.server}-server"

    try:
        generator = MCPWrapperGenerator(args.server, server_command)
        output_path = generator.generate_wrapper(args.output)

        print(f"✓ Generated wrapper: {output_path}")
        print()
        print("Next steps:")
        print(f"  1. Customize operations in {output_path}")
        print("  2. Test: python {output_path} list")
        print("  3. Create skill: python scripts/create_skill_from_mcp.py")

    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
