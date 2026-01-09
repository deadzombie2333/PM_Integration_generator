#!/bin/bash

# PayerMax MCP Lambda Deployment Script
# Deploy Lambda function for PayerMax MCP Server

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Configuration
REGION=${AWS_REGION:-us-west-2}
STACK_NAME=${1:-"payermax-mcp-lambda-stack"}
GATEWAY_NAME="payermax-mcp-gateway"
VPC_NAME="payermax-mcp"

echo -e "${GREEN}Starting PayerMax MCP Lambda deployment...${NC}"
echo "Region: $REGION"
echo "Stack Name: $STACK_NAME"
echo "Gateway Name: $GATEWAY_NAME"

# Check for network config
if [ ! -f "network-config.json" ]; then
    echo -e "${RED}Error: network-config.json not found${NC}"
    echo "Please run deploy-vpc.sh first"
    exit 1
fi

# Extract network configuration
VPC_ID=$(jq -r '.vpc_id' network-config.json)
PRIVATE_SUBNET_1=$(jq -r '.subnet_config."Private-us-west-2a".subnet_id' network-config.json)
PRIVATE_SUBNET_2=$(jq -r '.subnet_config."Private-us-west-2b".subnet_id' network-config.json)
SECURITY_GROUP_ID=$(jq -r '.sg_config[0]' network-config.json)

echo "VPC ID: $VPC_ID"
echo "Private Subnets: $PRIVATE_SUBNET_1, $PRIVATE_SUBNET_2"
echo "Security Group: $SECURITY_GROUP_ID"

# Check if Gateway stack exists to get Cognito info
GATEWAY_STACK_NAME="payermax-mcp-gateway-stack"
if aws cloudformation describe-stacks --stack-name "$GATEWAY_STACK_NAME" --region "$REGION" >/dev/null 2>&1; then
    echo -e "${YELLOW}Gateway stack found, retrieving Cognito configuration...${NC}"
    COGNITO_POOL_ID=$(aws cloudformation describe-stacks \
        --stack-name "$GATEWAY_STACK_NAME" \
        --region "$REGION" \
        --query 'Stacks[0].Outputs[?OutputKey==`CognitoUserPoolId`].OutputValue' \
        --output text)
    
    COGNITO_CLIENT_ID=$(aws cloudformation describe-stacks \
        --stack-name "$GATEWAY_STACK_NAME" \
        --region "$REGION" \
        --query 'Stacks[0].Outputs[?OutputKey==`ClientId`].OutputValue' \
        --output text)
    
    echo "Cognito Pool ID: $COGNITO_POOL_ID"
    echo "Cognito Client ID: $COGNITO_CLIENT_ID"
else
    echo -e "${YELLOW}Gateway stack not found. Lambda will be deployed without Cognito config.${NC}"
    echo "You can update the Lambda environment variables after deploying the gateway."
    COGNITO_POOL_ID=""
    COGNITO_CLIENT_ID=""
fi

# Check if OpenSearch stack exists
OPENSEARCH_STACK_NAME="payermax-mcp-opensearch-stack"
if aws cloudformation describe-stacks --stack-name "$OPENSEARCH_STACK_NAME" --region "$REGION" >/dev/null 2>&1; then
    echo -e "${YELLOW}OpenSearch stack found, retrieving configuration...${NC}"
    OPENSEARCH_ENDPOINT=$(aws cloudformation describe-stacks \
        --stack-name "$OPENSEARCH_STACK_NAME" \
        --region "$REGION" \
        --query 'Stacks[0].Outputs[?OutputKey==`CollectionEndpoint`].OutputValue' \
        --output text)
    
    OPENSEARCH_INDEX=$(aws cloudformation describe-stacks \
        --stack-name "$OPENSEARCH_STACK_NAME" \
        --region "$REGION" \
        --query 'Stacks[0].Outputs[?OutputKey==`IndexName`].OutputValue' \
        --output text)
    
    echo "OpenSearch Endpoint: $OPENSEARCH_ENDPOINT"
    echo "OpenSearch Index: $OPENSEARCH_INDEX"
