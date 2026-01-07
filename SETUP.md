# PayerMax API Code Generator - Setup Guide

This guide helps users install and configure the PayerMax API Code Generator power and MCP server.

## For End Users

### Prerequisites

- Python 3.10 or higher
- Kiro IDE installed
- Git (to clone the repository)

### Installation Steps

#### 1. Clone or Download the Repository

```bash
# Clone the repository
git clone <your-repo-url>
cd PM_Integration_generator

# Or download and extract the ZIP file
```

#### 2. Set Up Python Virtual Environment

**IMPORTANT**: The virtual environment must be created inside the `mcp-server` directory.

```bash
# Navigate to project root
cd PM_Integration_generator

# Create virtual environment inside mcp-server
python3 -m venv mcp-server/venv

# Activate virtual environment
# On macOS/Linux:
source mcp-server/venv/bin/activate

# On Windows:
mcp-server\venv\Scripts\activate

# Install dependencies
pip install -r mcp-server/requirements.txt

# Verify fastmcp is installed
pip list | grep fastmcp
```

#### 3. Configure MCP Server in Kiro

**IMPORTANT**: Kiro requires **absolute paths** for MCP server configuration.

**Step 1: Get your workspace absolute path**

```bash
# In your terminal, navigate to the project directory
cd PM_Integration_generator

# Get the absolute path
pwd
# Example output: /Users/yourname/Documents/python/Github/PM_Integration_generator
```

**Step 2: Configure MCP in Kiro**

Create or edit `.kiro/settings/mcp.json` in your workspace and replace `YOUR_ABSOLUTE_PATH` with the path from Step 1:

**For macOS/Linux:**
```json
{
  "mcpServers": {
    "payermax-api-docs": {
      "command": "YOUR_ABSOLUTE_PATH/mcp-server/venv/bin/python",
      "args": ["YOUR_ABSOLUTE_PATH/mcp-server/api_docs_server.py"],
      "disabled": false,
      "autoApprove": [],
      "env": {
        "PYTHONIOENCODING": "utf-8"
      }
    }
  }
}
```

**Example (macOS/Linux):**
```json
{
  "mcpServers": {
    "payermax-api-docs": {
      "command": "/Users/jwgan/Documents/python/Github/PM_Integration_generator/mcp-server/venv/bin/python",
      "args": ["/Users/jwgan/Documents/python/Github/PM_Integration_generator/mcp-server/api_docs_server.py"],
      "disabled": false,
      "autoApprove": [],
      "env": {
        "PYTHONIOENCODING": "utf-8"
      }
    }
  }
}
```

**For Windows:**
```json
{
  "mcpServers": {
    "payermax-api-docs": {
      "command": "C:\\Users\\YourName\\Documents\\PM_Integration_generator\\mcp-server\\venv\\Scripts\\python.exe",
      "args": ["C:\\Users\\YourName\\Documents\\PM_Integration_generator\\mcp-server\\api_docs_server.py"],
      "disabled": false,
      "autoApprove": [],
      "env": {
        "PYTHONIOENCODING": "utf-8"
      }
    }
  }
}
```

**Note**: Replace backslashes with double backslashes (`\\`) in Windows paths.

#### 4. Verify Installation

1. Open Kiro IDE
2. Open the workspace folder
3. Click the Kiro icon in the sidebar
4. Look for "MCP Servers" section
5. You should see "payermax-api-docs" with status "running"
6. It should show 6 available tools

#### 5. Test the Power

In Kiro chat, try:
- "List all API categories"
- "Generate Python code for 付款查询"
- "Show me payment APIs"

### Troubleshooting

**MCP Server not starting:**
```bash
# Test the server manually
source mcp-server/venv/bin/activate
python mcp-server/api_docs_server.py

# Check Python version
python --version  # Should be 3.10+

# Verify fastmcp installation
pip list | grep fastmcp

# If fastmcp is missing, install it:
mcp-server/venv/bin/pip install fastmcp
```

**Error: "spawn ... ENOENT" or "No such file or directory":**
- This means Kiro cannot find the Python executable
- Make sure you're using **absolute paths** in mcp.json
- Run `pwd` in your project directory to get the correct path
- Update both `command` and `args` with full absolute paths

**Tools not available:**
1. Restart Kiro IDE
2. Check MCP panel for error messages
3. Verify file paths in mcp.json are correct
4. Ensure venv is activated and fastmcp is installed

