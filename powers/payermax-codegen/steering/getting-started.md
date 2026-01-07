# Getting Started with PayerMax API Code Generator

This guide walks you through generating PayerMax API integration code.

## Interactive Code Generation

This power uses an **interactive three-step approach** to gather requirements before generating code:

**Step 1: Select Interaction Language (FIRST - REQUIRED)**
- Agent **MUST FIRST** ask: "Which language would you like to use for our conversation?"
- Options: **Chinese (中文)** or **English**
- This sets the language for ALL subsequent interactions
- All tool descriptions, questions, and responses will use the selected language

**Step 2: Describe Use Case (SECOND - REQUIRED)**
- After language selection, agent asks (in selected language): "Please briefly describe what you want to build with PayerMax APIs"
- User provides context about their integration needs
- Agent identifies relevant APIs based on description

**Step 3: Gather Configuration (THIRD - AFTER USE CASE)**
- Agent then presents clear selection options in Kiro's interface (in selected language) for:
  - Programming language (Python, Node.js, Java, etc.)
  - Code structure and style
  - Credential handling
  - Features to include
  - Target environment
  - Custom requirements

This ensures the generated code matches your exact needs and the interaction is in your preferred language.

## Quick Start

### Step 1: Select Interaction Language

When user starts, agent **MUST FIRST** ask:

```
Agent: "Which language would you like to use for our conversation?"
Options:
- Chinese (中文)
- English
```

**User selects**: Chinese or English

**Agent should**:
1. Remember the selected language
2. Use ONLY that language for all subsequent interactions
3. Proceed to Step 2

### Step 2: Request Code Generation

Start by telling the agent you want to integrate PayerMax (agent will respond in your selected language):

```
User: "I want to integrate PayerMax APIs"
```

**Agent should** (in selected language):
1. Ask: "Please briefly describe what you want to build with PayerMax APIs"
   - If Chinese selected: "请简要描述您想用 PayerMax API 构建什么功能"
   - If English selected: "Please briefly describe what you want to build with PayerMax APIs"

### Step 3: Describe Your Use Case

Provide a brief description:

```
User: "I need to query payment status for my e-commerce orders"
```

**Agent should**:
1. Identify relevant APIs based on description
2. Call `search_apis("查询")` or `search_apis("query")` or browse categories
3. Determine the best API match (e.g., "付款查询")

### Step 4: Configure Code Generation

**Agent workflow**:

1. **Select Language** (FIRST - REQUIRED)
   
   Agent asks: **"Which language would you like to use for our conversation? / 您希望使用哪种语言进行交流？"**
   
   Options: Chinese (中文) / English

2. **Gather Use Case** (SECOND - REQUIRED)
   
   Agent asks (in selected language): **"Please briefly describe what you want to build with PayerMax APIs"**
   
   User provides context about their needs.

