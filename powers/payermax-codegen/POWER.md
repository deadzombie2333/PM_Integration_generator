---
name: payermax-codegen
displayName: PayerMax API Code Generator
version: 1.0.0
description: Generate PayerMax API integration code with correct payloads and request formats using official documentation
keywords:
  - api
  - code generation
  - payermax
  - payment
  - integration
  - client
  - sdk
  - rest api
  - http
  - request
  - payload
  - codegen
mcpServers:
  - payermax-api-docs
---

# PayerMax API Code Generator

A Kiro Power for generating PayerMax API integration code with correct payloads, request formats, and error handling.

## Overview

This power enables AI agents to generate production-ready API integration code for PayerMax APIs. It uses the PayerMax API Documentation MCP server to access official API specifications and samples, ensuring generated code matches the exact requirements.

## Features

- **Accurate Code Generation**: Uses official API specs to generate correct payloads
- **Multiple Languages**: Supports Python, Node.js, Java, PHP, Go, and more
- **Complete Integration**: Generates request signing, error handling, and response parsing
- **Sample-Based**: Leverages real API samples for working code
- **Discovery**: Search and browse available APIs before generating code

## Use Cases

1. **Quick Integration**: Generate API client code for any PayerMax API
2. **Payload Creation**: Create correctly formatted request payloads
3. **Testing**: Generate test scripts with sample data
4. **Documentation**: Create code examples for internal documentation
5. **Migration**: Convert between programming languages

## Available Tools

This power uses the `payermax-api-docs` MCP server with the following tools:

### Discovery Tools

- `list_api_categories()` - List all API categories
- `list_apis_in_category(category)` - List APIs in a category
- `search_apis(query)` - Search for APIs by keyword

### Documentation Tools

- `get_api_documentation(category, api_name)` - Get full API spec and sample
- `get_api_sample(category, api_name)` - Get sample code only
- `get_api_spec(category, api_name)` - Get specification only

## How to Use

### Basic Workflow

1. **Describe Use Case**: Agent asks you to briefly describe what you want to build
2. **Discover APIs**: Agent searches or browses available APIs based on your description
3. **Retrieve Spec**: Agent gets the API documentation and samples
4. **Interactive Configuration**: Agent presents selections to gather:
   - Target programming language
   - API credentials requirements (placeholder vs actual)
   - Code style preferences (class-based, functional, etc.)
   - Additional features (logging, retry logic, etc.)
5. **Generate Code**: Create integration code based on your selections
6. **Customize**: Adapt the code to your specific needs

### Interactive Code Generation

When you request code generation, the agent will follow this **three-step process**:

#### Step 1: Select Interaction Language (FIRST - REQUIRED)

**Agent MUST FIRST ask**: "Which language would you like to use for our conversation?"

**Options**:
- **Chinese (中文)**
- **English**

**After user selects**:
- Agent remembers the selected language
- ALL subsequent interactions use ONLY that language
- Tool descriptions, questions, and responses are in the selected language

#### Step 2: Gather Use Case (SECOND - REQUIRED)

**Agent asks** (in selected language): "Please briefly describe what you want to build with PayerMax APIs"

**Examples**:
- English: "I need to query payment status for my e-commerce platform"
- Chinese: "我需要为我的电商平台查询支付状态"

Based on this description, the agent will identify relevant APIs.

#### Step 3: Interactive Configuration (THIRD - AFTER USE CASE)

**IMPORTANT**: Before asking any question, check if the user already provided that information in Step 2 (use case description). If they did, skip that question and use their provided value.

**Then, ask configuration questions ONE AT A TIME** (in selected language), waiting for user response before proceeding to next question:

1. **Programming Language** - Ask: "Which programming language would you like to use?"
   - **SKIP IF**: User mentioned language in use case (e.g., "I need Python code for...")
   - Options: 1) Python, 2) Node.js, 3) Java, 4) PHP, 5) Go, 6) Ruby, 7) C#, 8) Shell
   - User enters: **1-8**
   - Wait for response

2. **Code Structure** - Ask: "What code structure do you prefer?"
   - **SKIP IF**: User specified structure (e.g., "I need a class-based client...")
   - Options: 1) Class-based client, 2) Standalone function, 3) Complete module, 4) Code snippet only
   - User enters: **1-4**
   - Wait for response

