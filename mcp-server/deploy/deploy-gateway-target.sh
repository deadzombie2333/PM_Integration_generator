#!/bin/bash

# PayerMax MCP Gateway Target Deployment Script
# Deploy AgentCore Gateway Target

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Configuration
REGION=${AWS_REGION:-us-west-2}
TARGET_STACK_NAME=${1:-"payermax-mcp-target-stack"}
GATEWAY_STACK_NAME="payermax-mcp-gateway-stack"
LAMBDA_STACK_NAME="payermax-mcp-lambda-stack"
GATEWAY_NAME="payermax-mcp-gateway"

echo -e "${GREEN}Starting PayerMax MCP Gateway Target deployment...${NC}"
echo "Region: $REGION"
echo "Target Stack Name: $TARGET_STACK_NAME"
echo "Gateway Stack Name: $GATEWAY_STACK_NAME"
echo "Lambda Stack Name: $LAMBDA_STACK_NAME"

# Check if gateway config exists
if [ ! -f "payermax-mcp-gateway-config.json" ]; then
    echo -e "${RED}Error: payermax-mcp-gateway-config.json not found${NC}"
    echo "Please run deploy-gateway.sh first"
    exit 1
fi

# Check if lambda config exists
if [ ! -f "payermax-mcp-lambda-config.json" ]; then
    echo -e "${RED}Error: payermax-mcp-lambda-config.json not found${NC}"
    echo "Please run deploy-lambda.sh first"
    exit 1
fi

# Read configuration
GATEWAY_ID=$(jq -r '.gateway_id' payermax-mcp-gateway-config.json)
GATEWAY_URL=$(jq -r '.gateway_url' payermax-mcp-gateway-config.json)
CLIENT_ID=$(jq -r '.client_id' payermax-mcp-gateway-config.json)
CLIENT_SECRET=$(jq -r '.client_secret' payermax-mcp-gateway-config.json)
USER_POOL_ID=$(jq -r '.pool_id' payermax-mcp-gateway-config.json)
DISCOVERY_URL=$(jq -r '.discovery_url' payermax-mcp-gateway-config.json)
JWT_ISSUER=$(jq -r '.jwt_issuer' payermax-mcp-gateway-config.json)
SCOPES=$(jq -r '.scopes' payermax-mcp-gateway-config.json)
TOKEN_ENDPOINT=$(jq -r '.token_endpoint' payermax-mcp-gateway-config.json)

LAMBDA_ARN=$(jq -r '.lambda_function_arn' payermax-mcp-lambda-config.json)
LAMBDA_ROLE_ARN=$(jq -r '.lambda_execution_role_arn' payermax-mcp-lambda-config.json)

echo "Gateway ID: $GATEWAY_ID"
echo "Lambda ARN: $LAMBDA_ARN"

# Verify resources exist
echo -e "\n${YELLOW}Verifying resources...${NC}"

# Verify Lambda function
LAMBDA_FUNCTION_NAME=$(echo $LAMBDA_ARN | cut -d':' -f7)
if aws lambda get-function --function-name $LAMBDA_FUNCTION_NAME --region $REGION >/dev/null 2>&1; then
    echo -e "${GREEN}✓ Lambda function verified: $LAMBDA_FUNCTION_NAME${NC}"
else
    echo -e "${RED}Error: Lambda function not found - $LAMBDA_FUNCTION_NAME${NC}"
    exit 1
fi

# Deploy Gateway Target stack
echo -e "\n${YELLOW}Deploying Gateway Target CloudFormation stack...${NC}"

aws cloudformation deploy \
    --template-file mcp-server/deploy/gateway-target-template.yaml \
    --stack-name $TARGET_STACK_NAME \
    --parameter-overrides \
        GatewayName=$GATEWAY_NAME \
        GatewayStackName=$GATEWAY_STACK_NAME \
        LambdaStackName=$LAMBDA_STACK_NAME \
    --capabilities CAPABILITY_NAMED_IAM \
    --region $REGION

# Get outputs
echo -e "\n${YELLOW}Retrieving deployment information...${NC}"
GATEWAY_TARGET_ID=$(aws cloudformation describe-stacks \
    --stack-name $TARGET_STACK_NAME \
    --region $REGION \
    --query 'Stacks[0].Outputs[?OutputKey==`AgentCoreGatewayTargetId`].OutputValue' \
    --output text)

# Create complete configuration file
echo -e "\n${YELLOW}Creating complete Gateway configuration file...${NC}"
cat > payermax-mcp-complete-config.json << EOF
{
    "region": "$REGION",
    "lambda_stack_name": "$LAMBDA_STACK_NAME",
    "gateway_stack_name": "$GATEWAY_STACK_NAME",
    "target_stack_name": "$TARGET_STACK_NAME",
    "gateway_name": "$GATEWAY_NAME",
    "client_id": "$CLIENT_ID",
    "pool_id": "$USER_POOL_ID",
    "client_secret": "$CLIENT_SECRET",
    "token_endpoint": "$TOKEN_ENDPOINT",
    "discovery_url": "$DISCOVERY_URL",
    "jwt_issuer": "$JWT_ISSUER",
    "scopes": "$SCOPES",
    "lambda_function_arn": "$LAMBDA_ARN",
    "execution_role_arn": "$LAMBDA_ROLE_ARN",
    "gateway_id": "$GATEWAY_ID",
    "gateway_url": "$GATEWAY_URL",
    "gateway_target_id": "$GATEWAY_TARGET_ID",
    "authorizer_config": {
        "jwtConfiguration": {
            "issuer": "$JWT_ISSUER",
            "audience": ["$CLIENT_ID"]
        }
    }
}
EOF

echo -e "\n${GREEN}✅ Gateway Target deployment completed!${NC}"
echo -e "\n${YELLOW}Deployment Information:${NC}"
echo "Lambda Function ARN: $LAMBDA_ARN"
echo "Cognito User Pool ID: $USER_POOL_ID"
echo "Cognito Client ID: $CLIENT_ID"
echo "Gateway ID: $GATEWAY_ID"
echo "Gateway URL: $GATEWAY_URL"
echo "Gateway Target ID: $GATEWAY_TARGET_ID"
echo ""
echo -e "${YELLOW}Configuration saved to: payermax-mcp-complete-config.json${NC}"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "1. Package and deploy your MCP server code to Lambda"
echo "2. Test the Gateway connection"
echo "3. View Gateway Target status:"
echo "   aws bedrock-agentcore get-gateway-target \\"
echo "     --gateway-identifier $GATEWAY_ID \\"
echo "     --gateway-target-identifier $GATEWAY_TARGET_ID \\"
echo "     --region $REGION"