#!/usr/bin/env python3
"""
AGENTS.md Generator Script

This script analyzes a repository and generates an AGENTS.md file
that helps AI coding agents understand the codebase structure.
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Optional


class AgentsMdGenerator:
    """Generates AGENTS.md files for repositories"""

    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path).resolve()
        self.repo_name = self.repo_path.name

    def analyze_repository(self) -> Dict:
        """Analyze repository structure and extract metadata"""
        analysis = {
            "name": self.repo_name,
            "structure": self._analyze_structure(),
            "tech_stack": self._detect_tech_stack(),
            "conventions": self._extract_conventions(),
            "dependencies": self._parse_dependencies()
        }
        return analysis

    def _analyze_structure(self) -> Dict:
        """Analyze directory structure"""
        structure = {}
        important_dirs = ['src', 'app', 'lib', 'tests', 'test', 'docs', 'scripts',
                         'k8s', 'kubernetes', '.claude', 'api', 'services']

        for dir_name in important_dirs:
            dir_path = self.repo_path / dir_name
            if dir_path.exists() and dir_path.is_dir():
                structure[dir_name] = self._get_directory_description(dir_name)

        return structure

    def _get_directory_description(self, dir_name: str) -> str:
        """Get description for common directory names"""
        descriptions = {
            'src': 'Source code',
            'app': 'Application code',
            'lib': 'Library modules',
            'tests': 'Test files',
            'test': 'Test files',
            'docs': 'Documentation',
            'scripts': 'Automation scripts',
            'k8s': 'Kubernetes manifests',
            'kubernetes': 'Kubernetes manifests',
            '.claude': 'Claude Code skills',
            'api': 'API endpoints',
            'services': 'Microservices'
        }
        return descriptions.get(dir_name, 'Project files')

    def _detect_tech_stack(self) -> Dict:
        """Detect technologies used in the repository"""
        tech_stack = {}

        # Check for Python
        if (self.repo_path / "requirements.txt").exists() or \
           (self.repo_path / "pyproject.toml").exists() or \
           (self.repo_path / "setup.py").exists():
            tech_stack["language"] = "Python"
            tech_stack["runtime"] = self._detect_python_version()
            tech_stack["framework"] = self._detect_python_framework()

        # Check for Node.js
        if (self.repo_path / "package.json").exists():
            tech_stack["language"] = "JavaScript/TypeScript"
            tech_stack["runtime"] = "Node.js"
            tech_stack["framework"] = self._detect_js_framework()

        # Check for Go
        if (self.repo_path / "go.mod").exists():
            tech_stack["language"] = "Go"
            tech_stack["framework"] = self._detect_go_framework()

        # Check for Docker
        if (self.repo_path / "Dockerfile").exists():
            tech_stack["containerization"] = "Docker"

        # Check for Kubernetes
        if (self.repo_path / "k8s").exists() or \
           (self.repo_path / "kubernetes").exists():
            tech_stack["orchestration"] = "Kubernetes"

        return tech_stack

    def _detect_python_version(self) -> str:
        """Detect Python version from project files"""
        pyproject = self.repo_path / "pyproject.toml"
        if pyproject.exists():
            content = pyproject.read_text()
            if "python = " in content:
                # Extract version from pyproject.toml
                for line in content.split('\n'):
                    if 'python = ' in line:
                        return line.split('"')[1] if '"' in line else "3.11+"
        return "3.11+"

    def _detect_python_framework(self) -> Optional[str]:
        """Detect Python web framework"""
        requirements_file = self.repo_path / "requirements.txt"
        if requirements_file.exists():
            content = requirements_file.read_text().lower()
            if "fastapi" in content:
                return "FastAPI"
            elif "flask" in content:
                return "Flask"
            elif "django" in content:
                return "Django"
        return None

    def _detect_js_framework(self) -> Optional[str]:
        """Detect JavaScript/TypeScript framework"""
        package_json = self.repo_path / "package.json"
        if package_json.exists():
            with open(package_json, 'r') as f:
                data = json.load(f)
                deps = {**data.get('dependencies', {}), **data.get('devDependencies', {})}

                if 'next' in deps:
                    return "Next.js"
                elif 'react' in deps:
                    return "React"
                elif 'vue' in deps:
                    return "Vue.js"
                elif '@angular/core' in deps:
                    return "Angular"
        return None

    def _detect_go_framework(self) -> Optional[str]:
        """Detect Go framework"""
        go_mod = self.repo_path / "go.mod"
        if go_mod.exists():
            content = go_mod.read_text()
            if "gin-gonic/gin" in content:
                return "Gin"
            elif "gorilla/mux" in content:
                return "Gorilla Mux"
            elif "fiber" in content:
                return "Fiber"
        return None

    def _extract_conventions(self) -> Dict:
        """Extract coding conventions from linter configs"""
        conventions = {}

        # Check for Python linting
        if (self.repo_path / ".flake8").exists() or \
           (self.repo_path / "setup.cfg").exists():
            conventions["python_linter"] = "flake8"

        if (self.repo_path / ".pylintrc").exists():
            conventions["python_linter"] = "pylint"

        if (self.repo_path / "pyproject.toml").exists():
            content = (self.repo_path / "pyproject.toml").read_text()
            if "[tool.black]" in content:
                conventions["python_formatter"] = "black"

        # Check for JS/TS linting
        if (self.repo_path / ".eslintrc.json").exists() or \
           (self.repo_path / ".eslintrc.js").exists():
            conventions["js_linter"] = "ESLint"

        if (self.repo_path / ".prettierrc").exists():
            conventions["js_formatter"] = "Prettier"

        return conventions

    def _parse_dependencies(self) -> List[str]:
        """Parse and return key dependencies"""
        dependencies = []

        # Python dependencies
        requirements_file = self.repo_path / "requirements.txt"
        if requirements_file.exists():
            content = requirements_file.read_text()
            key_packages = ['fastapi', 'flask', 'django', 'kafka', 'redis',
                          'postgresql', 'sqlalchemy', 'pydantic', 'openai']
            for line in content.split('\n'):
                for pkg in key_packages:
                    if pkg in line.lower():
                        dependencies.append(line.strip().split('==')[0])

        # Node dependencies
        package_json = self.repo_path / "package.json"
        if package_json.exists():
            with open(package_json, 'r') as f:
                data = json.load(f)
                deps = {**data.get('dependencies', {}), **data.get('devDependencies', {})}
                dependencies.extend(list(deps.keys())[:10])  # Top 10

        return dependencies

    def generate_agents_md(self, analysis: Dict) -> str:
        """Generate AGENTS.md content from analysis"""

        content = f"""# {analysis['name']}