3. **Credential Handling** - Ask: "How should API credentials be handled?"
   - **SKIP IF**: User mentioned credentials (e.g., "use environment variables...")
   - Options: 1) Use placeholders, 2) Provide actual credentials, 3) Use environment variables
   - User enters: **1-3**
   - Wait for response

4. **Features to Include** - Ask: "Which features would you like to include? (comma-separated for multiple, e.g., 1,2,4)"
   - **SKIP IF**: User specified features (e.g., "with error handling and logging...")
   - Options: 1) Error handling, 2) Logging, 3) Validation, 4) Type hints, 5) Examples, 6) Unit tests
   - User enters: **1-6 (comma-separated for multiple)**
   - Wait for response

5. **Target Environment** - Ask: "Which environment will you use?"
   - **SKIP IF**: User mentioned environment (e.g., "for production..." or "for testing...")
   - Options: 1) UAT (testing), 2) Production
   - User enters: **1-2**
   - Wait for response

6. **Custom Requirements** - Ask: "Do you have any special requirements? (Enter text or 'no' to skip)"
   - **SKIP IF**: User already provided special requirements in use case
   - User enters: **Text description or "no"**
   - Wait for response

**CRITICAL**: 
- Ask questions sequentially, ONE AT A TIME
- Do NOT present all questions at once
- Always provide numbered options
- **SKIP any question if user already provided that information in Step 2**

#### Step 4: Collect Required API Parameters (FOURTH - AFTER CONFIGURATION)

**After configuration is complete**:

1. **Retrieve API Documentation**: Call `get_api_documentation(category, api_name)` to get the full API specification

2. **Identify Required Fields**: Parse the API spec to find all required parameters (marked as "必填" or "Required")

3. **Check User's Use Case Description**: Review Step 2 to see if user already provided values for any required parameters

4. **Ask for Parameter Values ONE AT A TIME** (in selected language):
   - **SKIP IF**: User already provided this parameter value in Step 2 use case description
   - For each required parameter not yet provided, ask: "Please provide value for [parameter_name]: [description]"
   - Show parameter constraints (max length, format, etc.)
   - Example: "Please provide value for 'outTradeNo' (Merchant order number, max 63 characters):"
   - User enters the value
   - Wait for response, then proceed to next parameter

5. **Skip Common Parameters**: Do NOT ask for these (use placeholders or config):
   - appId (from configuration)
   - merchantNo (from configuration)
   - requestTime (auto-generated)
   - version (use default)
   - keyVersion (use default)

6. **Validate Input**: Check if provided values meet constraints (length, format, etc.)

**CRITICAL**: Always check Step 2 use case description first. Do NOT ask for parameters that user already provided.

#### Step 5: Generate and Review Code (FIFTH - FINAL STEP)

**After all parameters are collected**:

1. **Generate Code**: Create the integration code with:
   - All user-provided parameter values
   - Selected configuration options
   - Proper error handling and features

2. **Self-Review Code** (CRITICAL - BEFORE DELIVERY):
   - Read through the generated code line by line
   - Check for syntax errors
   - Verify all required parameters are included
   - Ensure signature generation is correct
   - Validate endpoint URLs match the environment
   - Confirm error handling is complete
   - Check that the code can run as-is without modifications

3. **Fix Any Issues**: If errors found, correct them immediately

4. **Deliver Final Code**: Present the reviewed, production-ready code to user

**CRITICAL**: The code MUST be ready to use immediately without any modifications. Always perform self-review before delivery.

### Example Prompts

- "I want to integrate PayerMax payment APIs" (agent will ask for use case details)
- "Help me generate code for PayerMax" (agent will ask what you want to build)
- "I need to query payment status" (agent will ask for more context, then present selections)
- "Create a payment integration" (agent will ask about your specific needs first)

## Code Generation Guidelines

When generating code, the agent will:

1. **Gather Requirements Interactively**: Ask user for language, style, and features through Kiro selections
2. **Retrieve Official Specs**: Use MCP tools to get exact API requirements
3. **Include All Required Fields**: Ensure all mandatory parameters are present
4. **Add Validation**: Include parameter validation and constraints
5. **Handle Errors**: Implement proper error handling
6. **Add Comments**: Document the code with parameter descriptions
7. **Use Samples**: Base code on official sample requests/responses
8. **Include Signing**: Add signature generation logic where needed

