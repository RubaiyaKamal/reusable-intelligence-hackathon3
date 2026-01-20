#!/usr/bin/env python3
"""
Create Skill from MCP Wrapper

Generates a complete skill directory structure from an MCP wrapper script.
"""

import sys
import argparse
from pathlib import Path


class SkillGenerator:
    """Generates skills from MCP wrappers"""

    def __init__(self, script_path: str, skill_name: str):
        self.script_path = Path(script_path)
        self.skill_name = skill_name
        self.skill_dir = Path(".claude/skills") / skill_name

    def generate(self):
        """Generate complete skill structure"""
        print(f"🚀 Generating skill: {self.skill_name}")

        # Create directory structure
        self.skill_dir.mkdir(parents=True, exist_ok=True)
        (self.skill_dir / "scripts").mkdir(exist_ok=True)

        # Copy wrapper script
        import shutil
        shutil.copy(self.script_path, self.skill_dir / "scripts" / self.script_path.name)

        # Generate SKILL.md
        self._generate_skill_md()

        # Generate REFERENCE.md
        self._generate_reference_md()

        print(f"✓ Skill generated: {self.skill_dir}")
        print()
        print("Next steps:")
        print(f"  1. Review and customize {self.skill_dir}/SKILL.md")
        print(f"  2. Add documentation to {self.skill_dir}/REFERENCE.md")
        print(f"  3. Test with: claude 'use {self.skill_name}'")

    def _generate_skill_md(self):
        """Generate SKILL.md"""
        script_name = self.script_path.name

        content = f'''---
name: {self.skill_name}
description: MCP-based operations with code execution pattern
version: 1.0.0
author: Auto-generated
tags: [mcp, efficiency, wrapper]
---

# {self.skill_name.replace("-", " ").title()}

## When to Use
- Need to interact with {self.skill_name} resources
- Want efficient token usage (80-98% reduction)
- Performing batch or repeated operations

## What This Skill Does
Provides efficient access to {self.skill_name} MCP server through code execution pattern.
Operations execute outside agent context, returning only minimal results.

## Instructions

1. **List Available Operations**
   ```bash
   python scripts/{script_name} list
   ```

2. **Execute Operation**
   ```bash
   python scripts/{script_name} execute --args '{{"operation": "value"}}'
   ```

3. **Custom Operations**
   ```bash
   python scripts/{script_name} <operation-name>
   ```

## Token Efficiency

| Approach | Tokens | Context % |
|----------|--------|-----------|
| Direct MCP | 15,000+ | 12%+ |
| This Skill | ~120 | <1% |
| **Savings** | **~99%** | **~12x less** |

## Validation Checklist
- [ ] Operation completes successfully
- [ ] Results are minimal and actionable
- [ ] No errors in execution
- [ ] Output matches expectations

## Expected Output
```
✓ Operation completed
✓ Processed X items
```

See [REFERENCE.md](./REFERENCE.md) for detailed documentation and examples.
'''

        (self.skill_dir / "SKILL.md").write_text(content)
        print(f"  ✓ Created SKILL.md")

    def _generate_reference_md(self):
        """Generate REFERENCE.md template"""
        content = f'''# {self.skill_name.replace("-", " ").title()} - Reference Documentation

## Overview

This skill provides efficient access to {self.skill_name} MCP server using the code execution pattern.

## MCP Server Details

**Server Command**: `mcp-{self.skill_name}-server`

**Purpose**: [DESCRIBE PURPOSE]

## Available Operations

### List Resources
```bash
python scripts/{self.script_path.name} list
python scripts/{self.script_path.name} list --filter "pattern"
```

Returns: Minimal count of resources

### Execute Operation
```bash
python scripts/{self.script_path.name} execute --args '{{"operation": "name", "param": "value"}}'
```

Returns: Operation status

## Examples

### Example 1: [OPERATION NAME]
```bash
python scripts/{self.script_path.name} [operation]
```

**Output:**
```
✓ [Operation] completed: [result]
```

### Example 2: [OPERATION NAME]
```bash
python scripts/{self.script_path.name} [operation] --args '{{"key": "value"}}'
```

**Output:**
```
✓ Processed X items
```

## Customization

### Adding New Operations

Edit `scripts/{self.script_path.name}` and add methods:

```python
def custom_operation(self, param1: str) -> str:
    """Custom operation description"""
    with MCPClient(self.server_command) as client:
        result = client.call_tool("tool_name", {{"param": param1}})
        # Process and filter result
        return f"✓ Operation result: {{summary}}"
```

## Token Efficiency Analysis

### Before (Direct MCP)
- MCP server loaded at startup: 10,000 tokens
- Tool call returns full data: 15,000 tokens
- **Total: 25,000 tokens (20% of context)**

### After (Code Execution)
- Skill loaded on trigger: 100 tokens
- Script executes, filters data, returns summary: 20 tokens
- **Total: 120 tokens (< 1% of context)**

### Savings: 99% token reduction

## Troubleshooting

### MCP Server Not Found
```bash
# Check server installation
which mcp-{self.skill_name}-server

# Test server directly
mcp-{self.skill_name}-server --version
```

### Connection Errors
```bash
# Test wrapper directly
python scripts/{self.script_path.name} list

# Check MCP client
python scripts/mcp_client.py mcp-{self.skill_name}-server
```

## Best Practices

1. **Filter Data Aggressively**: Return only essential information
2. **Use Summaries**: Counts and statuses instead of full data
3. **Handle Errors Gracefully**: Return clear error messages
4. **Cache When Possible**: Avoid repeated expensive operations
5. **Batch Operations**: Process multiple items in one script execution

## Resources

- [MCP Code Execution Pattern](https://www.anthropic.com/engineering/code-execution-with-mcp)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [MCP Server Documentation]([ADD LINK])
'''

        (self.skill_dir / "REFERENCE.md").write_text(content)
        print(f"  ✓ Created REFERENCE.md")


def main():
    parser = argparse.ArgumentParser(
        description="Generate skill from MCP wrapper script"
    )
    parser.add_argument(
        "--script",
        required=True,
        help="Path to MCP wrapper script"
    )
    parser.add_argument(
        "--name",
        required=True,
        help="Skill name (e.g., k8s-ops, gdrive-sync)"
    )

    args = parser.parse_args()

    try:
        generator = SkillGenerator(args.script, args.name)
        generator.generate()

    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