**Permission errors:**
```bash
# Make script executable (macOS/Linux)
chmod +x mcp-server/api_docs_server.py
```

## For Power Distribution

### Method 1: GitHub Repository (Recommended)

1. **Push to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit: PayerMax API Code Generator"
   git remote add origin <your-repo-url>
   git push -u origin main
   ```

2. **Users install via:**
   ```bash
   git clone <your-repo-url>
   cd PM_Integration_generator
   python3 -m venv venv
   source venv/bin/activate
   pip install -r mcp-server/requirements.txt
   ```

3. **Add to README.md:**
   - Installation instructions
   - Configuration steps
   - Usage examples

### Method 2: PyPI Package (Advanced)

Package the MCP server as a Python package:

1. **Update pyproject.toml** (already created)
2. **Build and publish:**
   ```bash
   pip install build twine
   python -m build
   twine upload dist/*
   ```

3. **Users install via:**
   ```bash
   pip install payermax-api-docs-mcp
   ```

4. **Update mcp.json:**
   ```json
   {
     "mcpServers": {
       "payermax-api-docs": {
         "command": "uvx",
         "args": ["payermax-api-docs-mcp"],
         "disabled": false
       }
     }
   }
   ```

### Method 3: Kiro Power Registry (Future)

When Kiro supports power registry:
1. Package the power with metadata
2. Submit to Kiro power registry
3. Users install via Kiro UI

### Method 4: ZIP Distribution

1. **Create distribution package:**
   ```bash
   # Exclude unnecessary files
   zip -r payermax-codegen-power.zip \
     mcp-server/ \
     powers/ \
     api-docs/ \
     api-samples/ \
     .kiro/ \
     SETUP.md \
     README.md \
     -x "*.pyc" "*__pycache__*" "*.git*" "*venv*"
   ```

2. **Users install:**
   - Extract ZIP to their workspace
   - Follow SETUP.md instructions
   - Configure mcp.json

## Directory Structure for Distribution

```
PM_Integration_generator/
├── mcp-server/            # MCP server (required)
│   ├── api-docs/          # API documentation (required)
│   ├── api-samples/       # API samples (required)
│   ├── venv/              # Virtual environment (created by user)
│   ├── api_docs_server.py
│   ├── pyproject.toml
│   ├── requirements.txt
│   └── README.md
├── powers/                # Power definition (required)
│   └── payermax-codegen/
│       ├── POWER.md
│       ├── power.json
│       └── getting-started.md
├── .kiro/                 # Kiro configuration (template)
│   └── settings/
│       └── mcp.json
├── SETUP.md              # This file
├── README.md             # Project overview
└── .gitignore            # Git ignore file
```

## Configuration Templates

### For Team Sharing (Same Organization)

**IMPORTANT**: Each team member must configure their own absolute paths.

**Setup script for team members:**

Create a `setup.sh` script (macOS/Linux):
```bash
#!/bin/bash
# Get absolute path
WORKSPACE_PATH=$(pwd)

# Create venv and install dependencies
python3 -m venv mcp-server/venv
source mcp-server/venv/bin/activate
pip install -r mcp-server/requirements.txt

# Create MCP config with absolute paths
mkdir -p .kiro/settings
cat > .kiro/settings/mcp.json << EOF
{
  "mcpServers": {
    "payermax-api-docs": {
      "command": "${WORKSPACE_PATH}/mcp-server/venv/bin/python",
      "args": ["${WORKSPACE_PATH}/mcp-server/api_docs_server.py"],
      "disabled": false,
      "autoApprove": [],
      "env": {
        "PYTHONIOENCODING": "utf-8"
      }
    }
  }
}
EOF

echo "Setup complete! Restart Kiro IDE to use the MCP server."
```

Team members:
1. Clone the repo
2. Run `chmod +x setup.sh && ./setup.sh`
3. Restart Kiro IDE

### For Public Distribution

Include in README.md:
- Clear installation steps
- Prerequisites
- Configuration examples for different OS
- Troubleshooting guide
- Usage examples

## Maintenance

### Updating the Power

Users can update by:
```bash
git pull origin main
pip install -r mcp-server/requirements.txt --upgrade
```

Then restart Kiro IDE.

### Version Management

Use semantic versioning in `power.json`:
- Major: Breaking changes
- Minor: New features
- Patch: Bug fixes

## Support

Provide support channels:
- GitHub Issues
- Documentation wiki
- Example repository
- Video tutorials

## License

Include appropriate license file (MIT, Apache, etc.)