### Required User Input

Before generating code, the agent **must** follow this three-step process:

#### Step 1: Select Interaction Language (Required First)

Agent asks: **"Which language would you like to use for our conversation? / 您希望使用哪种语言进行交流？"**

Options:
1. **English**
2. **Chinese (中文)**

User enters: **1 or 2**

**CRITICAL**: This selection determines the language for ALL subsequent interactions.

#### Step 2: Gather Use Case (Required Second)

Agent asks (in selected language): **"Please briefly describe what you want to build with PayerMax APIs"**

Examples of user responses:
- English: "I need to query payment status for my e-commerce platform"
- English: "I want to create a payout system for my marketplace"
- Chinese: "我需要为我的电商平台查询支付状态"
- Chinese: "我想为我的市场创建一个支付系统"

Based on this description, the agent will identify relevant APIs.

#### Step 3: Interactive Configuration (After Use Case)

Then the agent presents **clear selection options** in Kiro's interface:

1. **Target Language** (required)
   - Options: Python, Node.js, Java, PHP, Go, Ruby, C#, Shell/curl
   
2. **Code Structure** (required)
   - Options: Class-based client, Standalone function, Complete module, Code snippet only
   
3. **Credential Handling** (required)
   - Options: Use placeholders (recommended), Provide actual credentials, Use environment variables
   
4. **Additional Features** (optional, multi-select)
   - Error handling and retry logic
   - Request/response logging
   - Parameter validation
   - Type hints/annotations
   - Usage examples
   - Unit test template
   
5. **Environment** (required)
   - Options: UAT (testing), Production
   
6. **Custom Requirements** (optional, text input)
   - Any specific requirements or preferences

## Supported Languages

- **Python**: Using `requests` library
- **Node.js**: Using `axios` or `fetch`
- **Java**: Using `HttpClient` or `OkHttp`
- **PHP**: Using `cURL` or `Guzzle`
- **Go**: Using `net/http`
- **Ruby**: Using `net/http` or `httparty`
- **C#**: Using `HttpClient`
- **Shell**: Using `curl`

## Prerequisites

- PayerMax API Documentation MCP server must be installed and running
- API credentials (appId, merchantNo, signing keys) from PayerMax

## Configuration

This power requires the `payermax-api-docs` MCP server. Ensure it's configured in your `.kiro/settings/mcp.json`:

```json
{
  "mcpServers": {
    "payermax-api-docs": {
      "command": "python",
      "args": ["mcp-server/api_docs_server.py"],
      "disabled": false
    }
  }
}
```

## Examples

### Example 1: Generate Python Payment Query Client

**User**: "I want to integrate PayerMax APIs"

**Agent will**:
1. **Ask for language preference FIRST**: "Which language would you like to use for our conversation? / 您希望使用哪种语言进行交流？"
   - Options: 1) English, 2) Chinese (中文)
2. **User enters**: 1
3. **Ask for use case** (in English): "Please briefly describe what you want to build with PayerMax APIs"
4. **User responds**: "I need Python code with a class-based client to query payment status for order ORDER_001, using environment variables for credentials, with error handling and logging for production"
5. **Agent identifies relevant API**: Searches and finds "付款查询" (Payment Order Query)
6. **Agent extracts from Step 4**: Python (language), class-based (structure), environment variables (credentials), error handling + logging (features), production (environment), ORDER_001 (outTradeNo parameter)
7. **Ask ONLY missing configuration questions** (in English):
   - Q1: SKIPPED (Python mentioned)
   - Q2: SKIPPED (class-based mentioned)
   - Q3: SKIPPED (environment variables mentioned)
   - Q4: SKIPPED (error handling and logging mentioned)
   - Q5: SKIPPED (production mentioned)
   - Q6: "Any special requirements?" → User: "no" → Continue
8. **Call API documentation**: `get_api_documentation("付款", "付款查询")`
9. **Parse required parameters** from API spec
10. **Collect ONLY missing parameter values**:
   - outTradeNo: SKIPPED (ORDER_001 already provided in Step 4)
   - merchantNo: SKIPPED (system parameter, use placeholder)
   - (Ask for any other required parameters not yet provided)
