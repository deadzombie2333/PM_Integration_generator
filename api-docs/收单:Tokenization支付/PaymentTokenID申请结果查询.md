# PaymentTokenID申请结果查询 (Inquire Apply Request)

## Endpoint
```
POST https://pay-gate-uat.payermax.com/aggregate-pay/api/gateway/InquireApplyRequest
```

## Request Headers

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| Content-Type | string | required | - | application/json |
| sign | string | required | 签名信息请参考技术文档 | FPFVT3o227JrFRbqu19boZCpVVTF9KznxyRawUmxpfXilHV/0yK46haPhAjNu1hPUMy7Vw/ILXhfzffNm4Fj0apWknlTY9OJxnSoQxS9BTFtc61tn5yV1q69x/kkBl82/qwg+XTJ4fOzy7Mar3VaC1E2PlDA6RkkKBUyNE6RYgsdB+Su7an4+4HVTNAnoe74WyvBgxTLMNg28igBTdqxaO3w/UBY6ObVp7vkqkQGdL1Y+HgmMYaAVwrM3+ALWGId0sJ+YqTY4WJ+0xCRGhaSnybiIjZsQEYyID68WNUfuavDLDsEhaMm/HfQvf5p0R1Ltovp3wwJnEbQcjY458iX5A== |

## Request Body

**Content-Type:** `application/json`

| Parameter | Type | Required | Description | Constraints |
|-----------|------|----------|-------------|-------------|
| version | string | required | 接口版本 当前值为：1.4 | <= 8 characters |
| keyVersion | string | required | 密钥版本 当前值为：1 | <= 8 characters |
| requestTime | string | required | 请求时间，符合rfc3339规范，格式：yyyy-MM-dd'T'HH:mm:ss.SSSXXX 时间需要在当前时间两分钟内 | <= 32 characters |
| appId | string | required | 商户应用Id，PayerMax分配给商户应用的唯一标识 | <= 64 characters |
| merchantNo | string | optional | 商户号，商户与PayerMax业务签约时生成的唯一标识 | <= 32 characters |
| data | object | required | 请求数据体 | - |

### data Object

| Parameter | Type | Required | Description | Constraints |
|-----------|------|----------|-------------|-------------|
| userId | string | required | 商户内部的用户Id，需要保证每个ID唯一性 | <= 64 characters |
| tokenScope | string | required | 固定值：tokenAcq | - |
| requestId | string | required | 请求单号，唯一标识商户的一笔请求 | - |

**Example Request:**
```json
{
  "version": "1.4",
  "keyVersion": "1",
  "requestTime": "2025-01-07T13:15:90.386Z",
  "appId": "your_app_id",
  "merchantNo": "your_merchant_no",
  "data": {
    "userId": "user_12345",
    "tokenScope": "tokenAcq",
    "requestId": "req_123456"
  }
}
```

## Response

### 200 OK

**Content-Type:** `application/json`

| Parameter | Type | Required | Description | Constraints |
|-----------|------|----------|-------------|-------------|
| code | string | required | 返回码，'APPLY_SUCCESS'代表成功 | - |
| msg | string | required | 返回描述，'Success.' | - |
| data | object | required | - | - |

### data Object

| Parameter | Type | Required | Description | Constraints |
|-----------|------|----------|-------------|-------------|
| requestId | string | required | 请求单号 | - |
| status | string | required | 状态 | Allowed: PENDING, SUCCESS, FAILED |
| redirectUrl | string | optional | token认证地址，当status=PENDING时有值 | - |
| paymentTokenID | string | optional | token值，当status=SUCCESS时有值 | - |

**Example Response (Pending):**
```json
{
  "code": "APPLY_SUCCESS",
  "msg": "Success.",
  "data": {
    "requestId": "req_123456",
    "status": "PENDING",
    "redirectUrl": "https://pay.payermax.com/token/auth/..."
  }
}
```

**Example Response (Success):**
```json
{
  "code": "APPLY_SUCCESS",
  "msg": "Success.",
  "data": {
    "requestId": "req_123456",
    "status": "SUCCESS",
    "paymentTokenID": "token_abc123"
  }
}
```

**Example Response (Failed):**
```json
{
  "code": "APPLY_SUCCESS",
  "msg": "Success.",
  "data": {
    "requestId": "req_123456",
    "status": "FAILED"
  }
}
```
