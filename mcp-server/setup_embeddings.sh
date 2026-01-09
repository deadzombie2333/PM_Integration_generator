#!/bin/bash

# PayerMax Document Embedder Service - Pre-Deployment Setup
# This script must be run BEFORE deploying the MCP server
# It indexes all documentation into OpenSearch Serverless for semantic search

set -e

echo "================================================================"
echo "PayerMax Document Embedder Service"
echo "Pre-Deployment Indexing Service"
echo "================================================================"
echo ""
echo "IMPORTANT: This must complete successfully before MCP deployment"
echo ""

# Check required environment variables
if [ -z "$OPENSEARCH_ENDPOINT" ]; then
    echo "✗ Error: OPENSEARCH_ENDPOINT environment variable not set"
    echo ""
    echo "Please set it to your OpenSearch Serverless endpoint:"
    echo "  export OPENSEARCH_ENDPOINT=your-collection.us-east-1.aoss.amazonaws.com"
    echo ""
    exit 1
fi

if [ -z "$AWS_REGION" ]; then
    echo "⚠ Warning: AWS_REGION not set, using default: us-east-1"
    export AWS_REGION=us-east-1
fi

echo "Configuration:"
echo "  OpenSearch Endpoint: $OPENSEARCH_ENDPOINT"
echo "  AWS Region: $AWS_REGION"
echo "  Index Name: ${OPENSEARCH_INDEX:-payermax-docs}"
echo ""

# Check AWS credentials
echo "Checking AWS credentials..."
if ! aws sts get-caller-identity > /dev/null 2>&1; then
    echo "✗ Error: AWS credentials not configured"
    echo ""
    echo "Please configure AWS credentials:"
    echo "  aws configure"
    echo "  OR"
    echo "  export AWS_ACCESS_KEY_ID=your_key"
    echo "  export AWS_SECRET_ACCESS_KEY=your_secret"
    echo ""
    exit 1
fi
echo "✓ AWS credentials configured"
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install -q -r requirements.txt
echo "✓ Dependencies installed"
echo ""

# Run embedder service
echo "Starting Document Embedder Service..."
echo "This will:"
echo "  1. Verify all prerequisites"
echo "  2. Create OpenSearch index"
echo "  3. Index all documentation (30-60 minutes)"
echo "  4. Generate embeddings for semantic search"
echo ""
echo "Press Ctrl+C to cancel, or wait 5 seconds to continue..."
sleep 5
echo ""

python -m tools.document_embedder "$@"

exit_code=$?

if [ $exit_code -eq 0 ]; then
    echo ""
    echo "================================================================"
    echo "✓ Pre-Deployment Indexing Complete"
    echo "================================================================"
    echo ""
    echo "You can now deploy the MCP server:"
    echo "  python api_docs_server.py"
    echo ""
    echo "Or configure it in Kiro IDE:"
    echo "  .kiro/settings/mcp.json"
    echo ""
else
    echo ""
    echo "================================================================"
    echo "✗ Pre-Deployment Indexing Failed"
    echo "================================================================"
    echo ""
    echo "Please fix the errors above and try again."
    echo ""
    exit $exit_code
fi
