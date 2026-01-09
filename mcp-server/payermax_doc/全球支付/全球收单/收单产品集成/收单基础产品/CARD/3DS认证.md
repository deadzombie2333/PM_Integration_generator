# 3DS认证

## 什么是 3D Secure

**3D Secure（3DS）** 是一种安全协议，用于提高在线信用和债务卡交易的安全性。

3DS让银行能够在即时验证卡片持有人身份。当卡主进行一个在线交易时，网站会要求他们输入一些特定信息，这些信息可以使银行确认卡主的身份。

### 验证方式

信息输入的方式包括：
- 手机验证码
- 银行预留身份信息（如预留手机号、证件号等）

若校验失败，则支付流程终止，交易无法完成。

### 安全保护

验证步骤通常在支付过程中自动进行，为用户提供了附加的安全保护，同时也保护了商家，防止欺诈交易。

### 发展历史

这个系统最初由Visa公司开发，作为其"Verified by Visa"服务的一部分，后来也被Mastercard、American Express和其他很多银行采用。

**PayerMax当前已全面支持了3D Secure 2**，这个版本在用户体验、数据收集和处理以及移动交易安全等方面都进行了改进。

## 1. 实现3DS认证

商户可以使用两种方式，实现3DS认证。

### 1.1 使用PayerMax 3DS服务

默认情况下，商户在使用PayerMax的卡支付服务时，PayerMax本身会作为一个3DS的服务提供商，帮助商户同时处理3DS认证和支付。

### 1.2 使用第三方3DS服务商

市场上有一些机构具备独立3DS认证的能力（Hitrust/Cardinal/Cybs等）。

商户可以选择使用自己信赖的3DS能力提供商，仅使用PayerMax的支付能力完成支付。

## 2. 使用动态3DS服务

除上述两种方式外，商户也可以申请开通动态3DS能力。

### 开通要求

- **联系方式**: 开通动态3DS能力，须联系技术支持团队
- **集成模式限制**: 使用动态3DS服务只支持通过**纯API集成模式**接入

### 动态3DS能力

开通后，商户在单次支付请求中，可以设置：
- 使用独立3DS服务商
- 使用PayerMax 3DS服务
- 不使用3DS

> **注意**: 仅独立3DS服务商或卡支付-纯API模式集成，支持动态3DS。

### 配置参数

通过 `/orderAndPay` API 创建支付时，商户可以通过 `data.paymentDetail.cardInfo.dynamic3DS` 设定是否使用3DS能力：

| dynamic3DS 值 | 说明 |
|--------------|------|
| 空值（不传） | 不使用动态3DS，直接使用PayerMax 3DS服务 |
| `no3DS` | 跳过PayerMax 3DS认证（但支付渠道仍可能发起3DS） |
| `do3DS` | 使用PayerMax 3DS服务 |
| `ext3DS` | 使用独立3DS服务商 |

## 2.1 动态3DS认证 - no3DS

> **特别提醒**: 即使设置为 `no3DS`，支付渠道仍然可能发起3DS认证流程。

### 请求示例

```bash
curl --request POST \
  --url https://pay-gate-uat.payermax.com/aggregate-pay/api/gateway/orderAndPay \
  --header 'Accept: application/json' \
  --header 'Content-Type: application/json' \
  --header 'sign: FPFMM3o227JrFRbqu19boZCpVVTF9KznxyRawUmxpfXilHV/0yK46haPhAjNu1hPUMy7Vw/ILXhfzffNm4Fj0apWknlTY9OJxnSoQxS9BTFtc61tn5yV1q69x/kkBl82/qwg+XTJ4fOzy7Mar3VaC1E2PlDA6RkkKBUyNE6RYgsdB+Su7an4+4HVTNAnoe74WyvBgxTLMNg28igBTdqxaO3w/UBY6ObVp7vkqkQGdL1Y+HgmMYaAVwrM3+ALWGId0sJ+YqTY4WJ+0xCRGhaSnybiIjZsQEYyID68WNUfuavDLDsEhaMm/HfQvf5p0R1Ltovp3wwJnEbQcjY458iX5A==' \
  --data '{
    "version": "1.4",
    "keyVersion": "1",
    "requestTime": "2025-05-22T11:00:40.614+00:00",
    "appId": "test86c2ee404ce1bb958e5a8c623667",
    "merchantNo": "TEST20118126922",
    "data": {
      "outTradeNo": "2024051218007331272785789980672",
      "integrate": "Direct_Payment",
      "subject": "Online Store",
      "totalAmount": 50.59,
      "currency": "USD",
      "country": "US",
      "userId": "123324",
      "paymentDetail": {
        "paymentMethodType": "CARD",
        "cardInfo": {
          "cardIdentifierNo": "47581523430442",
          "cardHolderFullName": "Heather Christensen",
          "cardExpirationMonth": "10",
          "cardExpirationYear": "27",
          "cvv": "230",
          "dynamic3DS": "no3DS"
        },
        "buyerInfo": {
          "firstName": "Miler",
          "lastName": "patrick",
          "phoneNo": "+18016733977",
          "email": "buyer@gmail.com",
          "clientIp": "2601:680:ce80:9be9:61a5:c9e3:64cc:24cc",
          "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 18_3_2 like Mac OS X) AppleWebKit/605.1.15"
        }
      }
    }
  }'
```