**Purpose**: [DESCRIBE_PURPOSE_HERE]

**Type**: [e.g., Microservice, Frontend App, Library]

**Primary Language**: {analysis['tech_stack'].get('language', 'Not detected')}

## Directory Structure

```
/
"""

        # Add directory structure
        for dir_name, description in analysis['structure'].items():
            content += f"├── {dir_name}/              # {description}\n"

        content += """```

## Technology Stack

"""

        # Add tech stack
        tech_stack = analysis['tech_stack']
        if 'runtime' in tech_stack:
            content += f"- **Runtime**: {tech_stack['runtime']}\n"
        if 'framework' in tech_stack:
            content += f"- **Framework**: {tech_stack['framework']}\n"
        if 'containerization' in tech_stack:
            content += f"- **Containerization**: {tech_stack['containerization']}\n"
        if 'orchestration' in tech_stack:
            content += f"- **Orchestration**: {tech_stack['orchestration']}\n"

        content += """
## Development Conventions

### Code Style
- Follow language-specific best practices
- Use consistent formatting
- Write clear, self-documenting code

### Testing
- Write tests for all business logic
- Maintain minimum 80% code coverage
- Include both unit and integration tests

## Getting Started

### Prerequisites
"""

        # Add prerequisites based on tech stack
        if tech_stack.get('language') == 'Python':
            content += f"- Python {tech_stack.get('runtime', '3.11')}+\n"
        elif tech_stack.get('language') == 'JavaScript/TypeScript':
            content += "- Node.js 18+\n"

        if 'containerization' in tech_stack:
            content += "- Docker Desktop\n"

        if 'orchestration' in tech_stack:
            content += "- kubectl\n"
            content += "- Minikube (for local development)\n"

        content += """
### Setup
```bash
# 1. Clone repository
git clone [REPO_URL]

# 2. Install dependencies
[INSTALL_COMMAND_HERE]

# 3. Configure environment
cp .env.example .env

# 4. Run application
[RUN_COMMAND_HERE]
```

## Common Tasks

### Run Tests
```bash
[TEST_COMMAND_HERE]
```

### Build
```bash
[BUILD_COMMAND_HERE]
```

### Deploy
```bash
[DEPLOY_COMMAND_HERE]
```

## Architecture Decisions

[DOCUMENT_KEY_ARCHITECTURAL_DECISIONS_HERE]

## Environment Variables

```bash
# Add environment variables here
```

## Related Documentation
- [API Documentation](./docs/api.md)
- [Deployment Guide](./docs/deployment.md)
"""

        return content

    def write_agents_md(self, content: str, output_path: str = "AGENTS.md"):
        """Write AGENTS.md file"""
        output_file = self.repo_path / output_path
        output_file.write_text(content)
        print(f"✓ Generated AGENTS.md at: {output_file}")
        return str(output_file)


def main():
    parser = argparse.ArgumentParser(
        description="Generate AGENTS.md file for AI coding agents"
    )
    parser.add_argument(
        "--analyze",
        action="store_true",
        help="Analyze repository and print results"
    )
    parser.add_argument(
        "--output",
        default="AGENTS.md",
        help="Output file path (default: AGENTS.md)"
    )
    parser.add_argument(
        "--repo",
        default=".",
        help="Repository path (default: current directory)"
    )

    args = parser.parse_args()

    try:
        generator = AgentsMdGenerator(args.repo)

        if args.analyze:
            # Just analyze and print
            analysis = generator.analyze_repository()
            print(json.dumps(analysis, indent=2))
        else:
            # Generate AGENTS.md
            analysis = generator.analyze_repository()
            content = generator.generate_agents_md(analysis)
            output_path = generator.write_agents_md(content, args.output)
            print(f"✓ AGENTS.md generated successfully at: {output_path}")
            print("\nNext steps:")
            print("1. Review the generated file")
            print("2. Fill in placeholders marked with [BRACKETS]")
            print("3. Add project-specific information")
            print("4. Commit to repository")

    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