3. **Interactive Configuration** (THIRD - AFTER USE CASE)
   
   **IMPORTANT**: Before asking any question, check if the user already provided that information in Step 2. If they did, skip that question and use their provided value.
   
   Agent asks questions **ONE AT A TIME**, waiting for user response before proceeding:
   
   **Question 1: Programming Language**
   
   Agent asks (in selected language): "Which programming language would you like to use?"
   
   **SKIP IF**: User mentioned language in Step 2 (e.g., "I need Python code...")
   
   Options:
   1. Python
   2. Node.js (JavaScript)
   3. Java
   4. PHP
   5. Go
   6. Ruby
   7. C#
   8. Shell (curl)
   
   User enters: **1-8**
   
   **Wait for user selection, then proceed to Question 2**
   
   ---
   
   **Question 2: Code Structure**
   
   Agent asks: "What code structure do you prefer?"
   
   **SKIP IF**: User specified structure in Step 2 (e.g., "a class-based client...")
   
   Options:
   1. Class-based API client (recommended)
   2. Standalone function
   3. Complete module with utilities
   4. Code snippet only
   
   User enters: **1-4**
   
   **Wait for user selection, then proceed to Question 3**
   
   ---
   
   **Question 3: Credential Handling**
   
   Agent asks: "How should API credentials be handled?"
   
   **SKIP IF**: User mentioned credentials in Step 2 (e.g., "use environment variables...")
   
   Options:
   1. Use placeholders (recommended for sharing)
   2. I'll provide actual credentials
   3. Use environment variables
   
   User enters: **1-3**
   
   **Wait for user selection, then proceed to Question 4**
   
   ---
   
   **Question 4: Features to Include**
   
   Agent asks: "Which features would you like to include? (You can select multiple, e.g., 1,2,4)"
   
   **SKIP IF**: User specified features in Step 2 (e.g., "with error handling and logging...")
   
   Options (multi-select):
   1. Error handling and retry logic
   2. Request/response logging
   3. Parameter validation
   4. Type hints/annotations
   5. Usage examples in comments
   6. Unit test template
   
   User enters: **1-6 (comma-separated for multiple, e.g., "1,2,3")**
   
   **Wait for user selection, then proceed to Question 5**
   
   ---
   
   **Question 5: Target Environment**
   
   Agent asks: "Which environment will you use?"
   
   **SKIP IF**: User mentioned environment in Step 2 (e.g., "for production..." or "for testing...")
   
   Options:
   1. UAT (testing) - recommended for development
   2. Production
   
   User enters: **1-2**
   
   **Wait for user selection, then proceed to Question 6**
   
   ---
   
   **Question 6: Custom Requirements (Optional)**
   
   Agent asks: "Do you have any special requirements? (Enter text or 'no' to skip)"
   
   **SKIP IF**: User already provided special requirements in Step 2
   
   Examples:
   - Specific payment methods
   - Regional configurations (e.g., Brazil market)
   - Custom error handling
   
   User enters: **Text description or "no"**
   
   **Wait for user response, then proceed to Step 4**

---

### Step 4: Collect Required API Parameters

**After configuration is complete, agent must**:

1. **Retrieve API Documentation**
   ```
   Call: get_api_documentation(category, api_name)
   ```

2. **Parse Required Parameters**
   - Identify all fields marked as "必填" (Required) or "Y" in the required column
   - Note parameter constraints (max length, format, allowed values)
   - Skip system parameters (appId, merchantNo, requestTime, version, keyVersion)

3. **Check Step 2 Use Case Description**
   - Review user's use case description from Step 2
   - Identify if user already provided values for any required parameters
   - Extract those values

4. **Ask for Each Required Parameter ONE AT A TIME** (in selected language)
   
   **SKIP IF**: User already provided this parameter value in Step 2
   
   For each required parameter not yet provided:
   ```
   Agent: "Please provide value for '[parameter_name]'"
   Agent: "Description: [parameter description from API spec]"
   Agent: "Constraints: [max length / format / allowed values]"
   
   User: [enters value]
   
   Agent validates and proceeds to next parameter
   ```

5. **Example Parameter Collection**:
   ```
   # If user said in Step 2: "I need to query order ORDER_20240107_001"
   # Agent extracts: outTradeNo = "ORDER_20240107_001"
   # Agent SKIPS asking for outTradeNo
   
   # Agent only asks for remaining required parameters:
   Agent: "Please provide value for 'amount'"
   Agent: "Description: Payment amount"
   Agent: "Constraints: Decimal, e.g., 100.50"
   User: "99.99"
   ```

6. **Validate Each Input**
   - Check length constraints
   - Verify format requirements
   - Confirm required fields are not empty

**CRITICAL**: Always review Step 2 first. Do NOT ask for information user already provided.

---

### Step 5: Generate and Review Code

**After all parameters are collected, agent must**:

1. **Generate Initial Code**
   - Use all collected configuration settings
   - Include all user-provided parameter values
   - Apply selected features (error handling, logging, etc.)
   - Use correct endpoint URL based on environment

