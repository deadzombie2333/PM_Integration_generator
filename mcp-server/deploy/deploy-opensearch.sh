#!/bin/bash

# PayerMax MCP OpenSearch Serverless Deployment Script
# Deploy OpenSearch Serverless collection in VPC (us-west-2)

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Configuration
REGION="us-west-2"
STACK_NAME="payermax-mcp-opensearch-stack"
VPC_NAME="payermax-mcp"
COLLECTION_NAME="payermax-docs"
INDEX_NAME="payermax-docs"

echo -e "${GREEN}Starting PayerMax MCP OpenSearch Serverless deployment...${NC}"
echo "Region: $REGION"
echo "Stack Name: $STACK_NAME"
echo "Collection Name: $COLLECTION_NAME"
echo "VPC Name: $VPC_NAME"

# Check if Lambda config exists to get execution role
if [ ! -f "payermax-mcp-lambda-config.json" ]; then
    echo -e "${RED}Error: payermax-mcp-lambda-config.json not found${NC}"
    echo "Please run deploy-lambda.sh first"
    exit 1
fi

# Get Lambda execution role ARN
LAMBDA_ROLE_ARN=$(jq -r '.lambda_execution_role_arn' payermax-mcp-lambda-config.json)
echo "Lambda Execution Role ARN: $LAMBDA_ROLE_ARN"

# Deploy OpenSearch stack
echo -e "\n${YELLOW}Deploying OpenSearch Serverless CloudFormation stack...${NC}"

aws cloudformation deploy \
    --template-file mcp-server/deploy/opensearch-template.yaml \
    --stack-name $STACK_NAME \
    --parameter-overrides \
        VpcName=$VPC_NAME \
        CollectionName=$COLLECTION_NAME \
        IndexName=$INDEX_NAME \
        LambdaExecutionRoleArn=$LAMBDA_ROLE_ARN \
    --capabilities CAPABILITY_NAMED_IAM \
    --region $REGION

# Get outputs
echo -e "\n${YELLOW}Retrieving deployment information...${NC}"
COLLECTION_ENDPOINT=$(aws cloudformation describe-stacks \
    --stack-name $STACK_NAME \
    --region $REGION \
    --query 'Stacks[0].Outputs[?OutputKey==`CollectionEndpoint`].OutputValue' \
    --output text)

COLLECTION_ARN=$(aws cloudformation describe-stacks \
    --stack-name $STACK_NAME \
    --region $REGION \
    --query 'Stacks[0].Outputs[?OutputKey==`CollectionArn`].OutputValue' \
    --output text)

COLLECTION_ID=$(aws cloudformation describe-stacks \
    --stack-name $STACK_NAME \
    --region $REGION \
    --query 'Stacks[0].Outputs[?OutputKey==`CollectionId`].OutputValue' \
    --output text)

# Remove https:// prefix for environment variable
OPENSEARCH_HOST=${COLLECTION_ENDPOINT#https://}

# Save configuration
echo -e "\n${YELLOW}Creating OpenSearch configuration file...${NC}"
cat > payermax-mcp-opensearch-config.json << EOF
{
    "region": "$REGION",
    "stack_name": "$STACK_NAME",
    "collection_name": "$COLLECTION_NAME",
    "collection_endpoint": "$COLLECTION_ENDPOINT",
    "collection_host": "$OPENSEARCH_HOST",
    "collection_arn": "$COLLECTION_ARN",
    "collection_id": "$COLLECTION_ID",
    "index_name": "$INDEX_NAME"
}
EOF

# Update Lambda environment variables
echo -e "\n${YELLOW}Updating Lambda environment variables with OpenSearch endpoint...${NC}"
aws lambda update-function-configuration \
    --function-name payermax-mcp-gateway-lambda \
    --environment Variables="{CUSTOM_REGION=$REGION,COGNITO_USER_POOL_ID=$(jq -r '.cognito_pool_id' payermax-mcp-lambda-config.json),COGNITO_CLIENT_ID=$(jq -r '.cognito_client_id' payermax-mcp-lambda-config.json),OPENSEARCH_ENDPOINT=$OPENSEARCH_HOST,OPENSEARCH_INDEX=$INDEX_NAME}" \
    --region $REGION

echo -e "\n${GREEN}✅ OpenSearch Serverless deployment completed!${NC}"
echo -e "\n${YELLOW}Deployment Information:${NC}"
echo "Collection Endpoint: $COLLECTION_ENDPOINT"
echo "Collection Host: $OPENSEARCH_HOST"
echo "Collection ARN: $COLLECTION_ARN"
echo "Collection ID: $COLLECTION_ID"
echo "Index Name: $INDEX_NAME"
echo ""
echo -e "${YELLOW}Configuration saved to: payermax-mcp-opensearch-config.json${NC}"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "1. Wait 60 seconds for OpenSearch collection to be ready"
echo ""
echo "2. Run document embedder to populate OpenSearch:"
echo "   export OPENSEARCH_ENDPOINT=$OPENSEARCH_HOST"
echo "   export OPENSEARCH_INDEX=$INDEX_NAME"
echo "   export AWS_REGION=$REGION"
echo "   python run_embedder.py"
echo ""
echo "3. Deploy Gateway Target:"
echo "   ./deploy/deploy-gateway-target.sh"

