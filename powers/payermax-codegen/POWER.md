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

⚠️ **CRITICAL: BEFORE YOU DO ANYTHING, READ THIS** ⚠️

**YOUR FIRST ACTION MUST BE:**
1. Read `steering/getting-started.md` using readSteering action
2. ALWAYS use vibe session mode for this power
3. Ask: "Which language would you like to use for our conversation? 1) English 2) Chinese (中文)"
4. Use ONLY the selected language for ALL subsequent messages (no mixing)
5. Follow the 6-step workflow exactly as written

**IF YOU SKIP STEP 1 (LANGUAGE QUESTION), YOU HAVE FAILED**
**IF YOU MIX LANGUAGES AFTER SELECTION, YOU HAVE FAILED**
**IF YOU GENERATE CODE BEFORE STEP 6, YOU HAVE FAILED**

---

Generate production-ready PayerMax API integration code with correct payloads, request formats, and error handling.

## Overview

This power uses the PayerMax API Documentation MCP server with AWS Nova LLM and semantic search to:
1. Analyze your requirements
2. Create integration plans
3. Recommend optimal integration methods
4. Generate accurate, ready-to-use code

## Features

- **Integration Planning**: Creates detailed `integration-plan.md` before coding
- **Intelligent Recommendations**: Uses LLM to suggest best integration methods
- **Semantic Search**: Finds relevant documentation using embedding-based search
- **Separate Files**: One file per API endpoint with clear naming
- **Web Integration**: Includes frontend and backend for Cashier/Drop-in modes
- **Multiple Languages**: Python, Node.js, Java, PHP, Go, Ruby, C#, Shell

## Available MCP Tools

### Tool 1: find_api_endpoint()
Finds correct API endpoint specifications using LLM analysis.

**Parameters:**
- `task_type`: create_payment, query_payment, refund, etc.
- `payment_type`: card, wallet, bank_transfer, etc.
- `integration_mode`: cashier, api, drop_in, link
- `include_samples`: Include sample code (default: True)

### Tool 2: get_integration_recommendation()
Analyzes requirements and recommends best integration method.

**Parameters:**
- `user_description`: Natural language description of requirements

## Workflow

⚠️ **STOP! READ THIS BEFORE DOING ANYTHING** ⚠️

**YOU MUST IMMEDIATELY READ `steering/getting-started.md` BEFORE TAKING ANY ACTION**

Use the `readSteering` action with `steeringFile: "getting-started.md"` RIGHT NOW.

**ABSOLUTE REQUIREMENTS - VIOLATION WILL CAUSE FAILURE:**

1. ❌ **NEVER EVER** generate code without completing ALL 6 steps first
2. ❌ **NEVER EVER** skip Step 1 (language selection) - THIS IS ALWAYS THE FIRST QUESTION
3. ❌ **NEVER EVER** skip Step 4 (6 information questions) - ALL 6 MUST BE ASKED
4. ❌ **NEVER EVER** skip Step 5 (confirmation) - MUST WAIT FOR "YES"
5. ❌ **NEVER EVER** combine multiple steps or questions together
6. ✅ **ALWAYS** ask ONE question at a time and WAIT for answer
7. ✅ **ALWAYS** follow the exact order: 1→2→3→4→5→6

**THE ONLY CORRECT FIRST ACTION:**
Ask: "Which language would you like to use for our conversation? - Chinese (中文) - English"

**Required Steps (ZERO SKIPPING ALLOWED):**
1. **Select language** → WAIT for user response
2. **Describe requirements** → WAIT for user response  
3. **Create integration-plan.md** → WAIT for user approval
4. **Ask 6 information questions** → WAIT for EACH answer (one at a time)
5. **Confirm code generation** → WAIT for "yes"
6. **Generate code files** (ONLY after steps 1-5 complete)

**IF YOU SKIP ANY STEP, YOU HAVE FAILED THE TASK**

## Prerequisites

- PayerMax Developer Account
- API credentials (appId, merchantNo, signing keys)
- RSA key pair configured
- Callback URLs configured
- Payment methods enabled

## Supported Languages

Python, Node.js, Java, PHP, Go, Ruby, C#, Shell/curl

## Best Practices

1. Always create integration plan first
2. Review plan before code generation
3. Use separate files per endpoint
4. Include frontend/backend for web integrations
5. Test in UAT before production
6. Use environment variables for credentials

## Troubleshooting

### MCP Server Not Connected
- Check `.kiro/settings/mcp.json` configuration
- Verify Python virtual environment path
- Restart MCP server from Kiro panel

### Code Generation Issues
- Ensure integration plan is created first
- Verify all information is collected
- Check MCP tools are responding

## Related Resources

- Integration Guide: `steering/getting-started.md`
- API Documentation: `mcp-server/api-docs/`
- API Samples: `mcp-server/api-samples/`
- Integration Processes: `mcp-server/integration_process/`
