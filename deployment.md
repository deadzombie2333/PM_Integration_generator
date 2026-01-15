# PayerMax MCP Server - AWS Deployment Guide

Complete step-by-step guide for deploying the PayerMax MCP Server infrastructure on AWS.

## Overview

This deployment creates a secure, scalable MCP (Model Context Protocol) server infrastructure with:
- VPC isolation with private subnets
- Cognito JWT authentication
- Lambda function for MCP server
- OpenSearch Serverless for semantic search
- Bedrock AI integration
- AgentCore Gateway for public access

## Architecture

```
Client (Kiro IDE/CLI)
    ↓ HTTPS + JWT Auth
AgentCore Gateway (Public)
    ↓ Invokes
Lambda Function (Private VPC)
    ↓ VPC Endpoints
AWS Services (Bedrock, OpenSearch, S3, CloudWatch)
```

## Prerequisites

### Required Tools
- AWS CLI configured with appropriate credentials
- Python 3.11+
- jq (JSON processor)
- bash shell

### AWS Permissions Required
- VPC and networking resources
- Lambda functions
- Cognito User Pools
- OpenSearch Serverless
- Bedrock access
- CloudFormation stacks
- IAM roles and policies

### Install Dependencies

**macOS:**
```bash
brew install jq awscli
```

**Ubuntu/Debian:**
```bash
sudo apt-get install jq awscli
```

**Verify Installation:**
```bash
aws --version
jq --version
python3 --version
```

## Deployment Steps

### Step 1: Deploy VPC Infrastructure

Deploy the VPC with subnets, NAT gateways, and VPC endpoints.

```bash
cd mcp-server/deploy
./deploy-vpc.sh
```

**What This Creates:**
- VPC (10.0.0.0/16)
- 2 Public Subnets (10.0.11.0/24, 10.0.12.0/24)
- 2 Private Subnets (10.0.21.0/24, 10.0.22.0/24)
- Internet Gateway
- 2 NAT Gateways with Elastic IPs
- 3 Route Tables
- Security Group for VPC endpoints
- 18 VPC Endpoints:
  - S3 Gateway Endpoint (free)
  - ECR Docker & API
  - CloudWatch Logs
  - Systems Manager (SSM, SSM Messages, EC2 Messages)
  - Bedrock (6 endpoints: bedrock, bedrock-runtime, bedrock-agent, etc.)
  - Lambda
  - Cognito Identity Provider
  - OpenSearch Serverless

**Output:**
- Creates `network-config.json` with VPC configuration
- Exports VPC ID, subnet IDs, security group ID

**Estimated Time:** 5-10 minutes

**Cost:** ~$187/month
- NAT Gateways: ~$65/month (can be removed if not needed)
- VPC Endpoints: ~$122/month

### Step 2: Deploy Gateway with Cognito

Deploy the AgentCore Gateway with Cognito authentication.

```bash
./deploy-gateway.sh
```

**What This Creates:**
- Cognito User Pool
- Cognito App Client with client credentials flow
- Cognito Domain for OAuth
- Resource Server with custom scopes
- AgentCore Gateway (public endpoint)
- JWT Authorizer

**Output:**
- Creates `payermax-mcp-gateway-config.json` with:
  - Gateway ID and URL
  - Cognito Pool ID
  - Client ID and Client Secret
  - Token Endpoint
  - JWT Issuer

**Estimated Time:** 3-5 minutes

**Cost:** Minimal (Cognito free tier covers most usage)

### Step 3: Deploy Lambda Function

Deploy the Lambda function that will run the MCP server.

```bash
./deploy-lambda.sh
```

**What This Creates:**
- Lambda Function (Python 3.11, 2048MB, 5min timeout)
- IAM Execution Role with policies for:
  - CloudWatch Logs
  - Bedrock Runtime
  - OpenSearch Serverless
  - S3 access
  - VPC network interface management
- Lambda deployed in private subnets
- Environment variables configured

**Output:**
- Creates `payermax-mcp-lambda-config.json` with:
  - Lambda Function ARN
  - Lambda Function Name
  - Execution Role ARN
  - VPC configuration

**Estimated Time:** 2-3 minutes

**Cost:** Pay per invocation
- First 1M requests/month free
- $0.20 per 1M requests after
- $0.0000166667 per GB-second

### Step 4: Deploy OpenSearch Serverless

Deploy OpenSearch Serverless collection for semantic search.

```bash
./deploy-opensearch.sh
```

**Prerequisites:**
- Lambda must be deployed first (needs execution role ARN)