### 响应示例

**场景1: 支付渠道发起3DS认证**

```json
{
  "msg": "Success.",
  "code": "APPLY_SUCCESS",
  "data": {
    "redirectUrl": "https://gpay.com.tr/Whitelabel/order/3DS_08UKL9BAcR",
    "outTradeNo": "2024051218007331272785789980672",
    "tradeToken": "T2024052223464910035619",
    "status": "PENDING"
  }
}
```

**场景2: 支付渠道未发起3DS认证**

```json
{
  "msg": "Success.",
  "code": "APPLY_SUCCESS",
  "data": {
    "outTradeNo": "2024051218007331272785789980672",
    "tradeToken": "T2024052223464910035619",
    "status": "SUCCESS"
  }
}
```

## 2.2 动态3DS认证 - do3DS

### 请求示例

```bash
curl --request POST \
  --url https://pay-gate-uat.payermax.com/aggregate-pay/api/gateway/orderAndPay \
  --header 'Accept: application/json' \
  --header 'Content-Type: application/json' \
  --header 'sign: FPFMM3o227JrFRbqu19boZCpVVTF9KznxyRawUmxpfXilHV/0yK46haPhAjNu1hPUMy7Vw/ILXhfzffNm4Fj0apWknlTY9OJxnSoQxS9BTFtc61tn5yV1q69x/kkBl82/qwg+XTJ4fOzy7Mar3VaC1E2PlDA6RkkKBUyNE6RYgsdB+Su7an4+4HVTNAnoe74WyvBgxTLMNg28igBTdqxaO3w/UBY6ObVp7vkqkQGdL1Y+HgmMYaAVwrM3+ALWGId0sJ+YqTY4WJ+0xCRGhaSnybiIjZsQEYyID68WNUfuavDLDsEhaMm/HfQvf5p0R1Ltovp3wwJnEbQcjY458iX5A==' \
  --data '{
    "version": "1.4",
    "keyVersion": "1",
    "requestTime": "2025-05-22T14:08:54.887+00:00",
    "appId": "test0279df374af8871d1da97c673894",
    "merchantNo": "TEST13827355079",
    "data": {
      "terminalType": "WEB",
      "outTradeNo": "R--Test1747922934887",
      "subject": "SUCCESS",
      "totalAmount": "0.1",
      "currency": "SAR",
      "country": "SA",
      "userId": "apptest0416",
      "integrate": "Direct_Payment",
      "paymentDetail": {
        "paymentMethodType": "CARD",
        "targetOrg": "VISA",
        "cardInfo": {
          "cardIdentifierNo": "53783211112320",
          "cardHolderFullName": "张秀",
          "cardExpirationMonth": "04",
          "cardExpirationYear": "30",
          "cvv": "232",
          "dynamic3DS": "do3DS"
        },
        "buyerInfo": {
          "firstName": "zhang",
          "lastName": "Simth",
          "phoneNo": "9032030628",
          "email": "your@google.com",
          "clientIp": "124.156.108.193",
          "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
      }
    }
  }'
```

### 响应示例

