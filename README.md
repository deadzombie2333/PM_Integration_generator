# PayerMax API Code Generator

A Kiro Power that generates production-ready PayerMax API integration code with correct payloads, request formats, and error handling.

## What is This?

A specialized AI capability for Kiro IDE that generates intelligent PayerMax API integration code. The AI agent accesses official PayerMax documentation through an MCP gateway to create complete, working code based on your requirements.

**How it works:**
1. Describe what you want to build
2. Agent discovers relevant APIs and creates an integration plan
3. Configure through interactive questions
4. Get production-ready code immediately

## Features

- Multi-language support (Python, Node.js, Java, PHP, Go, Ruby, C#)
- Complete integration with request signing and error handling
- Intelligent API discovery using semantic search
- Interactive guided workflow
- Separate files per endpoint with proper structure

## Prerequisites

- Kiro IDE
- PayerMax MCP Gateway credentials (contact PayerMax developer team)

## Quick Start

### 1. Install the Power

Open Kiro IDE → Command Palette (Cmd/Ctrl + Shift + P) → **"Powers: Add Custom Power"**

Provide the path to this power or GitHub URL.

### 2. Get MCP Credentials

Contact PayerMax developer team for:
- **MCP Gateway URL**
- **Bearer Token** (temporary, expires after a few hours)

Include: Your name, company, and use case.

### 3. Configure MCP

Create `.kiro/settings/mcp.json`:

```json
{
  "mcpServers": {
    "payermax-api-docs": {
      "url": "YOUR_MCP_GATEWAY_URL",
      "headers": {
        "Authorization": "Bearer YOUR_BEARER_TOKEN"
      },
      "disabled": false,
      "autoApprove": [
        "get_integration_recommendation",
        "find_api_endpoint",
        "search_integration_guides",
        "search_api_documentation"
      ]
    }
  }
}
```

### 4. Verify & Use

- Restart Kiro IDE
- Check MCP panel: `payermax-api-docs` should be connected
- Try: "I want to integrate PayerMax payment APIs"

## What Can You Build?

- Payment creation (Cashier, API, Drop-in modes)
- Payment queries and status checks
- Refunds and payouts
- Multi-currency operations
- Tokenization
- Dispute management
- Risk control

## Usage Examples

**Example 1:**
```
"I want to integrate PayerMax payment APIs"
```
Agent guides you through language selection, requirements analysis, and generates complete integration code.

**Example 2:**
```
"I need to check payment status for my orders"
```
Agent generates code with proper request signing and error handling.

**Example 3:**
```
"Build a complete payment system with creation, query, and refund"
```
Agent creates separate files for each endpoint with shared utilities.

## MCP Tools

The power uses these tools from the `payermax-api-docs` MCP server:

- **find_api_endpoint()** - Finds API specs using LLM and semantic search
- **get_integration_recommendation()** - Analyzes requirements and recommends integration method
- **search_api_documentation()** - Semantic search of API docs
- **search_integration_guides()** - Search integration guides

## Troubleshooting

### MCP Server Not Connecting
- Verify URL and token are correct (no extra spaces)
- Check token hasn't expired (request new one)
- Restart Kiro or reconnect from MCP panel
- Check MCP panel for error messages

### Authorization Errors (401/403)
- Token expired - request new one
- Verify `Authorization: Bearer YOUR_TOKEN` format

### Tools Not Available
- Check MCP panel shows server as connected
- Ensure `disabled: false` in mcp.json
- Restart Kiro IDE

## Documentation

- [Power Documentation](powers/payermax-codegen/POWER.md)
- [Getting Started Guide](powers/payermax-codegen/steering/getting-started.md)

## Security

- Never commit credentials to version control
- Tokens are temporary and expire
- Review generated code before production use

## Distribution

**For Teams:**
1. Share this repository
2. Each member requests their own MCP credentials
3. Configure mcp.json with credentials
4. Start using in Kiro

---

Built for PayerMax developers using [Kiro IDE](https://kiro.dev)
