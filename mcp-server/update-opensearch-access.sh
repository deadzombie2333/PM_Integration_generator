#!/bin/bash

# Update OpenSearch access policy to include IAM user

set -e

REGION="us-west-2"
POLICY_NAME="payermax-docs-access"
USER_ARN="arn:aws:iam::183017937161:user/jingwei"
LAMBDA_ROLE_ARN="arn:aws:iam::183017937161:role/payermax-mcp-gateway-lambda-execution-role"

echo "Getting current policy version..."
POLICY_VERSION=$(aws opensearchserverless get-access-policy \
  --name $POLICY_NAME \
  --type data \
  --region $REGION \
  --query 'accessPolicyDetail.policyVersion' \
  --output text)

echo "Current policy version: $POLICY_VERSION"
echo "Updating access policy to include IAM user..."

aws opensearchserverless update-access-policy \
  --name $POLICY_NAME \
  --type data \
  --region $REGION \
  --policy-version $POLICY_VERSION \
  --policy "[{\"Rules\":[{\"ResourceType\":\"collection\",\"Resource\":[\"collection/payermax-docs\"],\"Permission\":[\"aoss:CreateCollectionItems\",\"aoss:UpdateCollectionItems\",\"aoss:DescribeCollectionItems\"]},{\"ResourceType\":\"index\",\"Resource\":[\"index/payermax-docs/*\"],\"Permission\":[\"aoss:CreateIndex\",\"aoss:DeleteIndex\",\"aoss:UpdateIndex\",\"aoss:DescribeIndex\",\"aoss:ReadDocument\",\"aoss:WriteDocument\"]}],\"Principal\":[\"$LAMBDA_ROLE_ARN\",\"$USER_ARN\"]}]"

echo "✅ Access policy updated successfully!"
echo "You can now run: python run_embedder.py"
