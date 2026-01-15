#!/bin/bash

# Update OpenSearch access policy to include IAM user

set -e

REGION=${AWS_REGION:-us-west-2}
POLICY_NAME="payermax-docs-access"

# Get Lambda role ARN from config file
if [ ! -f "payermax-mcp-lambda-config.json" ]; then
    echo "❌ Error: payermax-mcp-lambda-config.json not found"
    echo "Please run deploy-lambda.sh first to create the Lambda function and config"
    exit 1
fi

LAMBDA_ROLE_ARN=$(jq -r '.lambda_execution_role_arn' payermax-mcp-lambda-config.json)

# Optional: Add your IAM user ARN for local testing
USER_ARN=${USER_ARN:-""}

echo "Lambda Role ARN: $LAMBDA_ROLE_ARN"
if [ -n "$USER_ARN" ]; then
    echo "User ARN: $USER_ARN"
fi

echo ""
echo "Getting current policy version..."
POLICY_VERSION=$(aws opensearchserverless get-access-policy \
  --name $POLICY_NAME \
  --type data \
  --region $REGION \
  --query 'accessPolicyDetail.policyVersion' \
  --output text)

echo "Current policy version: $POLICY_VERSION"
echo "Updating access policy..."

# Build principal list
if [ -n "$USER_ARN" ]; then
    PRINCIPALS="[\"$LAMBDA_ROLE_ARN\",\"$USER_ARN\"]"
else
    PRINCIPALS="[\"$LAMBDA_ROLE_ARN\"]"
fi

aws opensearchserverless update-access-policy \
  --name $POLICY_NAME \
  --type data \
  --region $REGION \
  --policy-version $POLICY_VERSION \
  --policy "[{\"Rules\":[{\"ResourceType\":\"collection\",\"Resource\":[\"collection/payermax-docs\"],\"Permission\":[\"aoss:CreateCollectionItems\",\"aoss:UpdateCollectionItems\",\"aoss:DescribeCollectionItems\"]},{\"ResourceType\":\"index\",\"Resource\":[\"index/payermax-docs/*\"],\"Permission\":[\"aoss:CreateIndex\",\"aoss:DeleteIndex\",\"aoss:UpdateIndex\",\"aoss:DescribeIndex\",\"aoss:ReadDocument\",\"aoss:WriteDocument\"]}],\"Principal\":$PRINCIPALS}]"

echo ""
echo "✅ Access policy updated successfully!"
echo ""
echo "Next steps:"
echo "1. Set environment variables:"
echo "   export OPENSEARCH_ENDPOINT=\$(jq -r '.collection_host' payermax-mcp-opensearch-config.json)"
echo "   export OPENSEARCH_INDEX=payermax-docs"
echo "   export AWS_REGION=$REGION"
echo ""
echo "2. Run the embedder:"
echo "   python run_embedder.py"