2. **Self-Review Code (CRITICAL - MANDATORY)**
   
   Agent must review the generated code for:
   - ✓ Syntax errors (brackets, semicolons, indentation)
   - ✓ All required parameters are included
   - ✓ Parameter values are correctly placed
   - ✓ Signature generation logic is correct
   - ✓ Endpoint URL matches selected environment
   - ✓ Error handling is complete
   - ✓ Import statements are correct
   - ✓ Variable names are consistent
   - ✓ Code follows language best practices
   - ✓ Code can run immediately without modifications

3. **Fix Any Issues**
   - If errors found, correct them immediately
   - Re-review after fixes

4. **Deliver Production-Ready Code**
   - Present the final, reviewed code
   - Include brief usage instructions
   - Mention any setup requirements (install dependencies, etc.)

**CRITICAL**: The delivered code MUST be production-ready and runnable as-is. Always perform thorough self-review before delivery.

2. **Retrieve Documentation**
   ```
   Call: get_api_documentation("付款", "付款查询")
   ```

3. **Parse Specification**
   - Extract endpoint URL
   - Identify required headers
   - List all request parameters
   - Note parameter constraints (max length, required/optional)
   - Understand response structure

4. **Generate Code Structure** (based on user selections)
   ```python
   import requests
   import json
   from datetime import datetime
   
   class PayerMaxClient:
       def __init__(self, app_id, merchant_no, private_key):
           self.app_id = app_id
           self.merchant_no = merchant_no
           self.private_key = private_key
           self.base_url = "https://pay-gate-uat.payermax.com"
       
       def generate_signature(self, payload):
           # TODO: Implement signature generation
           pass
       
       def payment_order_query(self, out_trade_no):
           # Implementation based on API spec
           pass
   ```

5. **Add Request Logic**
   - Build request payload with all required fields
   - Add parameter validation (if selected)
   - Generate signature
   - Make HTTP request
   - Handle response

6. **Include Error Handling** (if selected)
   ```python
   try:
       response = requests.post(url, json=payload, headers=headers)
       response.raise_for_status()
       result = response.json()
       
       if result.get('code') == 'APPLY_SUCCESS':
           return result['data']
       else:
           raise Exception(f"API Error: {result.get('msg')}")
   except requests.exceptions.RequestException as e:
       # Handle network errors
       pass
   ```

7. **Add Documentation**
   - Document each parameter from API spec
   - Add usage examples (if selected)
   - Include response field descriptions

## Language-Specific Templates

### Python Template

```python
import requests
import json
from datetime import datetime, timezone

class PayerMaxClient:
    """PayerMax API Client"""
    
    def __init__(self, app_id: str, merchant_no: str, private_key: str):
        self.app_id = app_id
        self.merchant_no = merchant_no
        self.private_key = private_key
        self.base_url = "https://pay-gate-uat.payermax.com"
        self.version = "1.4"
        self.key_version = "1"
    
    def _generate_signature(self, payload: dict) -> str:
        """Generate request signature"""
        # Implement RSA signature generation
        # See PayerMax technical documentation
        pass
    
    def _make_request(self, endpoint: str, data: dict) -> dict:
        """Make API request with signature"""
        request_time = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + '+00:00'
        
        payload = {
            "version": self.version,
            "keyVersion": self.key_version,
            "requestTime": request_time,
            "appId": self.app_id,
            "merchantNo": self.merchant_no,
            "data": data
        }
        
        signature = self._generate_signature(payload)
        headers = {
            "Content-Type": "application/json",
            "sign": signature
        }
        
        url = f"{self.base_url}{endpoint}"
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        
        return response.json()
```

### Node.js Template