else
    echo -e "${YELLOW}OpenSearch stack not found. Lambda will be deployed without OpenSearch config.${NC}"
    OPENSEARCH_ENDPOINT=""
    OPENSEARCH_INDEX="payermax-docs"
fi

# Deploy Lambda stack
echo -e "\n${YELLOW}Deploying Lambda CloudFormation stack...${NC}"

PARAMS="VpcName=$VPC_NAME GatewayName=$GATEWAY_NAME"

if [ -n "$COGNITO_POOL_ID" ]; then
    PARAMS="$PARAMS CognitoUserPoolId=$COGNITO_POOL_ID"
fi

if [ -n "$COGNITO_CLIENT_ID" ]; then
    PARAMS="$PARAMS CognitoClientId=$COGNITO_CLIENT_ID"
fi

if [ -n "$OPENSEARCH_ENDPOINT" ]; then
    PARAMS="$PARAMS OpenSearchEndpoint=$OPENSEARCH_ENDPOINT"
fi

if [ -n "$OPENSEARCH_INDEX" ]; then
    PARAMS="$PARAMS OpenSearchIndexName=$OPENSEARCH_INDEX"
fi

aws cloudformation deploy \
    --template-file deploy/lambda-template.yaml \
    --stack-name $STACK_NAME \
    --parameter-overrides $PARAMS \
    --capabilities CAPABILITY_NAMED_IAM \
    --region $REGION

# Get outputs
echo -e "\n${YELLOW}Retrieving deployment information...${NC}"
LAMBDA_ARN=$(aws cloudformation describe-stacks \
    --stack-name $STACK_NAME \
    --region $REGION \
    --query 'Stacks[0].Outputs[?OutputKey==`LambdaFunctionArn`].OutputValue' \
    --output text)

LAMBDA_NAME=$(aws cloudformation describe-stacks \
    --stack-name $STACK_NAME \
    --region $REGION \
    --query 'Stacks[0].Outputs[?OutputKey==`LambdaFunctionName`].OutputValue' \
    --output text)

LAMBDA_ROLE_ARN=$(aws cloudformation describe-stacks \
    --stack-name $STACK_NAME \
    --region $REGION \
    --query 'Stacks[0].Outputs[?OutputKey==`LambdaExecutionRoleArn`].OutputValue' \
    --output text)

# Save configuration
echo -e "\n${YELLOW}Creating Lambda configuration file...${NC}"
cat > payermax-mcp-lambda-config.json << EOF
{
    "region": "$REGION",
    "stack_name": "$STACK_NAME",
    "lambda_function_arn": "$LAMBDA_ARN",
    "lambda_function_name": "$LAMBDA_NAME",
    "lambda_execution_role_arn": "$LAMBDA_ROLE_ARN",
    "vpc_id": "$VPC_ID",
    "private_subnet_ids": ["$PRIVATE_SUBNET_1", "$PRIVATE_SUBNET_2"],
    "security_group_id": "$SECURITY_GROUP_ID",
    "cognito_pool_id": "$COGNITO_POOL_ID",
    "cognito_client_id": "$COGNITO_CLIENT_ID",
    "opensearch_endpoint": "$OPENSEARCH_ENDPOINT",
    "opensearch_index": "$OPENSEARCH_INDEX"
}
EOF

echo -e "\n${GREEN}✅ Lambda deployment completed!${NC}"
echo -e "\n${YELLOW}Deployment Information:${NC}"
echo "Lambda Function ARN: $LAMBDA_ARN"
echo "Lambda Function Name: $LAMBDA_NAME"
echo "Lambda Execution Role ARN: $LAMBDA_ROLE_ARN"
echo ""
echo -e "${YELLOW}Configuration saved to: payermax-mcp-lambda-config.json${NC}"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "1. Package and upload your MCP server code:"
echo "   cd deploy && ./package-lambda.sh"
echo ""
echo "2. If OpenSearch not deployed yet, deploy it now:"
echo "   ./deploy-opensearch.sh"
echo ""
echo "3. Deploy the Gateway:"
echo "   ./deploy-gateway.sh"