11. **Generate initial code** with all configurations and parameter values
12. **Self-review code** for syntax errors, completeness, and correctness
13. **Fix any issues** found during review
14. **Deliver production-ready Python code** that can run immediately

### Example 2: Create Multi-API Integration (Chinese)

**User**: "帮我构建支付集成"

**Agent will**:
1. **Ask for language preference FIRST**: "Which language would you like to use for our conversation? / 您希望使用哪种语言进行交流？"
   - Options: 1) English, 2) Chinese (中文)
2. **User enters**: 2
3. **Ask for use case** (in Chinese): "请简要描述您想用 PayerMax API 构建什么功能"
4. **User responds**: "我需要一个完整的收单系统，包括订单创建和状态查询"
5. **Agent identifies category**: Determines "收单" (Payment Collection) category is needed
6. **Ask configuration questions ONE AT A TIME** (in Chinese):
   - Q1: "您希望使用哪种编程语言？1) Python 2) Node.js 3) Java..." → User: "2" → Continue
   - Q2: "您希望生成什么样的代码结构？1) 基于类 2) 独立函数..." → User: "1" → Continue
   - Q3: "如何处理 API 凭证？1) 占位符 2) 实际凭证 3) 环境变量" → User: "3" → Continue
   - Q4: "您希望包含哪些功能？1) 错误处理 2) 日志 3) 验证..." → User: "1,2,3" → Continue
   - Q5: "目标环境？1) UAT 2) 生产环境" → User: "1" → Continue
   - Q6: "有特殊需求吗？" → User: "需要支持多个 API" → Continue
7. **Call API documentation**: `list_apis_in_category("收单")` and `get_api_documentation()` for each API
8. **Parse required parameters** from each API spec
9. **Collect parameter values for each API ONE AT A TIME**:
   - For 交易下单: "请提供 'outTradeNo' 的值（商户订单号，最多64字符）：" → User: "ORDER_001" → Continue
   - For 交易下单: "请提供 'totalAmount' 的值（订单金额）：" → User: "99.99" → Continue
   - (Repeat for other required parameters and APIs)
10. **Generate initial Node.js module** with all configurations and parameter values
11. **Self-review code** for syntax errors, completeness, and correctness
12. **Fix any issues** found during review
13. **Deliver production-ready Node.js code** that can run immediately

### Example 3: Quick Test Script

**User**: "I need to test an API quickly"

**Agent will**:
1. **Ask for use case**: "What API functionality do you want to test?"
2. **User responds**: "I want to test transaction query"
3. **Agent identifies API**: Finds "交易查询" (Transaction Query)
4. **Present selections**: Shell/curl, UAT/Production, etc.
5. Call `get_api_sample("收单", "交易查询")`
6. Extract the sample curl command
7. Provide it with placeholder credentials

## Best Practices

1. **Always Retrieve Specs First**: Don't guess API formats
2. **Use Official Samples**: Base code on provided samples
3. **Validate Parameters**: Check length limits and required fields
4. **Handle All Status Codes**: Include error handling for all scenarios
5. **Document Credentials**: Clearly mark where API keys should be inserted
6. **Add Logging**: Include logging for debugging
7. **Use Environment Variables**: Don't hardcode credentials

## Troubleshooting

### MCP Server Not Available

If the agent reports MCP tools are unavailable:
1. Check MCP server is running in Kiro's MCP panel
2. Verify `mcp.json` configuration
3. Restart Kiro IDE

### API Not Found

If an API cannot be found:
1. Use `list_api_categories()` to see available categories
2. Use `search_apis()` to find the correct API name
3. Check spelling and use exact names from documentation

### Generated Code Doesn't Work

1. Verify you're using correct API credentials
2. Check the endpoint URL (UAT vs Production)
3. Ensure signature generation is correct
4. Review parameter validation

## Related Resources

- PayerMax API Documentation: `api-docs/` directory
- API Samples: `api-samples/` directory
- MCP Server: `mcp-server/` directory

## Keywords

api, code generation, payermax, payment, integration, client, sdk, rest api, http, request, payload, codegen
