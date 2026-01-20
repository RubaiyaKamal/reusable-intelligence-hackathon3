#!/usr/bin/env python3
"""
Generate API Documentation from OpenAPI Specification

Converts OpenAPI/Swagger specs to Docusaurus markdown documentation.
"""

import sys
import json
import yaml
import argparse
from pathlib import Path
from typing import Dict, Any


class APIDocsGenerator:
    """Generates API documentation from OpenAPI specs"""

    def __init__(self, spec_file: str, output_dir: str):
        self.spec_file = Path(spec_file)
        self.output_dir = Path(output_dir)
        self.spec = None

    def load_spec(self):
        """Load OpenAPI specification"""
        print(f"📖 Loading OpenAPI spec: {self.spec_file}")

        try:
            with open(self.spec_file, 'r') as f:
                if self.spec_file.suffix in ['.yaml', '.yml']:
                    self.spec = yaml.safe_load(f)
                else:
                    self.spec = json.load(f)

            print(f"✓ Loaded {self.spec.get('info', {}).get('title', 'API')} v{self.spec.get('info', {}).get('version', '1.0')}")
            return True

        except Exception as e:
            print(f"✗ Failed to load spec: {e}")
            return False

    def generate_overview(self):
        """Generate API overview page"""
        info = self.spec.get('info', {})
        servers = self.spec.get('servers', [])

        content = f"""---
sidebar_position: 1
title: {info.get('title', 'API Documentation')}
---

# {info.get('title', 'API Documentation')}

{info.get('description', '')}

## Version

**Current Version:** {info.get('version', '1.0.0')}

## Base URLs

"""

        for server in servers:
            content += f"- `{server.get('url')}` - {server.get('description', 'API Server')}\n"

        content += """
## Authentication

"""

        # Add security schemes
        security_schemes = self.spec.get('components', {}).get('securitySchemes', {})
        if security_schemes:
            for name, scheme in security_schemes.items():
                scheme_type = scheme.get('type')
                content += f"### {name}\n\n"
                content += f"**Type:** {scheme_type}\n\n"

                if scheme_type == 'http':
                    content += f"**Scheme:** {scheme.get('scheme')}\n\n"
                elif scheme_type == 'apiKey':
                    content += f"**Location:** {scheme.get('in')}\n"
                    content += f"**Parameter:** {scheme.get('name')}\n\n"

                content += f"{scheme.get('description', '')}\n\n"

        content += """
## Endpoints

"""

        # List all endpoints
        paths = self.spec.get('paths', {})
        for path, operations in paths.items():
            for method, operation in operations.items():
                if method.upper() in ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']:
                    summary = operation.get('summary', path)
                    tag = operation.get('tags', ['General'])[0]
                    content += f"- [{method.upper()} {path}](./{tag.lower()}.md#{self._make_anchor(method, path)}) - {summary}\n"

        # Write overview
        output_file = self.output_dir / "overview.md"
        output_file.write_text(content)
        print(f"✓ Generated {output_file}")

    def generate_endpoint_docs(self):
        """Generate documentation for each endpoint"""
        paths = self.spec.get('paths', {})

        # Group by tags
        endpoints_by_tag = {}
        for path, operations in paths.items():
            for method, operation in operations.items():
                if method.upper() not in ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']:
                    continue

                tags = operation.get('tags', ['General'])
                for tag in tags:
                    if tag not in endpoints_by_tag:
                        endpoints_by_tag[tag] = []

                    endpoints_by_tag[tag].append({
                        'path': path,
                        'method': method.upper(),
                        'operation': operation
                    })

        # Generate a file for each tag
        for tag, endpoints in endpoints_by_tag.items():
            content = self._generate_tag_page(tag, endpoints)
            output_file = self.output_dir / f"{tag.lower()}.md"
            output_file.write_text(content)
            print(f"✓ Generated {output_file}")

    def _generate_tag_page(self, tag: str, endpoints: list) -> str:
        """Generate markdown for a tag's endpoints"""
        content = f"""---
sidebar_position: 2
title: {tag} API
---

# {tag} API

"""

        for endpoint in endpoints:
            path = endpoint['path']
            method = endpoint['method']
            operation = endpoint['operation']

            # Endpoint header
            content += f"""
## {method} {path}}

<span id="{self._make_anchor(method, path)}"></span>

{operation.get('summary', '')}

{operation.get('description', '')}

"""

            # Parameters
            parameters = operation.get('parameters', [])
            if parameters:
                content += """
### Parameters

| Name | Location | Type | Required | Description |
|------|----------|------|----------|-------------|
"""
                for param in parameters:
                    name = param.get('name')
                    location = param.get('in')
                    param_type = param.get('schema', {}).get('type', 'string')
                    required = '✓' if param.get('required') else ''
                    description = param.get('description', '')
                    content += f"| {name} | {location} | {param_type} | {required} | {description} |\n"

                content += "\n"

            # Request body
            request_body = operation.get('requestBody')
            if request_body:
                content += """
### Request Body

"""
                content_types = request_body.get('content', {})
                for content_type, schema_info in content_types.items():
                    content += f"**Content-Type:** `{content_type}`\n\n"

                    schema = schema_info.get('schema', {})
                    if '$ref' in schema:
                        schema_name = schema['$ref'].split('/')[-1]
                        content += f"**Schema:** [{schema_name}](#schemas)\n\n"
                    else:
                        content += "```json\n"
                        content += json.dumps(self._example_from_schema(schema), indent=2)
                        content += "\n```\n\n"

            # Responses
            responses = operation.get('responses', {})
            if responses:
                content += """
### Responses

"""
                for status_code, response in responses.items():
                    description = response.get('description', '')
                    content += f"**{status_code}** - {description}\n\n"

                    response_content = response.get('content', {})
                    for content_type, schema_info in response_content.items():
                        schema = schema_info.get('schema', {})
                        content += "```json\n"
                        content += json.dumps(self._example_from_schema(schema), indent=2)
                        content += "\n```\n\n"

            # Example
            content += f"""
### Example

```bash
curl -X {method} \\
  https://api.learnflow.com{path} \\
  -H 'Authorization: Bearer YOUR_TOKEN' \\
  -H 'Content-Type: application/json'
```

---

"""

        return content

    def _example_from_schema(self, schema: Dict[str, Any]) -> Dict[str, Any]:
        """Generate example JSON from schema"""
        if '$ref' in schema:
            return {"$ref": schema['$ref']}

        schema_type = schema.get('type')

        if schema_type == 'object':
            properties = schema.get('properties', {})
            example = {}
            for prop_name, prop_schema in properties.items():
                example[prop_name] = self._example_value(prop_schema)
            return example

        elif schema_type == 'array':
            items = schema.get('items', {})
            return [self._example_from_schema(items)]

        else:
            return self._example_value(schema)

    def _example_value(self, schema: Dict[str, Any]) -> Any:
        """Generate example value for a schema"""
        if 'example' in schema:
            return schema['example']

        schema_type = schema.get('type', 'string')

        type_examples = {
            'string': 'string',
            'integer': 0,
            'number': 0.0,
            'boolean': True,
            'array': [],
            'object': {}
        }

        return type_examples.get(schema_type, 'value')

    def _make_anchor(self, method: str, path: str) -> str:
        """Create anchor ID from method and path"""
        return f"{method.lower()}-{path.replace('/', '-').replace('{', '').replace('}', '').strip('-')}"

    def generate(self):
        """Generate all documentation"""
        print("🚀 Generating API documentation...")
        print()

        if not self.load_spec():
            return False

        # Create output directory
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Generate docs
        self.generate_overview()
        self.generate_endpoint_docs()

        print()
        print("✓ API documentation generated successfully!")
        print(f"  Output: {self.output_dir}")
        print()
        print("Next steps:")
        print("  1. Review generated markdown files")
        print("  2. npm run build")
        print("  3. Deploy documentation")

        return True


def main():
    parser = argparse.ArgumentParser(
        description="Generate API documentation from OpenAPI spec"
    )
    parser.add_argument(
        "--spec",
        required=True,
        help="Path to OpenAPI specification file (YAML or JSON)"
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Output directory for generated docs"
    )

    args = parser.parse_args()

    try:
        generator = APIDocsGenerator(args.spec, args.output)
        success = generator.generate()
        sys.exit(0 if success else 1)

    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
