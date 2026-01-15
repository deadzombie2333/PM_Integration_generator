#!/bin/bash

# PayerMax MCP VPC Network CloudFormation Deployment Script
# This script deploys the VPC infrastructure using CloudFormation

STACK_NAME="payermax-mcp-vpc-stack"
TEMPLATE_FILE="mcp-server/deploy/vpc-network-cloudformation.yaml"
REGION=${AWS_REGION:-us-west-2}
VPC_NAME="payermax-mcp"

# Check for required dependencies
if ! command -v jq &> /dev/null; then
    echo "❌ jq is required but not installed. Please install jq first:"
    echo "   macOS: brew install jq"
    echo "   Ubuntu/Debian: sudo apt-get install jq"
    echo "   CentOS/RHEL: sudo yum install jq"
    exit 1
fi

if ! command -v aws &> /dev/null; then
    echo "❌ AWS CLI is required but not installed. Please install AWS CLI first."
    exit 1
fi

echo "🚀 Deploying PayerMax MCP VPC Network Infrastructure..."
echo "Stack Name: $STACK_NAME"
echo "Region: $REGION"
echo "VPC Name: $VPC_NAME"
echo "Template: $TEMPLATE_FILE"
echo ""

# Deploy the stack
echo "📦 Deploying CloudFormation stack..."
aws cloudformation deploy \
    --template-file $TEMPLATE_FILE \
    --stack-name $STACK_NAME \
    --parameter-overrides \
        VpcName=$VPC_NAME \
        VpcCidr=10.0.0.0/16 \
        AvailabilityZone1=${REGION}a \
        AvailabilityZone2=${REGION}b \
    --capabilities CAPABILITY_NAMED_IAM \
    --region $REGION

