#!/bin/bash

# Script to get MCP Gateway URL and Bearer Token
# Usage: ./get-mcp-credentials.sh

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

CONFIG_FILE="mcp-server/payermax-mcp-complete-config.json"

echo -e "${BLUE}=== PayerMax MCP Gateway Credentials ===${NC}\n"

# Check if config file exists
if [ ! -f "$CONFIG_FILE" ]; then
    echo -e "${RED}Error: Configuration file not found: $CONFIG_FILE${NC}"
    exit 1
fi

# Check if jq is installed
if ! command -v jq &> /dev/null; then
    echo -e "${RED}Error: 'jq' is required but not installed.${NC}"
    echo "Install it with: brew install jq (macOS) or apt-get install jq (Linux)"
    exit 1
fi

# Extract configuration
GATEWAY_URL=$(jq -r '.gateway_url' "$CONFIG_FILE")
CLIENT_ID=$(jq -r '.client_id' "$CONFIG_FILE")
CLIENT_SECRET=$(jq -r '.client_secret' "$CONFIG_FILE")
TOKEN_ENDPOINT=$(jq -r '.token_endpoint' "$CONFIG_FILE")
SCOPES=$(jq -r '.scopes' "$CONFIG_FILE")

echo -e "${GREEN}1. MCP Gateway URL:${NC}"
echo "$GATEWAY_URL"
echo ""

echo -e "${YELLOW}2. Generating Bearer Token...${NC}"

# Get token from Cognito
TOKEN_RESPONSE=$(curl -s -X POST "$TOKEN_ENDPOINT" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -u "${CLIENT_ID}:${CLIENT_SECRET}" \
  -d "grant_type=client_credentials&scope=${SCOPES// /%20}")

# Check if token request was successful
if echo "$TOKEN_RESPONSE" | jq -e '.access_token' > /dev/null 2>&1; then
    ACCESS_TOKEN=$(echo "$TOKEN_RESPONSE" | jq -r '.access_token')
    EXPIRES_IN=$(echo "$TOKEN_RESPONSE" | jq -r '.expires_in')
    
    echo -e "${GREEN}✓ Token generated successfully${NC}"
    echo ""
    echo -e "${GREEN}3. Bearer Token:${NC}"
    echo "$ACCESS_TOKEN"
    echo ""
    echo -e "${YELLOW}Token expires in: ${EXPIRES_IN} seconds ($(($EXPIRES_IN / 3600)) hours)${NC}"
    echo ""
    
    # Print URL and Token clearly
    echo -e "${BLUE}=== Copy These Values ===${NC}\n"
    echo -e "${GREEN}URL:${NC}"
    echo "$GATEWAY_URL"
    echo ""
    echo -e "${GREEN}TOKEN:${NC}"
    echo "$ACCESS_TOKEN"
    echo ""
    
    # Generate Kiro MCP config
    echo -e "${BLUE}=== Kiro MCP Configuration ===${NC}\n"
    echo "Copy this to your .kiro/settings/mcp.json:"
    echo ""
    cat << EOF
{
  "mcpServers": {
    "payermax-api-docs": {
      "url": "$GATEWAY_URL",
      "headers": {
        "Authorization": "Bearer $ACCESS_TOKEN"
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
EOF
    echo ""
    
    # Save to file
    OUTPUT_FILE="mcp-credentials.json"
    cat > "$OUTPUT_FILE" << EOF
{
  "gateway_url": "$GATEWAY_URL",
  "bearer_token": "$ACCESS_TOKEN",
  "expires_in_seconds": $EXPIRES_IN,
  "generated_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
}
EOF
    
    echo -e "${GREEN}✓ Credentials saved to: $OUTPUT_FILE${NC}"
    echo ""
    echo -e "${YELLOW}Note: Token will expire in $(($EXPIRES_IN / 3600)) hours. Run this script again to get a new token.${NC}"
    
else
    echo -e "${RED}Error: Failed to get access token${NC}"
    echo "Response: $TOKEN_RESPONSE"
    exit 1
fi
