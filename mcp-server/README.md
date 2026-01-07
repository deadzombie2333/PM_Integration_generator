# PayerMax API Documentation MCP Server

An MCP (Model Context Protocol) server that provides access to PayerMax API documentation, allowing AI agents to query API formats, requirements, and sample code.

## Features

- **List Categories**: Browse all available API categories
- **Search APIs**: Search for APIs by name or keyword
- **Get Documentation**: Retrieve complete API specifications
- **Get Samples**: Access sample request/response code
- **Category Browsing**: List all APIs within a specific category

## Installation

### Prerequisites

- Python 3.10 or higher
- `uv` package manager (recommended) or `pip`

### Install with uv (Recommended)

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# The MCP server will be automatically installed when configured in Kiro
```

### Install with pip

```bash
cd mcp-server
pip install -e .
```

## Configuration

### For Kiro IDE

Add to your `.kiro/settings/mcp.json`:

```json
{
  "mcpServers": {
    "payermax-api-docs": {
      "command": "uvx",
      "args": ["--directory", "mcp-server", "fastmcp", "run", "api_docs_server.py"],
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

Or use Python directly:

```json
{
  "mcpServers": {
    "payermax-api-docs": {
      "command": "python",
      "args": ["mcp-server/api_docs_server.py"],
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

## Available Tools

### 1. `list_api_categories()`
Lists all available API categories.

**Returns**: List of category names (e.g., "付款", "收单", "多币种资金管理")

### 2. `list_apis_in_category(category: str)`
Lists all APIs in a specific category.

**Parameters**:
- `category`: Category name (e.g., "付款", "收单")

**Returns**: List of API information including name and paths

### 3. `search_apis(query: str)`
Searches for APIs by name or keyword across all categories.

**Parameters**:
- `query`: Search term (e.g., "付款", "查询", "payment")

**Returns**: List of matching APIs (max 20 results)

### 4. `get_api_documentation(category: str, api_name: str)`
Gets complete API documentation including specification and sample code.

**Parameters**:
- `category`: API category (e.g., "付款", "收单")
- `api_name`: API name (e.g., "付款查询", "交易查询")

**Returns**: Dictionary with documentation, sample code, and metadata

### 5. `get_api_sample(category: str, api_name: str)`
Gets only the sample code for a specific API (faster than full documentation).

**Parameters**:
- `category`: API category
- `api_name`: API name

**Returns**: Dictionary with sample request/response code

### 6. `get_api_spec(category: str, api_name: str)`
Gets only the API specification/documentation (without samples).

**Parameters**:
- `category`: API category
- `api_name`: API name

**Returns**: Dictionary with API specification

## Usage Examples

### Example 1: Discover Available APIs

```python
# List all categories
categories = list_api_categories()
# Returns: ["付款", "收单", "多币种资金管理", ...]

# List APIs in a category
apis = list_apis_in_category("付款")
# Returns: [{"api_name": "付款查询", "category": "付款", ...}, ...]
```

### Example 2: Search for Specific API

```python
# Search for payment-related APIs
results = search_apis("付款")
# Returns matching APIs across all categories
```

### Example 3: Get Complete API Information

```python
# Get full documentation and sample
api_info = get_api_documentation("付款", "付款查询")
# Returns: {
#   "documentation": "# 付款查询\n\n## 接口信息...",
#   "sample": "# 付款查询 API Sample\n\n## Request...",
#   "has_documentation": true,
#   "has_sample": true
# }
```

### Example 4: Quick Sample Lookup

```python
# Get just the sample code
sample = get_api_sample("收单", "交易查询")
# Returns sample request/response code only
```

## Use Cases for AI Agents

1. **Code Generation**: Agents can retrieve exact API formats and generate correct payload code
2. **API Discovery**: Agents can search and browse available APIs
3. **Documentation Lookup**: Agents can access parameter requirements and constraints
4. **Sample Code**: Agents can use real examples to generate working code
5. **Validation**: Agents can verify API usage against official specifications

## Directory Structure

```
.
├── api-docs/           # API documentation files
│   ├── 付款/
│   ├── 收单/
│   └── 多币种资金管理/
├── api-samples/        # API sample code
│   ├── 付款/
│   ├── 收单/
│   └── 多币种资金管理/
└── mcp-server/         # MCP server implementation
    ├── api_docs_server.py
    ├── pyproject.toml
    └── README.md
```

## Troubleshooting

### Server Not Starting

1. Check Python version: `python --version` (should be 3.10+)
2. Verify installation: `pip list | grep fastmcp`
3. Check file paths in configuration

### Documentation Not Found

1. Ensure `api-docs` and `api-samples` directories are in the parent directory of `mcp-server`
2. Verify file encoding is UTF-8
3. Check that markdown files have `.md` extension

### Connection Issues

1. Restart Kiro IDE
2. Check MCP server logs in Kiro's MCP panel
3. Verify the command path in `mcp.json`

## Development

To modify or extend the server:

1. Edit `api_docs_server.py`
2. Add new tools using the `@mcp.tool()` decorator
3. Test locally: `python api_docs_server.py`
4. Restart the MCP server in Kiro

## License

This MCP server is part of the PayerMax API documentation project.
