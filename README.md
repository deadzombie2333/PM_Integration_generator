# PayerMax Integration Generator

An intelligent AI-powered system for PayerMax payment integration that combines MCP (Model Context Protocol) server with AWS infrastructure to provide semantic search, API recommendations, and code generation capabilities.

## 🎯 Project Overview

This project provides two main components:

1. **MCP Server**: An intelligent documentation server with LLM-powered API discovery and semantic search
2. **Kiro Power**: A code generation power for Kiro IDE that helps developers generate PayerMax integration code
3. **AWS Infrastructure**: Scalable cloud deployment with VPC isolation, Bedrock AI, and OpenSearch

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Client Applications                       │
│              (Kiro IDE, CLI, Web Clients)                   │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTPS + JWT Auth
                         ↓
┌─────────────────────────────────────────────────────────────┐
│         AWS Bedrock AgentCore Gateway (Public)              │
│              - Cognito JWT Authentication                    │
│              - MCP Protocol Handler                          │
└────────────────────────┬────────────────────────────────────┘
                         │ Invokes
                         ↓
┌─────────────────────────────────────────────────────────────┐
│              Lambda Function (Private VPC)                   │
│         - MCP Server (FastMCP)                              │
│         - 4 Intelligent Tools                               │
│         - Python 3.11, 2048MB, 5min timeout                 │
└─────┬───────────────────┬───────────────────┬───────────────┘
      │                   │                   │
      │ VPC Endpoints     │                   │
      ↓                   ↓                   ↓
┌──────────┐      ┌──────────────┐    ┌─────────────────┐
│ Bedrock  │      │  OpenSearch  │    │  CloudWatch     │
│ Runtime  │      │  Serverless  │    │  Logs           │
│ (AI)     │      │  (Search)    │    │  (Monitoring)   │
└──────────┘      └──────────────┘    └─────────────────┘
```

## 📦 Project Structure

```
.
├── mcp-server/                      # MCP Server Implementation
│   ├── api_docs_server.py          # Main MCP server with 4 tools
│   ├── tools/                       # Tool implementations
│   │   ├── api_endpoint_finder.py  # Tool 1: API Endpoint Finder
│   │   ├── integration_assistant.py # Tool 2: Integration Assistant
│   │   ├── api_documentation_search.py # Tool 3: API Doc Search
│   │   └── integration_guide_search.py # Tool 4: Integration Guide Search
│   ├── api-docs/                    # PayerMax API specifications
│   ├── api-samples/                 # API code samples
│   ├── integration_process/         # Integration guides
│   ├── payermax_doc/               # PayerMax product documentation
│   ├── document_embedder/          # Embedding generation scripts
│   ├── deploy/                     # AWS CloudFormation templates
│   │   ├── vpc-network-cloudformation.yaml
│   │   ├── gateway-template.yaml
│   │   ├── lambda-template.yaml
│   │   ├── opensearch-template.yaml
│   │   └── architecture-diagram.md
│   └── tool_config.json            # Tool configuration
│
├── powers/                         # Kiro Power for Code Generation
│   ├── payermax-codegen/          # Power implementation
│   ├── config.py                  # PayerMax configuration
│   ├── payermax_client.py         # PayerMax client library
│   ├── payment_create.py          # Payment creation
│   ├── payment_query.py           # Payment query
│   ├── refund_request.py          # Refund operations
│   └── frontend_integration.html  # Frontend example
│
└── README.md                      # This file
```

## 🚀 Features

### MCP Server (4 Intelligent Tools)

#### Tool 1: API Endpoint Finder
- **Purpose**: Find the correct API endpoint using structured parameters
- **Technology**: AWS Bedrock Nova LLM for intelligent API selection
- **Input**: Task type, payment type, integration mode
- **Output**: API specification, sample code, reasoning, alternatives

#### Tool 2: Integration Assistant
- **Purpose**: Analyze requirements and recommend integration methods
- **Technology**: AWS Bedrock Nova LLM for requirement analysis
- **Input**: Natural language description of requirements
- **Output**: Recommended method, step-by-step guide, required APIs

#### Tool 3: API Documentation Search
- **Purpose**: Semantic search across API specifications and samples
- **Technology**: AWS Bedrock Titan Embeddings + OpenSearch Serverless
- **Input**: Natural language query
- **Output**: Relevant API docs with relevance scores

#### Tool 4: Integration Guide Search
- **Purpose**: Semantic search across integration guides and workflows
- **Technology**: AWS Bedrock Titan Embeddings + OpenSearch Serverless
- **Input**: Natural language query
- **Output**: Relevant integration guides with relevance scores

### Kiro Power: PayerMax Code Generator

- Generate PayerMax API integration code
- Support for multiple payment methods
- Request/response handling
- Signature generation and verification
- Error handling

## 🛠️ Technology Stack

### Backend
- **FastMCP**: MCP server framework
- **Python 3.11**: Runtime environment
- **boto3**: AWS SDK for Python
- **opensearch-py**: OpenSearch client

### AWS Services
- **Bedrock Runtime**: AI model inference (Nova, Titan)
- **OpenSearch Serverless**: Vector search for embeddings
- **Lambda**: Serverless compute
- **VPC**: Network isolation
- **Cognito**: Authentication
- **CloudWatch**: Logging and monitoring

### Infrastructure
- **CloudFormation**: Infrastructure as Code
- **VPC Endpoints**: Private AWS service connectivity (18 endpoints)
- **NAT Gateways**: Outbound internet access (if needed)
- **Security Groups**: Network access control

## 📋 Prerequisites

### For Local Development
- Python 3.11+
- AWS CLI configured
- OpenSearch endpoint (for Tools 3 & 4)

### For AWS Deployment
- AWS Account with appropriate permissions
- VPC with private subnets
- Cognito User Pool
- OpenSearch Serverless collection

## 🔧 Installation & Setup

### 1. Local Development Setup

```bash
# Clone the repository
git clone <repository-url>
cd PM_Integration_generator

