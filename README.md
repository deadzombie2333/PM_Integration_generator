# PayerMax API Code Generator

A Kiro Power that generates production-ready PayerMax API integration code with correct payloads, request formats, and error handling.

## 🚀 Features

- **Accurate Code Generation**: Uses official PayerMax API specifications
- **Multi-Language Support**: Python, Node.js, Java, PHP, Go, Ruby, C#, and more
- **Complete Integration**: Includes request signing, error handling, and response parsing
- **API Discovery**: Search and browse available PayerMax APIs
- **Sample-Based**: Leverages real API samples for working code
- **Type-Safe**: Generates code with proper type hints and validation

## 📋 Prerequisites

- Python 3.10 or higher
- Kiro IDE
- Git (for cloning)

## 🔧 Quick Start

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd PM_Integration_generator
```

### 2. Set Up Virtual Environment

```bash
# Create virtual environment inside mcp-server directory
python3 -m venv mcp-server/venv

# Activate it
source mcp-server/venv/bin/activate  # macOS/Linux
# or
mcp-server\venv\Scripts\activate     # Windows

# Install dependencies
pip install -r mcp-server/requirements.txt

# Verify installation
pip list | grep fastmcp
```

### 3. Configure Kiro

**Get your workspace absolute path:**
```bash
pwd
# Example: /Users/yourname/Documents/python/Github/PM_Integration_generator
```

**Create or edit `.kiro/settings/mcp.json`** (replace `YOUR_ABSOLUTE_PATH`):

**macOS/Linux:**
```json
{
  "mcpServers": {
    "payermax-api-docs": {
      "command": "YOUR_ABSOLUTE_PATH/mcp-server/venv/bin/python",
      "args": ["YOUR_ABSOLUTE_PATH/mcp-server/api_docs_server.py"],
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

**Windows:**
```json
{
  "mcpServers": {
    "payermax-api-docs": {
      "command": "C:\\YOUR\\ABSOLUTE\\PATH\\mcp-server\\venv\\Scripts\\python.exe",
      "args": ["C:\\YOUR\\ABSOLUTE\\PATH\\mcp-server\\api_docs_server.py"],
      "disabled": false
    }
  }
}
```

### 4. Start Using

Open Kiro IDE and try:
- "List all API categories"
- "Generate Python code for 付款查询"
- "Show me the 交易查询 API documentation"

## 📚 Available APIs

The power provides access to all PayerMax APIs including:

- **付款 (Payment)**: Payment queries, payment applications, validation
- **收单 (Acquiring)**: Transactions, refunds, payment confirmation
- **多币种资金管理 (Multi-Currency)**: Balance queries, exchange rates, forex
- **收单:Auth-Capture**: Authorization and capture flows
- **收单:Tokenization**: Token-based payments
- **收单:争议 (Disputes)**: Dispute management
- **风控 (Risk Control)**: Risk management APIs

## 💡 Usage Examples

### Example 1: Generate Python Client

```
User: "Generate Python code for 付款查询 API"
```

The agent will:
1. Retrieve official API specification
2. Generate complete Python client with:
   - Request payload structure
   - Signature generation
   - Error handling
   - Type hints and validation
   - Usage examples

### Example 2: Multi-Language Support

```
User: "Create a Node.js client for payment order query"
```

Generates Node.js/TypeScript code with async/await patterns.

### Example 3: Quick Testing

```
User: "Generate a curl command to test 交易查询"
```

Provides ready-to-use curl command with sample data.

### Example 4: Complete Integration

```
User: "Create a complete API integration module for all 收单 APIs"
```

Generates a full module with all acquiring APIs.

## 🛠️ MCP Server Tools

The power uses these MCP tools:

- `list_api_categories()` - List all API categories
- `list_apis_in_category(category)` - List APIs in a category
- `search_apis(query)` - Search APIs by keyword
- `get_api_documentation(category, api_name)` - Get full API spec
- `get_api_sample(category, api_name)` - Get sample code
- `get_api_spec(category, api_name)` - Get specification only

## 📁 Project Structure

```
PM_Integration_generator/
├── mcp-server/            # MCP server implementation
│   ├── api-docs/          # Official API documentation
│   │   ├── 付款/
│   │   ├── 收单/
│   │   └── 多币种资金管理/
│   ├── api-samples/       # API sample requests/responses
│   │   ├── 付款/
│   │   ├── 收单/
│   │   └── 多币种资金管理/
│   ├── venv/              # Virtual environment (created by user)
│   ├── api_docs_server.py
│   ├── requirements.txt
│   └── README.md
├── powers/                # Kiro Power definition
│   └── payermax-codegen/
│       ├── POWER.md
│       ├── power.json
│       └── getting-started.md
└── .kiro/                 # Kiro configuration
    └── settings/
        └── mcp.json
```

## 🔍 How It Works

1. **User Request**: User asks to generate code for a specific API
2. **API Discovery**: Agent searches/browses available APIs
3. **Spec Retrieval**: Agent fetches official API documentation via MCP
4. **Code Generation**: Agent generates code based on exact specifications
5. **Validation**: Generated code includes parameter validation and constraints
6. **Error Handling**: Complete error handling for all response codes

## 🐛 Troubleshooting

### MCP Server Not Starting

```bash
# Test manually
source mcp-server/venv/bin/activate
python mcp-server/api_docs_server.py

# Check Python version
python --version  # Should be 3.10+

# Verify installation
pip list | grep fastmcp

# Install if missing
mcp-server/venv/bin/pip install fastmcp
```

### Error: "spawn ... ENOENT"

This means Kiro cannot find the Python executable. **You must use absolute paths**:

1. Run `pwd` in your project directory
2. Update `.kiro/settings/mcp.json` with the full absolute path
3. Example: `/Users/yourname/Documents/python/Github/PM_Integration_generator/mcp-server/venv/bin/python`

### Tools Not Available

1. Restart Kiro IDE
2. Check MCP panel for errors
3. Verify absolute paths in `mcp.json`
4. Ensure fastmcp is installed in the venv

### Permission Errors

```bash
# Make script executable (macOS/Linux)
chmod +x mcp-server/api_docs_server.py
```

## 📖 Documentation

- [Setup Guide](SETUP.md) - Detailed installation instructions
- [MCP Server README](mcp-server/README.md) - MCP server documentation
- [Power Documentation](powers/payermax-codegen/POWER.md) - Power usage guide
- [Getting Started](powers/payermax-codegen/getting-started.md) - Workflow guide

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📦 Distribution

### For Teams

Share the repository URL and have team members:
1. Clone the repo
2. Run setup script
3. Configure Kiro

### For Public

1. Push to GitHub
2. Add clear README and SETUP.md
3. Tag releases with semantic versioning
4. Provide example usage

### As PyPI Package

```bash
pip install build
python -m build
twine upload dist/*
```

## 🔐 Security

- Never commit API credentials
- Use environment variables for sensitive data
- Review generated code before using in production
- Keep dependencies updated

## 📄 License

[Add your license here - MIT, Apache 2.0, etc.]

## 🙋 Support

- GitHub Issues: [your-repo-url]/issues
- Documentation: [your-docs-url]
- Email: [your-email]

## 🎯 Roadmap

- [ ] Add more language templates
- [ ] Support for webhook generation
- [ ] Batch operation utilities
- [ ] Testing framework integration
- [ ] CI/CD pipeline examples
- [ ] Docker support

## ⭐ Acknowledgments

Built for PayerMax API integration using:
- [Kiro IDE](https://kiro.dev)
- [FastMCP](https://github.com/jlowin/fastmcp)
- PayerMax Official API Documentation

---

Made with ❤️ for PayerMax developers