# Check deployment status
if [ $? -eq 0 ]; then
    echo "✅ Stack deployment completed successfully!"
    echo ""
    echo "📋 Stack Outputs:"
    aws cloudformation describe-stacks \
        --stack-name $STACK_NAME \
        --region $REGION \
        --query 'Stacks[0].Outputs[*].[OutputKey,OutputValue]' \
        --output table
    
    echo ""
    echo "📝 Exporting deployment results to network-config.json..."
    
    # Backup existing network-config.json if it exists
    if [ -f "network-config.json" ]; then
        cp network-config.json "network-config.json.backup.$(date +%Y%m%d_%H%M%S)"
        echo "📋 Backed up existing network-config.json"
    fi
    
    # Get stack outputs in JSON format
    OUTPUTS=$(aws cloudformation describe-stacks \
        --stack-name $STACK_NAME \
        --region $REGION \
        --query 'Stacks[0].Outputs' \
        --output json)
    
    # Extract values using jq (with error handling)
    if [ -z "$OUTPUTS" ] || [ "$OUTPUTS" = "null" ]; then
        echo "❌ Failed to retrieve stack outputs"
        exit 1
    fi
    
    VPC_ID=$(echo $OUTPUTS | jq -r '.[] | select(.OutputKey=="VPCId") | .OutputValue // "null"')
    # VPC_NAME is from the parameter, not outputs
    
    # Subnets
    PUBLIC_SUBNET_1=$(echo $OUTPUTS | jq -r '.[] | select(.OutputKey=="PublicSubnet1Id") | .OutputValue')
    PUBLIC_SUBNET_2=$(echo $OUTPUTS | jq -r '.[] | select(.OutputKey=="PublicSubnet2Id") | .OutputValue')
    PRIVATE_SUBNET_1=$(echo $OUTPUTS | jq -r '.[] | select(.OutputKey=="PrivateSubnet1Id") | .OutputValue')
    PRIVATE_SUBNET_2=$(echo $OUTPUTS | jq -r '.[] | select(.OutputKey=="PrivateSubnet2Id") | .OutputValue')
    
    # NAT Gateways
    NAT_GATEWAY_1=$(echo $OUTPUTS | jq -r '.[] | select(.OutputKey=="NATGateway1Id") | .OutputValue')
    NAT_GATEWAY_2=$(echo $OUTPUTS | jq -r '.[] | select(.OutputKey=="NATGateway2Id") | .OutputValue')
    
    # Security Group
    SECURITY_GROUP=$(echo $OUTPUTS | jq -r '.[] | select(.OutputKey=="SecurityGroupId") | .OutputValue')
    
    # VPC Endpoints
    S3_ENDPOINT=$(echo $OUTPUTS | jq -r '.[] | select(.OutputKey=="S3GatewayEndpointId") | .OutputValue')
    ECR_DOCKER_ENDPOINT=$(echo $OUTPUTS | jq -r '.[] | select(.OutputKey=="ECRDockerEndpointId") | .OutputValue')
    ECR_API_ENDPOINT=$(echo $OUTPUTS | jq -r '.[] | select(.OutputKey=="ECRAPIEndpointId") | .OutputValue')
    LOGS_ENDPOINT=$(echo $OUTPUTS | jq -r '.[] | select(.OutputKey=="LogsEndpointId") | .OutputValue')
    SSM_ENDPOINT=$(echo $OUTPUTS | jq -r '.[] | select(.OutputKey=="SSMEndpointId") | .OutputValue')
    SSM_MESSAGES_ENDPOINT=$(echo $OUTPUTS | jq -r '.[] | select(.OutputKey=="SSMMessagesEndpointId") | .OutputValue')
    EC2_MESSAGES_ENDPOINT=$(echo $OUTPUTS | jq -r '.[] | select(.OutputKey=="EC2MessagesEndpointId") | .OutputValue')
    BEDROCK_ENDPOINT=$(echo $OUTPUTS | jq -r '.[] | select(.OutputKey=="BedrockEndpointId") | .OutputValue')
    BEDROCK_RUNTIME_ENDPOINT=$(echo $OUTPUTS | jq -r '.[] | select(.OutputKey=="BedrockRuntimeEndpointId") | .OutputValue')
    BEDROCK_AGENT_ENDPOINT=$(echo $OUTPUTS | jq -r '.[] | select(.OutputKey=="BedrockAgentEndpointId") | .OutputValue')
    BEDROCK_AGENT_RUNTIME_ENDPOINT=$(echo $OUTPUTS | jq -r '.[] | select(.OutputKey=="BedrockAgentRuntimeEndpointId") | .OutputValue')
    BEDROCK_AGENT_CORE_ENDPOINT=$(echo $OUTPUTS | jq -r '.[] | select(.OutputKey=="BedrockAgentCoreEndpointId") | .OutputValue')
    BEDROCK_AGENT_CORE_GATEWAY_ENDPOINT=$(echo $OUTPUTS | jq -r '.[] | select(.OutputKey=="BedrockAgentCoreGatewayEndpointId") | .OutputValue')
    LAMBDA_ENDPOINT=$(echo $OUTPUTS | jq -r '.[] | select(.OutputKey=="LambdaEndpointId") | .OutputValue')
    COGNITO_ENDPOINT=$(echo $OUTPUTS | jq -r '.[] | select(.OutputKey=="CognitoEndpointId") | .OutputValue')
    OPENSEARCH_ENDPOINT=$(echo $OUTPUTS | jq -r '.[] | select(.OutputKey=="OpenSearchServerlessEndpointId") | .OutputValue')
    
    # Validate required values
    if [ "$VPC_ID" = "null" ] || [ -z "$VPC_ID" ]; then
        echo "❌ Failed to retrieve VPC ID from stack outputs"
        exit 1
    fi
    
    echo "🔍 Retrieved VPC ID: $VPC_ID"
    
    # Get route table IDs by describing subnets
    PUBLIC_RT=$(aws ec2 describe-route-tables \
        --filters "Name=association.subnet-id,Values=$PUBLIC_SUBNET_1" \
        --region $REGION \
        --query 'RouteTables[0].RouteTableId' \
        --output text)
    
    PRIVATE_RT_1=$(aws ec2 describe-route-tables \
        --filters "Name=association.subnet-id,Values=$PRIVATE_SUBNET_1" \
        --region $REGION \
        --query 'RouteTables[0].RouteTableId' \
        --output text)
    
    PRIVATE_RT_2=$(aws ec2 describe-route-tables \
        --filters "Name=association.subnet-id,Values=$PRIVATE_SUBNET_2" \
        --region $REGION \
        --query 'RouteTables[0].RouteTableId' \
        --output text)
    
    # Get Elastic IP allocation IDs
    EIP_1=$(aws ec2 describe-nat-gateways \
        --nat-gateway-ids $NAT_GATEWAY_1 \
        --region $REGION \
        --query 'NatGateways[0].NatGatewayAddresses[0].AllocationId' \
        --output text)
    
    EIP_2=$(aws ec2 describe-nat-gateways \
        --nat-gateway-ids $NAT_GATEWAY_2 \
        --region $REGION \
        --query 'NatGateways[0].NatGatewayAddresses[0].AllocationId' \
        --output text)
    
    # Create the network-config.json file
    cat > network-config.json << EOF
{
  "_metadata": {
    "generated_from": "$STACK_NAME",
    "generated_on": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
    "region": "$REGION"
  },
  "vpc_id": "$VPC_ID",
  "vpc_name": "$VPC_NAME",
  "nat_config": [
    "$NAT_GATEWAY_1",
    "$NAT_GATEWAY_2"
  ],
  "sg_config": [
    "$SECURITY_GROUP"
  ],
  "subnet_config": {
    "Public-us-west-2a": {
      "subnet_id": "$PUBLIC_SUBNET_1",
      "rt_id": "$PUBLIC_RT",
      "elastic_ip_id": "$EIP_1"
    },
    "Public-us-west-2b": {
      "subnet_id": "$PUBLIC_SUBNET_2",
      "rt_id": "$PUBLIC_RT",
      "elastic_ip_id": "$EIP_2"
    },
    "Private-us-west-2a": {
      "subnet_id": "$PRIVATE_SUBNET_1",
      "rt_id": "$PRIVATE_RT_1"
    },
    "Private-us-west-2b": {
      "subnet_id": "$PRIVATE_SUBNET_2",
      "rt_id": "$PRIVATE_RT_2"
    }
  },
  "vpc_endpoints": {
    "s3_gateway": "$S3_ENDPOINT",
    "ecr_docker": "$ECR_DOCKER_ENDPOINT",
    "ecr_api": "$ECR_API_ENDPOINT",
    "logs": "$LOGS_ENDPOINT",
    "ssm": "$SSM_ENDPOINT",
    "ssm_messages": "$SSM_MESSAGES_ENDPOINT",
    "ec2_messages": "$EC2_MESSAGES_ENDPOINT",
    "bedrock": "$BEDROCK_ENDPOINT",
    "bedrock_runtime": "$BEDROCK_RUNTIME_ENDPOINT",
    "bedrock_agent": "$BEDROCK_AGENT_ENDPOINT",
    "bedrock_agent_runtime": "$BEDROCK_AGENT_RUNTIME_ENDPOINT",
    "bedrock_agent_core": "$BEDROCK_AGENT_CORE_ENDPOINT",
    "bedrock_agent_core_gateway": "$BEDROCK_AGENT_CORE_GATEWAY_ENDPOINT",
    "lambda": "$LAMBDA_ENDPOINT",
    "cognito": "$COGNITO_ENDPOINT",
    "opensearch_serverless": "$OPENSEARCH_ENDPOINT"
  }
}
EOF
    
    echo "✅ Network configuration exported to network-config.json"
    
    # Validate the generated JSON
    if command -v python3 &> /dev/null; then
        python3 -c "