```json
{
  "msg": "Success.",
  "code": "APPLY_SUCCESS",
  "data": {
    "redirectUrl": "https://cashier-n-pre.payermax.com/static/processApiV2.html?tradeToken=T2023052214224172000075&integrate=DIRECT_API&country=SA",
    "outTradeNo": "R--Test1747922934887",
    "tradeToken": "T2023052214224172000075",
    "status": "PENDING"
  }
}
```

## 2.3 动态3DS认证 - ext3DS

使用外部3DS服务商时，需要传递 `paymentDetail.info3DSecure` 对象。

### 请求示例

```bash
curl --request POST \
  --url https://pay-gate-uat.payermax.com/aggregate-pay/api/gateway/orderAndPay \
  --header 'Accept: application/json' \
  --header 'Content-Type: application/json' \
  --header 'sign: FPFMM3o227JrFRbqu19boZCpVVTF9KznxyRawUmxpfXilHV/0yK46haPhAjNu1hPUMy7Vw/ILXhfzffNm4Fj0apWknlTY9OJxnSoQxS9BTFtc61tn5yV1q69x/kkBl82/qwg+XTJ4fOzy7Mar3VaC1E2PlDA6RkkKBUyNE6RYgsdB+Su7an4+4HVTNAnoe74WyvBgxTLMNg28igBTdqxaO3w/UBY6ObVp7vkqkQGdL1Y+HgmMYaAVwrM3+ALWGId0sJ+YqTY4WJ+0xCRGhaSnybiIjZsQEYyID68WNUfuavDLDsEhaMm/HfQvf5p0R1Ltovp3wwJnEbQcjY458iX5A==' \
  --data '{
    "version": "1.4",
    "keyVersion": "1",
    "requestTime": "2025-05-22T11:00:40.614+00:00",
    "appId": "test86c2ee404ce1bb958e5a8c623667",
    "merchantNo": "TEST20118126922",
    "data": {
      "outTradeNo": "2024051218007331272785789980672",
      "integrate": "Direct_Payment",
      "subject": "Online Store",
      "totalAmount": 50.59,
      "currency": "USD",
      "country": "US",
      "userId": "123324",
      "paymentDetail": {
        "paymentMethodType": "CARD",
        "cardInfo": {
          "cardIdentifierNo": "47581523430442",
          "cardHolderFullName": "Heather Christensen",
          "cardExpirationMonth": "10",
          "cardExpirationYear": "27",
          "cvv": "230",
          "dynamic3DS": "ext3DS"
        },
        "info3DSecure": {
          "eci": "05",
          "threeDSVersion": "2.2.0",
          "cavv": "MAAAAAAAAAAAAAAAAAAAAAAAAAA",
          "xid": "123",
          "dsTransactionId": "683001f5-3805-423a-b580-638e4b2093b3"
        },
        "buyerInfo": {
          "firstName": "Miler",
          "lastName": "patrick",
          "phoneNo": "+18016733977",
          "email": "buyer@gmail.com",
          "clientIp": "2601:680:ce80:9be9:61a5:c9e3:64cc:24cc",
          "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 18_3_2 like Mac OS X) AppleWebKit/605.1.15"
        }
      }
    }
  }'
```

### info3DSecure 参数规则

`paymentDetail.info3DSecure` 表示商户使用的第三方3DS服务商的验证信息，对象属性的值符合如下规则：

| 参数 | 必填条件 | 说明 |
|------|---------|------|
| `eci` | 必填 | 取值是两位数字：00、01、02、03、05、06、07 |
| `threeDSVersion` | 必填 | 只能以1或2开头。1开头表示3DS 1.0；2开头表示3DS 2.0 |
| `cavv` | 条件必填 | 当eci是01、02、05、06时，必填 |
| `xid` | 条件必填 | 当eci是01、02、05、06 且threeDSVersion以1开头，则必填 |
| `dsTransactionId` | 条件必填 | 当eci是01、02、05、06且threeDSVersion以2开头，则必填 |

### 响应示例

```json
{
  "msg": "Success.",
  "code": "APPLY_SUCCESS",
  "data": {
    "outTradeNo": "uft_1748243102273J9TseUzteH",
    "tradeToken": "T2025052607561687003664",
    "status": "SUCCESS"
  }
}
```
