# VPC Resources - Complete List

## VPC Configuration
- **CIDR Block**: 10.0.0.0/16
- **DNS Support**: Enabled
- **DNS Hostnames**: Enabled

---

## Core Network Resources (7)

### 1. VPC
- **Type**: AWS::EC2::VPC
- **Name**: `{VpcName}-vpc`
- **CIDR**: 10.0.0.0/16

### 2. Internet Gateway
- **Type**: AWS::EC2::InternetGateway
- **Name**: `{VpcName}-igw`
- **Attached to**: VPC

### 3-4. Public Subnets (2)
| Subnet | CIDR | AZ | Public IP |
|--------|------|----|-----------| 
| PublicSubnet1 | 10.0.11.0/24 | us-west-2a | Yes |
| PublicSubnet2 | 10.0.12.0/24 | us-west-2b | Yes |

### 5-6. Private Subnets (2)
| Subnet | CIDR | AZ | Public IP |
|--------|------|----|-----------| 
| PrivateSubnet1 | 10.0.21.0/24 | us-west-2a | No |
| PrivateSubnet2 | 10.0.22.0/24 | us-west-2b | No |

### 7. Security Group
- **Type**: AWS::EC2::SecurityGroup
- **Name**: `{VpcName}-sg`
- **Purpose**: VPC Endpoints security
- **Ingress Rules**:
  - Protocol: TCP
  - Port: 443
  - Source: 10.0.0.0/16 (VPC CIDR)
  - Description: VPC HTTPS access for endpoints

---

## NAT Gateway Resources (4)

### 8-9. Elastic IPs (2)
| EIP | Name | Purpose |
|-----|------|---------|
| NatGateway1EIP | `{VpcName}-nat-eip-1-1` | NAT Gateway 1 |
| NatGateway2EIP | `{VpcName}-nat-eip-1-2` | NAT Gateway 2 |

### 10-11. NAT Gateways (2)
| NAT Gateway | Name | Subnet | EIP |
|-------------|------|--------|-----|
| NatGateway1 | `{VpcName}-nat-gateway-0` | PublicSubnet1 | NatGateway1EIP |
| NatGateway2 | `{VpcName}-nat-gateway-1` | PublicSubnet2 | NatGateway2EIP |

---

## Route Tables (3)

### 12. Public Route Table
- **Name**: `{VpcName}-public-rt`
- **Routes**:
  - 0.0.0.0/0 → Internet Gateway
- **Associated Subnets**: PublicSubnet1, PublicSubnet2

### 13. Private Route Table 1
- **Name**: `{VpcName}-private-rt-1`
- **Routes**:
  - 0.0.0.0/0 → NAT Gateway 1
- **Associated Subnets**: PrivateSubnet1

### 14. Private Route Table 2
- **Name**: `{VpcName}-private-rt-2`
- **Routes**:
  - 0.0.0.0/0 → NAT Gateway 2
- **Associated Subnets**: PrivateSubnet2

---

## VPC Endpoints (18)

### Gateway Endpoints (1)

#### 15. S3 Gateway Endpoint
- **Type**: Gateway
- **Service**: com.amazonaws.{region}.s3
- **Route Tables**: PrivateRouteTable1, PrivateRouteTable2
- **Permissions**: GetObject, PutObject, DeleteObject, ListBucket

### Interface Endpoints (17)

All interface endpoints are deployed in both private subnets with the VPC Endpoint Security Group and Private DNS enabled.

#### Container Registry Endpoints (2)

**16. ECR Docker Endpoint**
- **Service**: com.amazonaws.{region}.ecr.dkr
- **Purpose**: Pull Docker images from ECR

**17. ECR API Endpoint**
- **Service**: com.amazonaws.{region}.ecr.api
- **Purpose**: ECR API operations

#### Logging & Monitoring (1)

**18. CloudWatch Logs Endpoint**
- **Service**: com.amazonaws.{region}.logs
- **Purpose**: Send logs to CloudWatch

#### Systems Manager Endpoints (3)

**19. SSM Endpoint**
- **Service**: com.amazonaws.{region}.ssm
- **Purpose**: Systems Manager operations

**20. SSM Messages Endpoint**
- **Service**: com.amazonaws.{region}.ssmmessages
- **Purpose**: Session Manager messaging

**21. EC2 Messages Endpoint**
- **Service**: com.amazonaws.{region}.ec2messages
- **Purpose**: EC2 instance messaging

#### Bedrock AI Endpoints (6)

**22. Bedrock Endpoint**
- **Service**: com.amazonaws.{region}.bedrock
- **Purpose**: Bedrock service API

**23. Bedrock Runtime Endpoint**
- **Service**: com.amazonaws.{region}.bedrock-runtime
- **Purpose**: Invoke AI models

**24. Bedrock Agent Endpoint**
- **Service**: com.amazonaws.{region}.bedrock-agent
- **Purpose**: Bedrock agent operations

**25. Bedrock Agent Runtime Endpoint**
- **Service**: com.amazonaws.{region}.bedrock-agent-runtime
- **Purpose**: Execute Bedrock agents