# Install MCP server dependencies
cd mcp-server
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Set environment variables
export OPENSEARCH_ENDPOINT="your-opensearch-endpoint"
export OPENSEARCH_INDEX="payermax-docs"
export AWS_REGION="us-west-2"

# Run the MCP server locally
python api_docs_server.py
```

### 2. Generate Embeddings (for Tools 3 & 4)

```bash
# Run the embedding generation script
cd mcp-server
python run_embedder.py

# Or use the shell script
./setup_embeddings.sh
```

### 3. AWS Deployment

#### Step 1: Deploy VPC Infrastructure

```bash
cd mcp-server/deploy

# Deploy VPC with endpoints
./deploy-vpc.sh
```

This creates:
- VPC with 2 public and 2 private subnets
- 2 NAT Gateways (optional, can be removed if not needed)
- 18 VPC Endpoints (S3, ECR, Bedrock, OpenSearch, etc.)
- Security Group for VPC endpoints

#### Step 2: Deploy Gateway with Cognito

```bash
# Deploy AgentCore Gateway with Cognito authentication
./deploy-gateway.sh
```

This creates:
- Cognito User Pool
- Cognito App Client
- AgentCore Gateway (public endpoint)
- IAM roles and policies

#### Step 3: Deploy OpenSearch Collection

```bash
# Deploy OpenSearch Serverless collection
./deploy-opensearch.sh
```

This creates:
- OpenSearch Serverless collection (VECTORSEARCH)
- Encryption, network, and data access policies
- VPC-only access configuration

#### Step 4: Deploy Lambda Function

```bash
# Package and deploy Lambda function
./package-lambda.sh
./deploy-lambda.sh
```

This creates:
- Lambda function in private subnets
- IAM execution role with necessary permissions
- Environment variables configuration

## 🔐 Authentication

The MCP server uses Cognito JWT authentication:

1. **Get Access Token**:
```bash
# Use the refresh script
./refresh-mcp-token.sh
```

2. **Use Token in Requests**:
```bash
curl -H "Authorization: Bearer <access_token>" \
     https://<gateway-url>/mcp
