#!/bin/bash

# Package and Deploy PayerMax MCP Server to Lambda

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

REGION="us-west-2"
FUNCTION_NAME="payermax-mcp-gateway-lambda"
PACKAGE_DIR="lambda-package"
SOURCE_DIR=".."

echo -e "${GREEN}Starting Lambda package creation...${NC}"

# Clean up old package
if [ -d "$PACKAGE_DIR" ]; then
    echo "Cleaning up old package directory..."
    rm -rf $PACKAGE_DIR
fi

# Create package directory
echo "Creating package directory..."
mkdir -p $PACKAGE_DIR

# Copy MCP server files
echo "Copying MCP server files..."
cp $SOURCE_DIR/api_docs_server.py $PACKAGE_DIR/
if [ -f "$SOURCE_DIR/tool_config.json" ]; then
    cp $SOURCE_DIR/tool_config.json $PACKAGE_DIR/
else
    echo "{}" > $PACKAGE_DIR/tool_config.json
fi
cp -r $SOURCE_DIR/tools $PACKAGE_DIR/
cp -r $SOURCE_DIR/api-docs $PACKAGE_DIR/
cp -r $SOURCE_DIR/api-samples $PACKAGE_DIR/
cp -r $SOURCE_DIR/integration_process $PACKAGE_DIR/
cp -r $SOURCE_DIR/payermax_doc $PACKAGE_DIR/

# Install dependencies
echo "Installing Python dependencies for Lambda (Amazon Linux)..."
pip install --target $PACKAGE_DIR \
    --platform manylinux2014_x86_64 \
    --implementation cp \
    --python-version 3.11 \
    --only-binary=:all: \
    --upgrade \
    fastmcp \
    boto3 \
    opensearch-py \
    requests \
    requests-aws4auth

# Create Lambda handler wrapper
echo "Creating Lambda handler..."
cat > $PACKAGE_DIR/lambda_handler.py << 'EOF'
"""
Lambda handler for PayerMax MCP Server
Wraps the FastMCP server for Lambda execution via AgentCore Gateway
"""
import json
import os
import sys
import traceback
from pathlib import Path

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

# Initialize tools globally (outside handler for reuse)
BASE_PATH = Path(__file__).parent
CONFIG_PATH = BASE_PATH / "tool_config.json"

# Load configuration
def load_config():
    try:
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Warning: Could not load config: {e}")
        return {}

CONFIG = load_config()

# Initialize tools
from tools import (
    APIEndpointFinder,
    IntegrationAssistant,
    APIDocumentationSearch,
    IntegrationGuideSearch
)

api_endpoint_finder = APIEndpointFinder(BASE_PATH, CONFIG)
integration_assistant = IntegrationAssistant(BASE_PATH, CONFIG)

# Initialize OpenSearch-based tools
try:
    api_documentation_search = APIDocumentationSearch(BASE_PATH, CONFIG)
    integration_guide_search = IntegrationGuideSearch(BASE_PATH, CONFIG)
except Exception as e:
    print(f"Warning: Could not initialize OpenSearch tools: {e}")
    api_documentation_search = None
    integration_guide_search = None

def handler(event, context):
    """
    Lambda handler that processes MCP requests from AgentCore Gateway
    AgentCore Gateway sends tool arguments directly in the event
    """
    try:
        # Log the incoming event for debugging
        print(f"Received event: {json.dumps(event)}")
        
        # AgentCore Gateway sends arguments directly
        arguments = event if isinstance(event, dict) else json.loads(event)
        
        # Determine which tool based on the arguments present
        result = None
        
        if 'task_type' in arguments:
            # Tool 1: find_api_endpoint
            print("Calling APIEndpointFinder.find_endpoint")
            result = api_endpoint_finder.find_endpoint(**arguments)
            
        elif 'user_description' in arguments:
            # Tool 2: get_integration_recommendation
            print("Calling IntegrationAssistant.analyze_requirements")
            result = integration_assistant.analyze_requirements(**arguments)
            
        elif 'query' in arguments:
            # Tool 3 or 4: search tools
            # Check if this is for integration guides (Tool 4)
            if arguments.get('doc_type_filter') == 'integration_guide' or arguments.get('search_integration_guides'):
                print("Calling IntegrationGuideSearch.search")
                if integration_guide_search:
                    result = integration_guide_search.search(**arguments)
                else:
                    result = {
                        'error': 'OpenSearch not configured',
                        'message': 'OPENSEARCH_ENDPOINT environment variable not set'
                    }
            else:
                # Default to API documentation search (Tool 3)
                print("Calling APIDocumentationSearch.search")
                if api_documentation_search:
                    result = api_documentation_search.search(**arguments)
                else:
                    result = {
                        'error': 'OpenSearch not configured',
                        'message': 'OPENSEARCH_ENDPOINT environment variable not set'
                    }
        else:
            error_msg = f'Cannot determine tool from arguments: {list(arguments.keys())}'
            print(error_msg)
            return {
                'error': error_msg,
                'available_tools': ['find_api_endpoint', 'get_integration_recommendation', 'search_api_documentation', 'search_integration_guides']
            }
        
        print(f"Result type: {type(result)}")
        print(f"Result keys: {list(result.keys()) if isinstance(result, dict) else 'not a dict'}")
        
        # Return the result directly (AgentCore Gateway handles MCP formatting)
        return result
    
    except Exception as e:
        error_msg = f"Error: {str(e)}\n{traceback.format_exc()}"
        print(error_msg)
        return {
            'error': str(e),
            'traceback': traceback.format_exc()
        }