**What This Creates:**
- OpenSearch Serverless Collection (VECTORSEARCH type)
- Encryption Policy (AWS-owned key)
- Network Policy (VPC-only access)
- Data Access Policy (Lambda execution role access)
- Index configuration

**Output:**
- Creates `payermax-mcp-opensearch-config.json` with:
  - Collection Endpoint
  - Collection ARN
  - Collection ID
  - Index Name
- Updates Lambda environment variables with OpenSearch endpoint

**Estimated Time:** 5-10 minutes (collection provisioning)

**Cost:** Based on OCU (OpenSearch Compute Units)
- Minimum: 2 OCUs (~$350/month for production)
- Development: Can use lower configuration

### Step 5: Package and Deploy Lambda Code

Package the MCP server code and deploy to Lambda.

```bash
./package-lambda.sh
```

**What This Does:**
- Creates `lambda-package` directory
- Copies MCP server files:
  - `api_docs_server.py`
  - `tools/` directory
  - `api-docs/` documentation
  - `api-samples/` code samples
  - `integration_process/` guides
  - `payermax_doc/` product docs
- Installs Python dependencies for Lambda runtime
- Creates Lambda handler wrapper
- Creates deployment ZIP
- Uploads to Lambda function
- Updates handler configuration

**Estimated Time:** 5-10 minutes (depending on package size)

**Note:** If package exceeds 50MB, it will automatically upload to S3 first.

### Step 6: Generate Document Embeddings

Index all documentation into OpenSearch for semantic search.

```bash
cd mcp-server

# Set environment variables
export OPENSEARCH_ENDPOINT="<your-collection-endpoint>"
export OPENSEARCH_INDEX="payermax-docs"
export AWS_REGION="us-west-2"

# Run embedder
python run_embedder.py
```

**What This Does:**
- Reads all API documentation files
- Generates embeddings using Bedrock Titan
- Creates OpenSearch index with vector mappings
- Indexes documents with embeddings
- Enables semantic search for Tools 3 & 4

**Estimated Time:** 30-60 minutes (depending on document count)

**Cost:** Bedrock Titan Embeddings
- $0.0001 per 1K input tokens
- Approximately $5-10 for full documentation set

### Step 7: Deploy Gateway Target

Connect the Gateway to the Lambda function.

```bash
cd mcp-server/deploy
./deploy-gateway-target.sh
```

**What This Creates:**
- AgentCore Gateway Target
- Lambda invoke permissions for Gateway
- Gateway-Lambda integration

**Output:**
- Creates `payermax-mcp-complete-config.json` with complete configuration
- Gateway Target ID

**Estimated Time:** 2-3 minutes

## Post-Deployment Configuration

### 1. Get Access Token

```bash
# Use the provided script
./get-mcp-credentials.sh

# Or manually get token
CLIENT_ID="<from-config>"
CLIENT_SECRET="<from-config>"
TOKEN_ENDPOINT="<from-config>"

curl -X POST "$TOKEN_ENDPOINT" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=client_credentials" \
  -d "client_id=$CLIENT_ID" \
  -d "client_secret=$CLIENT_SECRET" \
  -d "scope=payermax-mcp/mcp.access"
```

### 2. Test the Gateway

```bash
# Test MCP gateway
python mcp-server/test-mcp-gateway.py
```

### 3. Configure Kiro IDE

Add to `.kiro/settings/mcp.json`:

```json
{
  "mcpServers": {
    "payermax-mcp": {
      "command": "node",
      "args": ["path/to/mcp-client.js"],
      "env": {
        "GATEWAY_URL": "<gateway-url>",
        "CLIENT_ID": "<client-id>",
        "CLIENT_SECRET": "<client-secret>",
        "TOKEN_ENDPOINT": "<token-endpoint>"
      }
    }
  }
}
```

## Verification Steps

### 1. Verify VPC Resources

```bash
# Check VPC
aws ec2 describe-vpcs \
  --filters "Name=tag:Name,Values=payermax-mcp-vpc" \
  --region us-west-2

# Check VPC Endpoints
aws ec2 describe-vpc-endpoints \
  --filters "Name=vpc-id,Values=<vpc-id>" \
  --region us-west-2
```

### 2. Verify Lambda Function

```bash
# Get Lambda function
aws lambda get-function \
  --function-name payermax-mcp-gateway-lambda \
  --region us-west-2

# View Lambda logs
aws logs tail /aws/lambda/payermax-mcp-gateway-lambda \
  --follow \
  --region us-west-2
```

### 3. Verify OpenSearch Collection