```

## 📊 AWS Resources

### VPC Resources (32 total)
- 1 VPC (10.0.0.0/16)
- 1 Internet Gateway
- 4 Subnets (2 public, 2 private)
- 2 NAT Gateways + 2 Elastic IPs
- 3 Route Tables
- 1 Security Group
- 18 VPC Endpoints (1 Gateway, 17 Interface)

### Compute & Storage
- 1 Lambda Function (2048MB, 5min timeout)
- 1 OpenSearch Serverless Collection

### Security & Auth
- 1 Cognito User Pool
- 1 AgentCore Gateway
- Multiple IAM Roles and Policies

## 💰 Cost Optimization

### Current Monthly Costs (Estimated)
- **NAT Gateways**: ~$65/month (2 gateways) - **Can be removed if not needed**
- **VPC Endpoints**: ~$122/month (17 interface endpoints)
- **Lambda**: Pay per invocation
- **OpenSearch Serverless**: Based on OCU usage
- **Bedrock**: Pay per API call

### Optimization Tips
1. **Remove NAT Gateways**: If Lambda only accesses AWS services via VPC endpoints, NAT Gateways are not needed (saves ~$780/year)
2. **Reduce VPC Endpoints**: Remove unused endpoints
3. **Lambda Memory**: Adjust based on actual usage
4. **OpenSearch**: Use minimum OCU configuration for dev/test

## 🧪 Testing

### Test MCP Server Locally

```bash
# Test Tool 1: API Endpoint Finder
python -c "
from tools.api_endpoint_finder import APIEndpointFinder
finder = APIEndpointFinder('.')
result = finder.find_endpoint('create_payment', 'card', 'cashier')
print(result)
"

# Test Tool 3: API Documentation Search (requires OpenSearch)
python -c "
from tools.api_documentation_search import APIDocumentationSearch
search = APIDocumentationSearch('.')
result = search.search('How to create a payment?')
print(result)
"
```

### Test Gateway Endpoint

```bash
# Test MCP gateway
python mcp-server/test-mcp-gateway.py
```

## 📖 Usage Examples

### Example 1: Find Payment API

```python
# Using Tool 1: API Endpoint Finder
result = find_api_endpoint(
    task_type="create_payment",
    payment_type="card",
    integration_mode="cashier",
    include_samples=True
)

print(result['selected_api'])
print(result['sample_code'])
```

### Example 2: Get Integration Recommendation

```python
# Using Tool 2: Integration Assistant
result = get_integration_recommendation(
    user_description="I need to accept card payments on my website. "
                    "I want quick integration without PCI compliance."
)

print(result['recommended_method'])
print(result['integration_guide'])
```

### Example 3: Search API Documentation

```python
# Using Tool 3: API Documentation Search
result = search_api_documentation(
    query="How to handle 3DS authentication?",
    top_k=5,
    doc_type_filter="api_doc"
)

for doc in result['results']:
    print(f"{doc['api_name']}: {doc['content']}")
```

## 🔍 Monitoring & Debugging

### CloudWatch Logs
```bash
# View Lambda logs
aws logs tail /aws/lambda/payermax-mcp-gateway-lambda --follow

# View specific log stream
aws logs get-log-events \
  --log-group-name /aws/lambda/payermax-mcp-gateway-lambda \
  --log-stream-name <stream-name>
```

### OpenSearch Monitoring
```bash
# Check collection status
aws opensearchserverless get-collection \
  --id <collection-id>

# View collection metrics
aws cloudwatch get-metric-statistics \
  --namespace AWS/AOSS \
  --metric-name SearchableDocuments \
  --dimensions Name=CollectionId,Value=<collection-id>
```

## 🐛 Troubleshooting

### Issue: OpenSearch tools not available
**Solution**: Set `OPENSEARCH_ENDPOINT` environment variable

### Issue: Lambda timeout
**Solution**: Increase timeout in `lambda-template.yaml` (current: 300s)

### Issue: VPC endpoint connection failed
**Solution**: Check security group allows HTTPS (443) from VPC CIDR

### Issue: Cognito authentication failed
**Solution**: Verify token is not expired, refresh using `refresh-mcp-token.sh`

## 📚 Documentation

- [Architecture Diagram](mcp-server/deploy/architecture-diagram.md)
- [VPC Resources List](mcp-server/deploy/vpc-resources-list.md)
- [Powers README](powers/README.md)
- [Tool Configuration](mcp-server/tool_config.json)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is for internal use and reference.

## 📞 Support

For issues and questions:
- PayerMax Technical Support: support@payermax.com
- PayerMax Developer Center: https://developer.payermax.com

---

**PayerMax API Version**: 1.4