```javascript
const axios = require('axios');

class PayerMaxClient {
  constructor(appId, merchantNo, privateKey) {
    this.appId = appId;
    this.merchantNo = merchantNo;
    this.privateKey = privateKey;
    this.baseUrl = 'https://pay-gate-uat.payermax.com';
    this.version = '1.4';
    this.keyVersion = '1';
  }

  generateSignature(payload) {
    // Implement RSA signature generation
    // See PayerMax technical documentation
  }

  async makeRequest(endpoint, data) {
    const requestTime = new Date().toISOString();
    
    const payload = {
      version: this.version,
      keyVersion: this.keyVersion,
      requestTime: requestTime,
      appId: this.appId,
      merchantNo: this.merchantNo,
      data: data
    };

    const signature = this.generateSignature(payload);
    
    const response = await axios.post(
      `${this.baseUrl}${endpoint}`,
      payload,
      {
        headers: {
          'Content-Type': 'application/json',
          'sign': signature
        }
      }
    );

    return response.data;
  }
}
```

## Common Patterns

### Pattern 1: Single API Method

For generating a single API method:

1. Get full documentation: `get_api_documentation(category, api_name)`
2. Extract endpoint, method, parameters
3. Generate method with proper typing
4. Add parameter validation
5. Include error handling
6. Add docstring with parameter descriptions

### Pattern 2: Complete API Client

For generating a full client library:

1. List all APIs in category: `list_apis_in_category(category)`
2. For each API, get documentation
3. Create client class with shared configuration
4. Generate method for each API
5. Add common utilities (signature, error handling)
6. Create comprehensive documentation

### Pattern 3: Quick Test Script

For generating a test script:

1. Get API sample: `get_api_sample(category, api_name)`
2. Extract sample request
3. Convert to executable script
4. Add placeholders for credentials
5. Include response validation

## Best Practices

### 1. Always Validate Parameters

```python
def payment_order_query(self, out_trade_no: str):
    # Validate based on API spec constraints
    if not out_trade_no:
        raise ValueError("out_trade_no is required")
    if len(out_trade_no) > 63:
        raise ValueError("out_trade_no must be <= 63 characters")
    
    # Make request
    ...
```

### 2. Use Type Hints (Python) or TypeScript

```python
from typing import Dict, Optional

def payment_order_query(self, out_trade_no: str) -> Dict[str, any]:
    """
    Query payment order status
    
    Args:
        out_trade_no: Original merchant order number (max 63 chars)
    
    Returns:
        Dict containing order status and details
    
    Raises:
        ValueError: If parameters are invalid
        requests.HTTPError: If API request fails
    """
```

### 3. Include Usage Examples

```python
# Usage Example:
# 
# client = PayerMaxClient(
#     app_id="your_app_id",
#     merchant_no="your_merchant_no",
#     private_key="your_private_key"
# )
# 
# result = client.payment_order_query("order_123456")
# print(f"Order status: {result['status']}")
```

### 4. Handle All Response Codes

```python
result = response.json()

if result['code'] == 'APPLY_SUCCESS':
    # Success - but check order status
    if result['data']['status'] == 'SUCCESS':
        return result['data']
    elif result['data']['status'] == 'FAILED':
        raise PaymentFailedError(result['data'].get('responseMsg'))
    elif result['data']['status'] == 'PENDING':
        return result['data']  # Still processing
elif result['code'] == 'ORDER_NOT_EXIST':
    raise OrderNotFoundError("Order does not exist")
else:
    raise APIError(f"API Error: {result['msg']}")
```

## Troubleshooting

### Issue: Missing Required Fields

**Solution**: Always call `get_api_documentation()` to get the complete parameter list. Check the "必填" (Required) column.

### Issue: Parameter Length Violations

**Solution**: Check the "限制" (Limit) column in the API spec and add validation.

### Issue: Signature Generation

**Solution**: Refer to PayerMax technical documentation for signature algorithm. This is typically RSA with SHA256.

### Issue: Response Parsing

**Solution**: Use the response structure from `get_api_documentation()` to understand all possible fields.

## Next Steps

- Read `advanced-patterns.md` for complex scenarios
- Explore multi-API integrations
- Learn about error handling strategies
- Implement retry logic and timeouts
