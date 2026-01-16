#!/bin/bash

# PayerMax MCP Gateway Deployment Script
# Deploy AgentCore Gateway with Cognito OAuth authentication

set -e

# Configuration
STACK_NAME="payermax-mcp-gateway-stack"
TEMPLATE_FILE="gateway-template.yaml"
REGION=${AWS_REGION:-us-west-2}
GATEWAY_NAME="payermax-mcp-gateway"
DOMAIN_PREFIX="payermax-mcp-auth"
RESOURCE_SERVER_ID="payermax-mcp"

echo "🚀 Deploying PayerMax MCP Gateway Stack..."
echo "   Stack Name: $STACK_NAME"
echo "   Region: $REGION"
echo "   Gateway Name: $GATEWAY_NAME"
echo "   Domain Prefix: $DOMAIN_PREFIX"
echo "   Resource Server: $RESOURCE_SERVER_ID"

# Deploy the stack
echo "⏳ Deploying CloudFormation stack..."
aws cloudformation deploy \
    --template-file "$TEMPLATE_FILE" \
    --stack-name "$STACK_NAME" \
    --parameter-overrides \
        GatewayName="$GATEWAY_NAME" \
        DomainPrefix="$DOMAIN_PREFIX" \
        ResourceServerIdentifier="$RESOURCE_SERVER_ID" \
    --region "$REGION" \
    --capabilities CAPABILITY_NAMED_IAM

# Get outputs
echo "📋 Getting stack outputs..."
OUTPUTS=$(aws cloudformation describe-stacks \
    --stack-name "$STACK_NAME" \
    --region "$REGION" \
    --query 'Stacks[0].Outputs')

echo "✅ Stack deployment completed!"
echo "📋 Outputs:"
echo "$OUTPUTS" | jq -r '.[] | "   • \(.OutputKey): \(.OutputValue)"'

# Extract key values
GATEWAY_ID=$(echo "$OUTPUTS" | jq -r '.[] | select(.OutputKey=="AgentCoreGatewayId") | .OutputValue')
GATEWAY_URL=$(echo "$OUTPUTS" | jq -r '.[] | select(.OutputKey=="AgentCoreGatewayUrl") | .OutputValue')
CLIENT_ID=$(echo "$OUTPUTS" | jq -r '.[] | select(.OutputKey=="ClientId") | .OutputValue')
USER_POOL_ID=$(echo "$OUTPUTS" | jq -r '.[] | select(.OutputKey=="CognitoUserPoolId") | .OutputValue')
TOKEN_ENDPOINT=$(echo "$OUTPUTS" | jq -r '.[] | select(.OutputKey=="TokenEndpoint") | .OutputValue')
REQUIRED_SCOPES=$(echo "$OUTPUTS" | jq -r '.[] | select(.OutputKey=="RequiredScopes") | .OutputValue')
JWT_ISSUER=$(echo "$OUTPUTS" | jq -r '.[] | select(.OutputKey=="JwtIssuer") | .OutputValue')
COGNITO_DOMAIN=$(echo "$OUTPUTS" | jq -r '.[] | select(.OutputKey=="CognitoDomainName") | .OutputValue')

echo ""
echo "🔑 Getting client secret..."
CLIENT_SECRET=$(aws cognito-idp describe-user-pool-client \
    --user-pool-id "$USER_POOL_ID" \
    --client-id "$CLIENT_ID" \
    --region "$REGION" \
    --query 'UserPoolClient.ClientSecret' \
    --output text)

echo "✅ Client secret retrieved!"

# Create gateway configuration file
echo ""
echo "📝 Creating gateway configuration file..."

cat > payermax-mcp-gateway-config.json << EOF
{
  "region": "$REGION",
  "gateway_stack_name": "$STACK_NAME",
  "gateway_name": "$GATEWAY_NAME",
  "gateway_id": "$GATEWAY_ID",
  "gateway_url": "$GATEWAY_URL",
  "pool_id": "$USER_POOL_ID",
  "client_id": "$CLIENT_ID",
  "client_secret": "$CLIENT_SECRET",
  "token_endpoint": "$TOKEN_ENDPOINT",
  "cognito_domain": "$COGNITO_DOMAIN",
  "scopes": "$REQUIRED_SCOPES",
  "jwt_issuer": "$JWT_ISSUER",
  "discovery_url": "https://cognito-idp.$REGION.amazonaws.com/$USER_POOL_ID/.well-known/openid-configuration",
  "authorizer_config": {
    "jwtConfiguration": {
      "issuer": "$JWT_ISSUER",
      "audience": ["$CLIENT_ID"]
    }
  }
}
EOF

echo "✅ Configuration file created: payermax-mcp-gateway-config.json"

echo ""
echo "🎉 PayerMax MCP Gateway deployment finished!"
echo ""
echo "📋 Summary:"
echo "   • Gateway ID: $GATEWAY_ID"
echo "   • Gateway URL: $GATEWAY_URL"
echo "   • Client ID: $CLIENT_ID"
echo "   • Token Endpoint: $TOKEN_ENDPOINT"
echo "   • Scopes: $REQUIRED_SCOPES"
echo "   • Cognito Domain: $COGNITO_DOMAIN"
echo ""
echo "💡 Next steps:"
echo "   1. Update Lambda with Cognito configuration (if Lambda was deployed first)"
echo "   2. Deploy Gateway Target: ./deploy-gateway-target.sh"
echo ""
echo "🔧 Configuration saved to: payermax-mcp-gateway-config.json"