EOF

# Create deployment package
echo "Creating deployment package..."
cd $PACKAGE_DIR
zip -r ../../lambda-deployment.zip . -q
cd ../../

echo -e "${GREEN}Package created: lambda-deployment.zip${NC}"

# Get package size
PACKAGE_SIZE=$(du -h lambda-deployment.zip | cut -f1)
echo "Package size: $PACKAGE_SIZE"

# Check if package is too large for direct upload (50MB limit)
PACKAGE_SIZE_BYTES=$(stat -f%z lambda-deployment.zip 2>/dev/null || stat -c%s lambda-deployment.zip 2>/dev/null)
if [ $PACKAGE_SIZE_BYTES -gt 52428800 ]; then
    echo -e "${YELLOW}Package is larger than 50MB, uploading to S3...${NC}"
    
    # Create S3 bucket if it doesn't exist
    BUCKET_NAME="payermax-mcp-lambda-deployments-${AWS_ACCOUNT_ID:-$(aws sts get-caller-identity --query Account --output text)}"
    
    if ! aws s3 ls "s3://$BUCKET_NAME" 2>/dev/null; then
        echo "Creating S3 bucket: $BUCKET_NAME"
        aws s3 mb "s3://$BUCKET_NAME" --region $REGION
    fi
    
    # Upload to S3
    echo "Uploading to S3..."
    aws s3 cp lambda-deployment.zip "s3://$BUCKET_NAME/lambda-deployment.zip"
    
    # Update Lambda function from S3
    echo "Updating Lambda function from S3..."
    aws lambda update-function-code \
        --function-name $FUNCTION_NAME \
        --s3-bucket $BUCKET_NAME \
        --s3-key lambda-deployment.zip \
        --region $REGION
else
    # Update Lambda function directly
    echo "Updating Lambda function..."
    aws lambda update-function-code \
        --function-name $FUNCTION_NAME \
        --zip-file fileb://lambda-deployment.zip \
        --region $REGION
fi

# Wait for update to complete
echo "Waiting for Lambda update to complete..."
aws lambda wait function-updated \
    --function-name $FUNCTION_NAME \
    --region $REGION

# Update handler
echo "Updating Lambda handler configuration..."
aws lambda update-function-configuration \
    --function-name $FUNCTION_NAME \
    --handler lambda_handler.handler \
    --region $REGION

# Update environment variables to include Tool 3 and Tool 4 indices
echo "Updating Lambda environment variables..."
OPENSEARCH_ENDPOINT=$(jq -r '.collection_host // ""' payermax-mcp-opensearch-config.json)
if [ -n "$OPENSEARCH_ENDPOINT" ]; then
    aws lambda update-function-configuration \
        --function-name $FUNCTION_NAME \
        --region $REGION \
        --environment "Variables={OPENSEARCH_ENDPOINT=$OPENSEARCH_ENDPOINT,REGION=$REGION,TOOL_3_INDEX=payermax-api-docs,TOOL_4_INDEX=payermax-integration-guides}" \
        > /dev/null
    echo "✓ Environment variables updated with OpenSearch configuration"
fi

echo -e "\n${GREEN}✅ Lambda deployment completed!${NC}"
echo ""
echo "Function: $FUNCTION_NAME"
echo "Region: $REGION"
echo "Handler: lambda_handler.handler"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "1. Test the Lambda function"
echo "2. Test the Gateway connection"
echo "3. Delete old OpenSearch stack in us-east-1"
