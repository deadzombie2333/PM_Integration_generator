# paymentTokenID查询 (Inquire Payment Token)

## Endpoint
```
POST https://pay-gate-uat.payermax.com/aggregate-pay/api/gateway/inquirePaymentToken
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
| version | string | required | 接口版本 当前值为：1.2 | - |
| keyVersion | string | required | 密钥版本 当前值为：1 | <= 8 characters |
| requestTime | string | required | 请求时间，符合rfc3339规范，格式：yyyy-MM-dd'T'HH:mm:ss.SSSXXX 时间需要在当前时间两分钟内 | <= 32 characters |
| appId | string | required | 商户应用Id，PayerMax分配给商户应用的唯一标识 | <= 64 characters |
| merchantNo | string | optional | 商户号，商户与PayerMax业务签约时生成的唯一标识 | <= 32 characters |
| data | object | required | 请求数据体 | - |

### data Object

| Parameter | Type | Required | Description | Constraints |
|-----------|------|----------|-------------|-------------|
| userId | string | required | 商户内部的的用户号，必须唯一 | <= 64 characters |
| tokenScope | string | required | 不填默认为tokenAcq | <= 16 characters, Allowed: tokenAcq, tokenMit |
| paymentTokenID | string | optional | PMMax token | <= 64 characters |
| paymentMethodType | string | optional | 支付方式类型，可传CARD、WALLET等 | - |
| targetOrg | string | optional | 目标机构，当paymentMethodType=CARD时，该字段不传或传空字符串 | - |
| cardOrg | string | optional | 卡组，当paymentMethodType=CARD时，可传VISA、MASTERCARD等卡组 | - |
| referralCode | string | optional | token绑定的唯一标识 | - |

**Example Request:**
```json
{
  "version": "1.2",
  "keyVersion": "1",
  "requestTime": "2025-01-07T13:15:90.386Z",
  "appId": "your_app_id",
  "merchantNo": "your_merchant_no",
  "data": {
    "userId": "user_12345",
    "tokenScope": "tokenAcq",
    "paymentTokenID": "token_abc123",
    "paymentMethodType": "CARD",
    "cardOrg": "VISA"
  }
}
```

## Response

### 200 OK

**Content-Type:** `application/json`

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| code | string | required | 返回码，'APPLY_SUCCESS'代表成功 |
| msg | string | required | 返回描述，'Success.' |
| data | object or null | required | - |

### data Object

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| tokenList | array[object] or null | required | token列表 |

**Example Response:**
```json
{
  "code": "APPLY_SUCCESS",
  "msg": "Success.",
  "data": {
    "tokenList": [
      {
        "paymentTokenID": "token_abc123",
        "paymentMethodType": "CARD",
        "cardOrg": "VISA",
        "status": "ACTIVE"
      }
    ]
  }
}
```