```bash
# Get collection status
aws opensearchserverless get-collection \
  --id <collection-id> \
  --region us-west-2

# Check index
curl -X GET "https://<opensearch-endpoint>/payermax-docs/_search" \
  --aws-sigv4 "aws:amz:us-west-2:aoss" \
  --user "$AWS_ACCESS_KEY_ID:$AWS_SECRET_ACCESS_KEY"
```

### 4. Verify Gateway

```bash
# Get Gateway status
aws bedrock-agentcore get-gateway \
  --gateway-identifier <gateway-id> \
  --region us-west-2

# Get Gateway Target status
aws bedrock-agentcore get-gateway-target \
  --gateway-identifier <gateway-id> \
  --gateway-target-identifier <target-id> \
  --region us-west-2
```

## Monitoring and Logging

### CloudWatch Logs

**Lambda Logs:**
```bash
aws logs tail /aws/lambda/payermax-mcp-gateway-lambda --follow
```

**View Specific Log Stream:**
```bash
aws logs get-log-events \
  --log-group-name /aws/lambda/payermax-mcp-gateway-lambda \
  --log-stream-name <stream-name>
```

### OpenSearch Metrics

```bash
# View collection metrics
aws cloudwatch get-metric-statistics \
  --namespace AWS/AOSS \
  --metric-name SearchableDocuments \
  --dimensions Name=CollectionId,Value=<collection-id> \
  --start-time 2024-01-01T00:00:00Z \
  --end-time 2024-01-02T00:00:00Z \
  --period 3600 \
  --statistics Average
```

### Lambda Metrics

```bash
# View Lambda invocations
aws cloudwatch get-metric-statistics \
  --namespace AWS/Lambda \
  --metric-name Invocations \
  --dimensions Name=FunctionName,Value=payermax-mcp-gateway-lambda \
  --start-time 2024-01-01T00:00:00Z \
  --end-time 2024-01-02T00:00:00Z \
  --period 3600 \
  --statistics Sum
```

## Troubleshooting

### Issue: VPC Deployment Failed

**Symptoms:** CloudFormation stack creation failed

**Solutions:**
- Check AWS service limits (VPCs, Elastic IPs, NAT Gateways)
- Verify IAM permissions
- Check if CIDR block conflicts with existing VPCs
- Review CloudFormation events for specific error

### Issue: OpenSearch Template Principal Array Error

**Symptoms:** CloudFormation stack creation failed with "Policy json is invalid" error about empty Principal

**Solution:**
- Fixed the OpenSearch template to use only Lambda execution role ARN
- Removed the AdditionalPrincipalArns parameter that was causing empty strings

### Issue: Lambda Package Script Path Issues

**Symptoms:** Script couldn't find files when run from project root

**Solutions:**
- Updated all deployment scripts to use correct paths from project root
- Changed `TEMPLATE_FILE="deploy/..."` to `TEMPLATE_FILE="mcp-server/deploy/..."`
- Updated package script to use `SOURCE_DIR="mcp-server"` and reference files correctly

### Issue: Missing tool_config.json

**Symptoms:** Package script failed because tool_config.json doesn't exist

**Solution:**
- Made tool_config.json optional in package script
- Creates empty JSON object if file doesn't exist

### Issue: OpenSearch Authentication Failed for Embedder

**Symptoms:** Embedder gets 401 AuthenticationException when trying to connect

**Solutions:**
1. Add current IAM user to OpenSearch data access policy
2. Temporarily change network policy to allow public access during embedding
3. Change back to VPC-only after embedding completes

**Steps to fix:**
```bash
# Get current user ARN
aws sts get-caller-identity --query 'Arn' --output text

# Update data access policy to include user
aws opensearchserverless update-access-policy \
  --name payermax-docs-access \
  --type data \
  --policy-version <version> \
  --region us-west-2 \
  --policy '[{"Rules":[...],"Principal":["<lambda-role>","<user-arn>"]}]'

# Temporarily allow public access
aws opensearchserverless update-security-policy \
  --name payermax-docs-network \
  --type network \
  --policy-version <version> \
  --region us-west-2 \
  --policy '[{"Rules":[...],"AllowFromPublic":true}]'

# Run embedder
python3 mcp-server/run_embedder.py

# Change back to VPC-only
aws opensearchserverless update-security-policy \
  --name payermax-docs-network \
  --type network \
  --policy-version <new-version> \
  --region us-west-2 \
  --policy '[{"Rules":[...],"AllowFromPublic":false,"SourceVPCEs":["<vpce-id>"]}]'
```

### Issue: Lambda Cannot Access OpenSearch