import json
try:
    with open('network-config.json', 'r') as f:
        json.load(f)
    print('✅ Generated JSON is valid')
except Exception as e:
    print(f'❌ Generated JSON is invalid: {e}')
    exit(1)
" || echo "⚠️  Could not validate JSON format"
    elif command -v jq &> /dev/null; then
        if jq empty network-config.json 2>/dev/null; then
            echo "✅ Generated JSON is valid"
        else
            echo "❌ Generated JSON is invalid"
        fi
    fi
    
    echo "📁 File contents:"
    cat network-config.json
    
    echo ""
    echo "📊 Export Summary:"
    echo "   Format: JSON"
    echo "   VPC ID: $VPC_ID"
    echo "   Subnets: 4 (2 public, 2 private)"
    echo "   NAT Gateways: 2"
    echo "   Security Groups: 1"
    echo "   VPC Endpoints: 16 (including OpenSearch Serverless)"
    echo ""
    echo "🎉 Network configuration successfully exported to network-config.json!"
    echo ""
    echo "💡 Next step: Deploy OpenSearch Serverless"
    echo "   First deploy Lambda to get execution role ARN, then:"
    echo "   ./deploy/deploy-opensearch.sh"
    
else
    echo "❌ Stack deployment failed!"
    exit 1
fi