**26. Bedrock Agent Core Endpoint**
- **Service**: com.amazonaws.{region}.bedrock-agentcore
- **Purpose**: Agent core functionality

**27. Bedrock Agent Core Gateway Endpoint**
- **Service**: com.amazonaws.{region}.bedrock-agentcore.gateway
- **Purpose**: Agent core gateway operations

#### Compute & Serverless (1)

**28. Lambda Endpoint**
- **Service**: com.amazonaws.{region}.lambda
- **Purpose**: Invoke Lambda functions

#### Authentication (1)

**29. Cognito Identity Provider Endpoint**
- **Service**: com.amazonaws.{region}.cognito-idp
- **Purpose**: User authentication via Cognito

#### Search & Analytics (1)

**30. OpenSearch Serverless Endpoint**
- **Service**: com.amazonaws.{region}.aoss
- **Purpose**: Access OpenSearch Serverless collections

---

## Resources Deployed in VPC (from other stacks)

### Lambda Function (from lambda-template.yaml)
- **Name**: `{GatewayName}-lambda`
- **Runtime**: Python 3.11
- **Memory**: 2048 MB
- **Timeout**: 300 seconds
- **Subnets**: PrivateSubnet1, PrivateSubnet2
- **Security Group**: VPCEndpointSecurityGroup
- **Purpose**: MCP Gateway Lambda function

### OpenSearch Serverless Collection (from opensearch-template.yaml)
- **Name**: `{CollectionName}` (default: payermax-docs)
- **Type**: VECTORSEARCH
- **Access**: VPC-only via OpenSearch Serverless VPC Endpoint
- **Purpose**: Document search and retrieval

---

## Total Resource Count

| Category | Count |
|----------|-------|
| VPC & Core Network | 7 |
| NAT Gateways & EIPs | 4 |
| Route Tables | 3 |
| VPC Endpoints (Gateway) | 1 |
| VPC Endpoints (Interface) | 17 |
| **Total VPC Resources** | **32** |
| Lambda Functions (in VPC) | 1 |
| OpenSearch Collections (VPC access) | 1 |
| **Grand Total** | **34** |

---

## Network Flow

```
Internet
    ↓
Internet Gateway
    ↓
Public Subnets (10.0.11.0/24, 10.0.12.0/24)
    ↓
NAT Gateways (2)
    ↓
Private Subnets (10.0.21.0/24, 10.0.22.0/24)
    ↓
Lambda Function + VPC Endpoints
    ↓
AWS Services (Bedrock, OpenSearch, S3, etc.)
```

---

## Security Architecture

1. **Private Subnet Isolation**: Lambda runs in private subnets with no direct internet access
2. **NAT Gateway**: Outbound internet access for Lambda via NAT Gateways in public subnets
3. **VPC Endpoints**: Private connectivity to AWS services without internet gateway
4. **Security Group**: Restricts VPC endpoint access to HTTPS (443) from VPC CIDR only
5. **OpenSearch VPC-Only**: OpenSearch collection accessible only via VPC endpoint

---

## NAT Gateway Usage Analysis

### Current Status: **LIKELY UNUSED** ⚠️

The NAT Gateways are configured in the VPC but are **probably not being used** because:

1. **Lambda has VPC Endpoints**: All AWS services the Lambda needs (Bedrock, S3, OpenSearch, CloudWatch, Cognito) have VPC endpoints configured
2. **No Public Internet Required**: The Lambda doesn't need to access public internet resources
3. **VPC Endpoint Coverage**: 18 VPC endpoints cover all service dependencies

### What Uses NAT Gateways?
NAT Gateways would only be used if:
- Lambda needs to call external APIs (non-AWS services on the internet)
- Lambda needs to download packages from public repositories
- Lambda needs to access services without VPC endpoints

### Current Lambda Dependencies (All via VPC Endpoints):
- ✅ Amazon Bedrock → bedrock-runtime VPC endpoint
- ✅ OpenSearch Serverless → aoss VPC endpoint  
- ✅ Amazon S3 → S3 gateway endpoint
- ✅ CloudWatch Logs → logs VPC endpoint
- ✅ Cognito → cognito-idp VPC endpoint

### Traffic Flow:
```
Lambda (Private Subnet)
    ↓
VPC Endpoints (NOT NAT Gateway)
    ↓
AWS Services
```

**NAT Gateway is bypassed** because VPC endpoints provide direct private connectivity.

---

## Cost Optimization Notes

- **NAT Gateways**: 2 NAT Gateways (~$65/month + data transfer) - **CONSIDER REMOVING** if not needed
- **VPC Endpoints**: 17 interface endpoints (~$122/month + data transfer) - **ACTIVELY USED**
- **Recommendation**: Remove NAT Gateways to save ~$65/month unless Lambda needs public internet access
- **Gateway Endpoint**: S3 gateway endpoint is free (no hourly charge)

### Cost Savings Opportunity:
If NAT Gateways are not needed, removing them would save approximately **$780/year** per environment.