**Symptoms:** Lambda logs show connection timeout or access denied (401 error)

**Root Cause:** The default OpenSearch Serverless VPC endpoint created by CloudFormation may not work properly. A manually created VPC endpoint is required.

**Solution:**

1. **Create a new OpenSearch Serverless VPC Endpoint manually:**
```bash
# Get the OpenSearch Serverless VPC endpoint service name for your region
SERVICE_NAME=$(aws ec2 describe-vpc-endpoint-services \
  --region us-west-2 \
  --query 'ServiceNames[?contains(@, `aoss`)]' \
  --output text)

# Create VPC endpoint
aws ec2 create-vpc-endpoint \
  --vpc-id vpc-07657d7e58114b906 \
  --vpc-endpoint-type Interface \
  --service-name $SERVICE_NAME \
  --subnet-ids subnet-0a19f785d5cf68eec subnet-0101ad391342b81f9 \
  --security-group-ids sg-058e08a2878bb698c \
  --private-dns-enabled \
  --region us-west-2
```

2. **Add self-referencing rule to Security Group:**
```bash
aws ec2 authorize-security-group-ingress \
  --group-id sg-058e08a2878bb698c \
  --protocol tcp \
  --port 443 \
  --source-group sg-058e08a2878bb698c \
  --group-owner 183017937161 \
  --region us-west-2
```

3. **Update OpenSearch Network Policy to include the new VPC endpoint:**
```bash
# Get current policy version
POLICY_VERSION=$(aws opensearchserverless get-security-policy \
  --name payermax-docs-network \
  --type network \
  --region us-west-2 \
  --query 'securityPolicyDetail.policyVersion' \
  --output text)

# Update with new VPC endpoint ID
aws opensearchserverless update-security-policy \
  --name payermax-docs-network \
  --type network \
  --policy-version $POLICY_VERSION \
  --region us-west-2 \
  --policy '[{"Rules":[{"ResourceType":"collection","Resource":["collection/payermax-docs"]},{"ResourceType":"dashboard","Resource":["collection/payermax-docs"]}],"AllowFromPublic":false,"SourceVPCEs":["vpce-05f2ad77ee4a275ae","<new-vpce-id>"]}]'
```

4. **Update Data Access Policy with full permissions:**
```bash
# Get current policy version
POLICY_VERSION=$(aws opensearchserverless get-access-policy \
  --name payermax-docs-access \
  --type data \
  --region us-west-2 \
  --query 'accessPolicyDetail.policyVersion' \
  --output text)

# Update with aoss:* permissions
aws opensearchserverless update-access-policy \
  --name payermax-docs-access \
  --type data \
  --policy-version $POLICY_VERSION \
  --region us-west-2 \
  --policy '[{"Rules":[{"ResourceType":"collection","Resource":["collection/payermax-docs"],"Permission":["aoss:*"]},{"ResourceType":"index","Resource":["index/payermax-docs/*","index/payermax-api-docs/*","index/payermax-integration-guides/*"],"Permission":["aoss:*"]}],"Principal":["arn:aws:iam::183017937161:role/payermax-mcp-gateway-lambda-execution-role","arn:aws:iam::183017937161:user/jingwei"]}]'
```

**Verification Steps:**
```bash
# Check Lambda VPC configuration
aws lambda get-function-configuration \
  --function-name payermax-mcp-gateway-lambda \
  --region us-west-2 \
  --query 'VpcConfig'

# Check new VPC endpoint
aws ec2 describe-vpc-endpoints \
  --vpc-endpoint-ids <new-vpce-id> \
  --region us-west-2

# Check security group has self-referencing rule
aws ec2 describe-security-groups \
  --group-ids sg-058e08a2878bb698c \
  --region us-west-2 \
  --query 'SecurityGroups[0].IpPermissions[?FromPort==`443`]'

# Test Lambda access
aws lambda invoke \
  --function-name payermax-mcp-gateway-lambda \
  --region us-west-2 \
  --payload '{"query":"test","top_k":1}' \
  --cli-binary-format raw-in-base64-out \
  /tmp/test.json && jq . /tmp/test.json
```

**Note**: After applying these fixes, wait 2-3 minutes for the VPC endpoint to become available, then test the Lambda function.

### Issue: Gateway Authentication Failed

**Symptoms:** 401 Unauthorized error

**Solutions:**
- Verify token is not expired (tokens expire after 1 hour)
- Check client ID and secret are correct
- Verify scopes in token request match Gateway configuration
- Refresh token using `get-mcp-credentials.sh`

### Issue: Lambda Timeout

**Symptoms:** Lambda execution exceeds timeout

**Solutions:**
- Increase timeout in `lambda-template.yaml` (current: 300s)
- Optimize code performance
- Check if Bedrock API calls are slow
- Verify VPC endpoints are working (not routing through NAT)

### Issue: OpenSearch Index Not Found

**Symptoms:** Search tools return "index not found" error

**Solutions:**
- Run embedding generation: `python run_embedder.py`
- Verify `OPENSEARCH_ENDPOINT` environment variable is set
- Check OpenSearch collection is active
- Verify index name matches configuration

### Issue: High Costs

**Symptoms:** AWS bill higher than expected

**Solutions:**
- Remove NAT Gateways if not needed (saves ~$65/month)
- Reduce unused VPC endpoints
- Optimize Lambda memory allocation
- Use OpenSearch minimum OCU for dev/test
- Monitor Bedrock API usage

## Cost Optimization

### Remove NAT Gateways (Optional)

If Lambda only accesses AWS services via VPC endpoints, NAT Gateways are not needed.

**Savings:** ~$780/year per environment

**Steps:**
1. Verify Lambda doesn't need public internet access
2. Remove NAT Gateway resources from `vpc-network-cloudformation.yaml`
3. Update private route tables to remove NAT Gateway routes
4. Redeploy VPC stack

### Reduce VPC Endpoints

Remove unused VPC endpoints to save costs.

**Cost:** $7.20/month per interface endpoint

**Steps:**
1. Identify unused endpoints
2. Remove from `vpc-network-cloudformation.yaml`
3. Redeploy VPC stack

### Optimize Lambda Configuration

**Memory:** Adjust based on actual usage (current: 2048MB)
**Timeout:** Reduce if possible (current: 300s)

## Cleanup and Teardown

### Delete All Resources

```bash
# Delete Gateway Target
aws cloudformation delete-stack \
  --stack-name payermax-mcp-target-stack \
  --region us-west-2

# Delete Lambda
aws cloudformation delete-stack \
  --stack-name payermax-mcp-lambda-stack \
  --region us-west-2

# Delete OpenSearch
aws cloudformation delete-stack \
  --stack-name payermax-mcp-opensearch-stack \
  --region us-west-2

# Delete Gateway
aws cloudformation delete-stack \
  --stack-name payermax-mcp-gateway-stack \
  --region us-west-2

# Delete VPC (wait for others to complete first)
aws cloudformation delete-stack \
  --stack-name payermax-mcp-vpc-stack \
  --region us-west-2
```

**Note:** Delete in reverse order to avoid dependency issues.

## Configuration Files Reference

### network-config.json
Generated by `deploy-vpc.sh`, contains VPC configuration.

### payermax-mcp-gateway-config.json
Generated by `deploy-gateway.sh`, contains Gateway and Cognito configuration.

### payermax-mcp-lambda-config.json
Generated by `deploy-lambda.sh`, contains Lambda configuration.

### payermax-mcp-opensearch-config.json
Generated by `deploy-opensearch.sh`, contains OpenSearch configuration.

### payermax-mcp-complete-config.json
Generated by `deploy-gateway-target.sh`, contains complete deployment configuration.

## Security Best Practices

1. **VPC Isolation:** Lambda runs in private subnets with no direct internet access
2. **VPC Endpoints:** Private connectivity to AWS services
3. **Security Groups:** Restrict access to HTTPS (443) from VPC CIDR only
4. **IAM Roles:** Least privilege principle for Lambda execution role
5. **Cognito JWT:** Token-based authentication with expiration
6. **OpenSearch:** VPC-only access, no public endpoint
7. **Encryption:** Data encrypted at rest and in transit

## Support and Resources

- **Architecture Diagram:** `mcp-server/deploy/architecture-diagram.md`
- **VPC Resources:** `mcp-server/deploy/vpc-resources-list.md`
- **PayerMax Documentation:** https://developer.payermax.com
- **AWS Bedrock:** https://aws.amazon.com/bedrock/
- **OpenSearch Serverless:** https://aws.amazon.com/opensearch-service/features/serverless/

## Summary

Total deployment time: **1-2 hours** (including embedding generation)

Total monthly cost estimate:
- **Development:** ~$200-300/month
- **Production:** ~$500-700/month

Key components:
- 7 CloudFormation stacks
- 32 VPC resources
- 1 Lambda function
- 1 OpenSearch collection
- 1 Cognito User Pool
- 1 AgentCore Gateway

The infrastructure is now ready to serve MCP requests with intelligent API discovery, semantic search, and code generation capabilities.
