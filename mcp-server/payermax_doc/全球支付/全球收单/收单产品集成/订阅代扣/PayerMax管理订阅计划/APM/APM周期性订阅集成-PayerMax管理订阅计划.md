# APM周期性订阅集成-PayerMax管理订阅计划

该文档介绍了周期性订阅集成APM支付方式的相关集成步骤，具体包含：创建订阅计划、激活订阅计划以及接收订阅扣款结果等。

## 1. 准备事项

根据配置与签名：
- 获取商户自助平台账号
- 获取商户appId和密钥
- 配置异步通知地址
- 配置公钥和私钥

## 2. 创建订阅计划

以下是几种订阅计划类型的API创建请求响应示例，有关完整的API规范，请参阅**创建订阅计划 API**。

### 环境地址

创建订阅计划不同环境的请求地址如下：

- **Prod请求地址**: `https://pay-gate.payermax.com/aggregate-pay/api/gateway/subscriptionCreate`
- **Test请求地址**: `https://pay-gate-uat.payermax.com/aggregate-pay/api/gateway/subscriptionCreate`

### 2.1 普通订阅计划

首期扣款开始时间（`firstPeriodStartDate`）在请求时间（`requestTime`）后24小时内，且无优惠配置（`trialPeriodConfig`）。

#### 创建普通订阅计划入参

```json
{
  "version": "1.5",
  "keyVersion": "1",
  "requestTime": "2025-02-26T05:00:00.234+00:00",
  "appId": "6666c8b036a24579974497c2f9a33333",
  "merchantNo": "010213834784554",
  "data": {
    "subscriptionRequestId": "subscription100000000000001",
    "userId": "test10001",
    "language": "en",
    "callbackUrl": "http://***.com/notifyUrl/subscription",
    "subscriptionPlan": {
      "subject": "subject",
      "description": "PMMAX周期首期扣款",
      "totalPeriods": 24,
      "periodRule": {
        "periodUnit": "M",
        "periodCount": 2
      },
      "periodAmount": {
        "amount": 10.0,
        "currency": "USD"
      },
      "firstPeriodStartDate": "2025-02-26T12:00:00+00:00",
      "advanceDays": 2
    }
  }
}
```

### 2.2 n天试用

首期扣款开始时间（`firstPeriodStartDate`）在请求时间（`requestTime`）后，且两个时间相差n天，同时无优惠配置（`trialPeriodConfig`）。

以下订阅计划入参示例为试用2天的场景，`firstPeriodStartDate`和`requestTime`相差2天。

#### 创建2天试用订阅计划入参

```json
{
  "version": "1.5",
  "keyVersion": "1",
  "requestTime": "2025-02-26T05:00:00.234+00:00",
  "appId": "6666c8b036a24579974497c2f9a33333",
  "merchantNo": "010213834784554",
  "data": {
    "subscriptionRequestId": "subscription100000000000001",
    "userId": "test10001",
    "language": "en",
    "callbackUrl": "http://***.com/notifyUrl/subscription",
    "subscriptionPlan": {
      "subject": "subject",
      "description": "PMMAX周期首期扣款",
      "totalPeriods": 24,
      "periodRule": {
        "periodUnit": "M",
        "periodCount": 2
      },
      "periodAmount": {
        "amount": 10.0,
        "currency": "USD"
      },
      "firstPeriodStartDate": "2025-02-28T05:00:00+00:00",
      "advanceDays": 2
    }
  }
}
```

### 2.3 前n期优惠

首期扣款开始时间（`firstPeriodStartDate`）在请求时间（`requestTime`）后24小时内，包含优惠配置信息（`trialPeriodConfig`）。

以下订阅计划入参示例为前2期优惠的场景，优惠期扣款金额为3USD，从第3期开始，扣款金额为10USD。

#### 前2期优惠入参

```json
{
  "version": "1.5",
  "keyVersion": "1",
  "requestTime": "2025-02-26T05:00:00.234+00:00",
  "appId": "6666c8b036a24579974497c2f9a33333",
  "merchantNo": "010213834784554",
  "data": {
    "subscriptionRequestId": "subscription100000000000001",
    "userId": "test10001",
    "language": "en",
    "callbackUrl": "http://***.com/notifyUrl/subscription",
    "subscriptionPlan": {
      "subject": "subject",
      "description": "PMMAX周期首期扣款",
      "totalPeriods": 24,
      "periodRule": {
        "periodUnit": "M",
        "periodCount": 2
      },
      "periodAmount": {
        "amount": 10.0,
        "currency": "USD"
      },
      "firstPeriodStartDate": "2025-02-26T12:00:00+00:00",
      "trialPeriodConfig": {
        "trialPeriodCount": 2,
        "trialPeriodAmount": {
          "amount": 3.0,
          "currency": "USD"
        }
      },
      "advanceDays": 2
    }
  }
}
```

#### 创建订阅计划响应参数示例

```json
{
  "msg": "Success.",
  "code": "APPLY_SUCCESS",
  "data": {
    "subscriptionRequestId": "subscription100000000000001",
    "subscriptionPlan": {
      "subscriptionNo": "SUB20250202620949065212112",
      "subscriptionStatus": "INACTIVE"
    }
  }
}
```

## 3. 激活订阅计划

创建订阅计划后，此时订阅计划处于未激活状态，需用户完成一笔支付或授权来激活订阅计划，订阅计划才能生效。

PayerMax提供了收银台模式、API模式和前置组件模式3种集成模式来完成首笔支付或授权。

### 激活请求参数说明

- 如果订阅计划类型是**n天试用**，则激活时`totalAmount`的值为0
- 如果订阅计划类型是**前n期优惠**，则激活时`totalAmount`的值为优惠期设置的金额
- 如果订阅计划类型是**普通订阅**，则激活时`totalAmount`的值固定期的金额
- 激活时的`currency`必须和订阅计划中的币种保持一致
- 激活时的`userId`必须和订阅计划中的`userId`保持一致
- 激活时必须上送创建订阅计划后PayerMax返回的订阅单号`subscriptionNo`
- 激活时`subject`的值须与订阅计划中的`subject`保持一致

### 3.1 收银台模式激活订阅计划

> **注意**: 收银台模式激活订阅计划时，支持全量收银台模式、指定支付方式、指定支付方式+目标机构。

收银台模式激活订阅计划API文档，请参阅**收银台-下单 API**。

#### 环境地址

- **Prod请求地址**: `https://pay-gate.payermax.com/aggregate-pay/api/gateway/orderAndPay`
- **Test请求地址**: `https://pay-gate-uat.payermax.com/aggregate-pay/api/gateway/orderAndPay`

#### 全量收银台激活订阅计划请求参数示例

```json
{
  "version": "1.5",
  "keyVersion": "1",
  "requestTime": "2022-01-17T09:05:52.194+00:00",
  "appId": "bbd8d2639a7c4dfd8df7d005294390df",
  "merchantNo": "020113838535952",
  "data": {
    "outTradeNo": "APIFOXDEV1745388079422",
    "subject": "订阅计划的标题",
    "totalAmount": 10,
    "currency": "USD",
    "userId": "test1111",
    "language": "en",
    "reference": "test subscription",
    "frontCallbackUrl": "https://[your domain name]/[your callback URL]",
    "notifyUrl": "https://[your domain name]/[your notify URL]",
    "integrate": "Hosted_Checkout",
    "expireTime": "1800",
    "subscriptionPlan": {
      "subscriptionNo": "SUB25022603353890000002003"
    },
    "paymentDetail": {
      "mitType": "SCHEDULED",
      "tokenForFutureUse": true,
      "merchantInitiated": false
    }
  }
}
```

#### 指定支付方式激活订阅计划请求参数示例

```json
{
  "version": "1.5",
  "keyVersion": "1",
  "requestTime": "2022-01-17T09:05:52.194+00:00",
  "appId": "bbd8d2639a7c4dfd8df7d005294390df",
  "merchantNo": "020113838535952",
  "data": {
    "outTradeNo": "APIFOXDEV1745388079422",
    "subject": "订阅计划的标题",
    "totalAmount": 10,
    "currency": "USD",
    "country": "KR",
    "userId": "test1111",
    "language": "en",
    "reference": "test subscription",
    "frontCallbackUrl": "https://[your domain name]/[your callback URL]",
    "notifyUrl": "https://[your domain name]/[your notify URL]",
    "integrate": "Hosted_Checkout",
    "expireTime": "1800",
    "subscriptionPlan": {
      "subscriptionNo": "SUB25022603353890000002003"
    },
    "paymentDetail": {
      "paymentMethodType": "ONE_TOUCH",
      "mitType": "SCHEDULED",
      "tokenForFutureUse": true,
      "merchantInitiated": false
    }
  }
}
```

#### 指定支付方式+目标机构（钱包）激活订阅计划请求参数示例

```json
{
  "version": "1.5",
  "keyVersion": "1",
  "requestTime": "2022-01-17T09:05:52.194+00:00",
  "appId": "bbd8d2639a7c4dfd8df7d005294390df",
  "merchantNo": "020113838535952",
  "data": {
    "outTradeNo": "APIFOXDEV1745388079422",
    "subject": "订阅计划的标题",
    "totalAmount": 10,
    "currency": "USD",
    "country": "KR",
    "userId": "test1111",
    "language": "en",
    "reference": "test subscription",
    "frontCallbackUrl": "https://[your domain name]/[your callback URL]",
    "notifyUrl": "https://[your domain name]/[your notify URL]",
    "integrate": "Hosted_Checkout",
    "expireTime": "1800",
    "subscriptionPlan": {
      "subscriptionNo": "SUB25022603353890000002003"
    },
    "paymentDetail": {
      "paymentMethodType": "ONE_TOUCH",
      "targetOrg": "NAVERPAY",
      "mitType": "SCHEDULED",
      "tokenForFutureUse": true,
      "merchantInitiated": false,
      "buyerInfo": {
        "firstName": "Deborah",
        "lastName": "Swinstead",
        "email": "your@gmail.com",
        "phoneNo": "0609 031 114",
        "address": "Test Address",
        "city": "Holden Hill",
        "region": "SA",
        "zipCode": "5088",
        "clientIp": "211.52.321.225",
        "userAgent": "Mozilla/5.0 (iPad; CPU OS 18_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/22E252 [FBAN/FBIOS;FBAV/513.1.0.55.90;FBBV/735017191;FBDV/iPad13,16;FBMD/iPad;FBSN/iPadOS;FBSV/18.4.1;FBSS/2;FBID/tablet;FBLC/en_GB;FBOP/5;FBRV/737247184]"
      }
    }
  }
}
```

#### 响应示例

```json
{
  "msg": "Success.",
  "code": "APPLY_SUCCESS",
  "data": {
    "redirectUrl": "https://cashier-n-uat.payermax.com/static/processApiV2.html?tradeToken=T2025042306527802000033&integrate=DIRECT_API&country=UN&payRequestNo=20250423060120EP4366527897000250005&merchantId=010213834784554&merchantAppId=6666c8b036a24579974497c2f9a33333&token=902170aeaadb4621af8d9530398d0efa&orderLan=en&countryLan=en&strategyLan=LUBCO&pmaxLinkV=1",
    "outTradeNo": "APIFOXDEV1745388079422",
    "tradeToken": "T2025042306527802000033",
    "status": "PENDING"
  }
}
```

### 3.2 API模式激活订阅计划

API模式激活订阅计划API文档，请参阅**纯API支付 API**。

#### 环境地址

- **Prod请求地址**: `https://pay-gate.payermax.com/aggregate-pay/api/gateway/orderAndPay`
- **Test请求地址**: `https://pay-gate-uat.payermax.com/aggregate-pay/api/gateway/orderAndPay`

#### API模式指定钱包激活订阅计划请求参数示例

```json
{
  "version": "1.5",
  "keyVersion": "1",
  "requestTime": "2022-01-17T09:05:52.194+00:00",
  "appId": "bbd8d2639a7c4dfd8df7d005294390df",
  "merchantNo": "020113838535952",
  "data": {
    "outTradeNo": "APIFOXDEV1745388079422",
    "subject": "订阅计划的标题",
    "totalAmount": 10,
    "currency": "USD",
    "country": "KR",
    "userId": "test1111",
    "language": "en",
    "reference": "test subscription",
    "frontCallbackUrl": "https://[your domain name]/[your callback URL]",
    "notifyUrl": "https://[your domain name]/[your notify URL]",
    "integrate": "Direct_Payment",
    "expireTime": "1800",
    "subscriptionPlan": {
      "subscriptionNo": "SUB25022603353890000002003"
    },
    "terminalType": "WEB",
    "osType": "ANDROID",
    "paymentDetail": {
      "paymentMethodType": "ONE_TOUCH",
      "targetOrg": "NAVERPAY",
      "mitType": "SCHEDULED",
      "tokenForFutureUse": true,
      "merchantInitiated": false
    }
  }
}
```

#### API模式激活订阅计划响应示例

```json
{
  "msg": "Success.",
  "code": "APPLY_SUCCESS",
  "data": {
    "redirectUrl": "https://cashier-n-uat.payermax.com/static/processApiV2.html?tradeToken=T2025042306527802000033&integrate=DIRECT_API&country=UN&payRequestNo=20250423060120EP4366527897000250005&merchantId=010213834784554&merchantAppId=6666c8b036a24579974497c2f9a33333&token=902170aeaadb4621af8d9530398d0efa&orderLan=en&countryLan=en&strategyLan=LUBCO&pmaxLinkV=1",
    "outTradeNo": "APIFOXDEV1745388079422",
    "tradeToken": "T2025042306527802000033",
    "status": "PENDING"
  }
}
```

## 4. 获取订阅计划激活结果

商户可以通过创建订阅计划时上送的`callbackUrl`地址来接收订阅计划状态变更通知和订阅扣款结果。

### 4.1 获取订阅计划状态变更结果

订阅计划状态变更通知详细通知报文请参考：**订阅状态变更通知 API**。

#### 订阅激活成功通知参数示例

```json
{
  "keyVersion": "1",
  "merchantNo": "P01000116980333",
  "msg": "Success.",
  "notifyTime": "2023-04-24T09:44:40.761Z",
  "notifyType": "SUBSCRIPTION",
  "appId": "6c556bcd56c84652176b3c5abc389296",
  "code": "APPLY_SUCCESS",
  "data": {
    "subscriptionRequestId": "requestMWRkgX5iHaTmf45ePdEP",
    "userId": "10003",
    "subscriptionPlan": {
      "subscriptionNo": "SUB20221212174716894496912",
      "subscriptionStatus": "ACTIVE"
    }
  }
}
```

#### 订阅激活失败通知参数示例

```json
{
  "keyVersion": "1",
  "merchantNo": "P01000116980333",
  "msg": "Success.",
  "notifyTime": "2023-04-24T09:44:40.761Z",
  "notifyType": "SUBSCRIPTION",
  "appId": "6c556bcd56c84652176b3c5abc389296",
  "code": "APPLY_SUCCESS",
  "data": {
    "subscriptionRequestId": "requestMWRkgX5iHaTmf45ePdEP",
    "userId": "10003",
    "subscriptionPlan": {
      "subscriptionNo": "SUB20221212174716894496912",
      "subscriptionStatus": "ACTIVE_FAILED"
    }
  }
}
```

#### 商户响应参数示例

```json
{
  "msg": "Success",
  "code": "SUCCESS"
}
```

### 4.2 获取订阅扣款结果

若创建的订阅计划是普通订阅或前n期优惠，订阅计划激活的同时也会进行首期扣款，扣款完成后，PayerMax会通知商户扣款结果。

订阅扣款结果通知报文请参考：**扣款结果通知 API**。

#### 钱包支付方式扣款成功通知参数示例

```json
{
  "keyVersion": "1",
  "merchantNo": "P01000116980333",
  "msg": "Success.",
  "notifyTime": "2023-04-24T09:44:40.761Z",
  "notifyType": "SUBSCRIPTION_PAYMENT",
  "appId": "6c556bcd56c84652176b3c5abc389296",
  "code": "APPLY_SUCCESS",
  "data": {
    "subscriptionRequestId": "requestMWRkgX5iHaTmf45ePdEP",
    "merchantNo": "P01010113865434",
    "userId": "10003",
    "subscriptionPlan": {
      "subscriptionNo": "SUB20221212174716894496912"
    },
    "subscriptionPaymentDetail": {
      "subscriptionIndex": 1,
      "paymentStatus": "SUCCESS",
      "periodStartTime": "2025-10-13T15:59:59+0000",
      "periodEndTime": "2025-12-13T15:59:59+0000",
      "payAmount": {
        "amount": 10,
        "currency": "USD"
      },
      "paymentMethodType": "ONE_TOUCH",
      "targetOrg": "NAVERPAY",
      "lastPaymentInfo": {
        "tradeToken": "T20221212174800970116912",
        "lastPaymentStatus": "SUCCESS",
        "payTime": "2025-02-13T15:59:59+0000"
      }
    }
  }
}
```

#### 钱包支付方式扣款失败通知参数示例

```json
{
  "keyVersion": "1",
  "merchantNo": "P01000116980333",
  "msg": "Success.",
  "notifyTime": "2023-04-24T09:44:40.761Z",
  "notifyType": "SUBSCRIPTION_PAYMENT",
  "appId": "6c556bcd56c84652176b3c5abc389296",
  "code": "APPLY_SUCCESS",
  "data": {
    "subscriptionRequestId": "requestMWRkgX5iHaTmf45ePdEP",
    "merchantNo": "P01010113865434",
    "userId": "10003",
    "subscriptionPlan": {
      "subscriptionNo": "SUB20221212174716894496912"
    },
    "subscriptionPaymentDetail": {
      "subscriptionIndex": 1,
      "paymentStatus": "FAILED",
      "periodStartTime": "2022-10-13T15:59:59+0000",
      "periodEndTime": "2022-12-13T15:59:59+0000",
      "payAmount": {
        "amount": 10,
        "currency": "USD"
      },
      "paymentMethodType": "ONE_TOUCH",
      "targetOrg": "NAVERPAY",
      "lastPaymentInfo": {
        "tradeToken": "T20221212174800970116912",
        "lastPaymentStatus": "FAILED",
        "payTime": "2022-12-13T15:59:59+0000",
        "errorCode": "xxxx",
        "errorMsg": "xxxx"
      }
    }
  }
}
```

#### 商户响应参数示例

```json
{
  "msg": "Success",
  "code": "SUCCESS"
}
```

### 4.3 获取订阅激活请求结果

商户可以通过激活订阅计划时上送的`notifyUrl`地址来接收激活请求结果，详细通知报文请参考：**支付结果通知 API**。

#### 钱包支付方式激活请求成功结果示例

```json
{
  "appId": "d68f5da6a0174388821a64114c6b322c",
  "code": "APPLY_SUCCESS",
  "data": {
    "channelNo": "TPC425300174064927201759000685",
    "completeTime": "2025-02-27T09:41:12.267Z",
    "country": "UN",
    "currency": "USD",
    "outTradeNo": "20250227174104451122388",
    "paymentDetails": [
      {
        "paymentMethodType": "ONE_TOUCH",
        "targetOrg": "NAVERPAY",
        "paymentTokenID": "PMTOKEN20250227071843552050007000094"
      }
    ],
    "reference": "reference",
    "status": "SUCCESS",
    "thirdChannelNo": "mtjxuvedrz58345",
    "totalAmount": 10,
    "tradeToken": "T2025022709425329000091"
  },
  "keyVersion": "1",
  "merchantNo": "P01010118267336",
  "msg": "Success.",
  "notifyTime": "2025-02-27T09:41:12 +0000",
  "notifyType": "PAYMENT"
}
```

#### 钱包支付方式激活请求失败结果示例

```json
{
  "appId": "d68f5da6a0174388821a64114c6b322c",
  "code": "PAYMENT_FAILED",
  "data": {
    "channelNo": "TPC462800174064934688659000687",
    "completeTime": "2025-02-27T09:44:00.216Z",
    "country": "UN",
    "currency": "USD",
    "outTradeNo": "20250227174218727122389",
    "paymentDetails": [
      {
        "paymentMethodType": "ONE_TOUCH",
        "targetOrg": "NAVERPAY"
      }
    ],
    "reference": "reference",
    "status": "FAILED",
    "thirdChannelNo": "dycbhzfsmz69480",
    "totalAmount": 10,
    "tradeToken": "T2025022709462829000092"
  },
  "keyVersion": "1",
  "merchantNo": "P01010118267336",
  "msg": "Provider failed to process.",
  "notifyTime": "2025-02-27T09:44:00 +0000",
  "notifyType": "PAYMENT"
}
```

#### 商户响应参数示例

```json
{
  "msg": "Success",
  "code": "SUCCESS"
}
```

## 5. PayerMax后续扣款

订阅计划激活后，PayerMax会按照创建订阅计划时指定的提前扣款天数进行扣款，若未指定提前扣款天数，则会按照PayerMax默认规则进行扣款。

具体扣款规则请参考**订阅计划扣款规则说明**。

如果某期扣款重试后全部失败，PayerMax会将该订阅计划终止，并通知商户。

商户可以通过创建订阅计划时上送的`callbackUrl`地址来接收扣款结果，详细通知报文请参考：**支付结果通知 API**。

### 钱包支付方式扣款成功通知参数示例

```json
{
  "keyVersion": "1",
  "merchantNo": "P01000116980333",
  "msg": "Success.",
  "notifyTime": "2023-04-24T09:44:40.761Z",
  "notifyType": "SUBSCRIPTION_PAYMENT",
  "appId": "6c556bcd56c84652176b3c5abc389296",
  "code": "APPLY_SUCCESS",
  "data": {
    "subscriptionRequestId": "requestMWRkgX5iHaTmf45ePdEP",
    "merchantNo": "P01010113865434",
    "userId": "10003",
    "subscriptionPlan": {
      "subscriptionNo": "SUB20221212174716894496912"
    },
    "subscriptionPaymentDetail": {
      "subscriptionIndex": 1,
      "paymentStatus": "SUCCESS",
      "periodStartTime": "2025-10-13T15:59:59+0000",
      "periodEndTime": "2025-12-13T15:59:59+0000",
      "payAmount": {
        "amount": 10,
        "currency": "USD"
      },
      "paymentMethodType": "ONE_TOUCH",
      "targetOrg": "NAVERPAY",
      "lastPaymentInfo": {
        "tradeToken": "T20221212174800970116912",
        "lastPaymentStatus": "SUCCESS",
        "payTime": "2025-02-13T15:59:59+0000"
      }
    }
  }
}
```

### 钱包支付方式扣款失败通知参数示例

```json
{
  "keyVersion": "1",
  "merchantNo": "P01000116980333",
  "msg": "Success.",
  "notifyTime": "2023-04-24T09:44:40.761Z",
  "notifyType": "SUBSCRIPTION_PAYMENT",
  "appId": "6c556bcd56c84652176b3c5abc389296",
  "code": "APPLY_SUCCESS",
  "data": {
    "subscriptionRequestId": "requestMWRkgX5iHaTmf45ePdEP",
    "merchantNo": "P01010113865434",
    "userId": "10003",
    "subscriptionPlan": {
      "subscriptionNo": "SUB20221212174716894496912"
    },
    "subscriptionPaymentDetail": {
      "subscriptionIndex": 1,
      "paymentStatus": "FAILED",
      "periodStartTime": "2022-10-13T15:59:59+0000",
      "periodEndTime": "2022-12-13T15:59:59+0000",
      "payAmount": {
        "amount": 10,
        "currency": "USD"
      },
      "paymentMethodType": "ONE_TOUCH",
      "targetOrg": "NAVERPAY",
      "lastPaymentInfo": {
        "tradeToken": "T20221212174800970116912",
        "lastPaymentStatus": "FAILED",
        "payTime": "2022-12-13T15:59:59+0000",
        "errorCode": "xxxx",
        "errorMsg": "xxxx"
      }
    }
  }
}
```

## 6. 管理订阅计划

订阅计划激活后，可进行订阅计划的管理，如查询订阅扣款结果、取消订阅计划等，订阅计划状态变更后，PayerMax会通知商户订阅计划状态。

### 6.1 订阅状态变更通知

商户可以通过创建订阅计划时上送的`callbackUrl`地址来接收订阅计划状态变更结果，详细通知报文请参考：**订阅状态变更通知 API**。

#### 订阅计划终止通知参数示例

```json
{
  "keyVersion": "1",
  "merchantNo": "P01000116980333",
  "msg": "Success.",
  "notifyTime": "2023-04-24T09:44:40.761Z",
  "notifyType": "SUBSCRIPTION",
  "appId": "6c556bcd56c84652176b3c5abc389296",
  "code": "APPLY_SUCCESS",
  "data": {
    "subscriptionRequestId": "requestMWRkgX5iHaTmf45ePdEP",
    "userId": "10003",
    "subscriptionPlan": {
      "subscriptionNo": "SUB20221212174716894496912",
      "subscriptionStatus": "TERMINATE"
    }
  }
}
```

### 6.2 取消订阅计划

商户可取消订阅计划，如果正处于最新一期处于扣款中，须等该期扣款成功或扣款失败后，才能取消订阅计划。

详细API报文请参考：**取消订阅计划 API**。

#### 环境地址

- **Prod请求地址**: `https://pay-gate.payermax.com/aggregate-pay/api/gateway/subscriptionCancel`
- **Test请求地址**: `https://pay-gate-uat.payermax.com/aggregate-pay/api/gateway/subscriptionCancel`

#### 取消订阅计划请求参数示例

```json
{
  "version": "1.5",
  "keyVersion": "1",
  "requestTime": "2023-02-13T06:32:50.455+00:00",
  "appId": "82ff47ea6c724a60b666e3ac0ea172dd",
  "merchantNo": "P01010113865434",
  "data": {
    "subscriptionNo": "SUB20221212174716894496912"
  }
}
```

#### 取消订阅计划响应参数示例

```json
{
  "msg": "Success.",
  "code": "APPLY_SUCCESS",
  "data": {
    "subscriptionRequestId": "requestMWRkgX5iHaTmf45ePdEP",
    "userId": "10003",
    "subscriptionPlan": {
      "subscriptionNo": "SUB20221212174716894496912",
      "subscriptionStatus": "CANCEL"
    }
  }
}
```

### 6.3 查询订阅扣款结果

查询订阅扣款结果API文档，请参考：**订阅扣款结果查询 API**。

#### 环境地址

- **Prod请求地址**: `https://pay-gate.payermax.com/aggregate-pay/api/gateway/subscriptionQuery`
- **Test请求地址**: `https://pay-gate-uat.payermax.com/aggregate-pay/api/gateway/subscriptionQuery`

#### 查询订阅计划请求参数示例

```json
{
  "version": "1.5",
  "keyVersion": "1",
  "requestTime": "2023-02-13T06:32:50.455+00:00",
  "appId": "82ff47ea6c724a60b666e3ac0ea172dd",
  "merchantNo": "P01010113865434",
  "data": {
    "subscriptionRequestId": "requestMWRkgX5iHaTmf45ePdEP",
    "subscriptionNo": "SUB20221212174716894496912"
  }
}
```

> **注意**: `subscriptionNo`和`subscriptionRequestId`必须传一个。

#### 查询订阅计划响应参数示例

```json
{
  "msg": "Success.",
  "code": "APPLY_SUCCESS",
  "data": {
    "subscriptionRequestId": "requestMWRkgX5iHaTmf45ePdEP",
    "merchantNo": "P01010113865434",
    "userId": "10003",
    "subscriptionPlan": {
      "subscriptionNo": "SUB20221212174716894496912",
      "subscriptionStatus": "ACTIVE"
    },
    "subscriptionPaymentDetails": [
      {
        "subscriptionIndex": 0,
        "paymentStatus": "SUCCESS",
        "periodStartTime": "2025-01-13T15:59:59+0000",
        "periodEndTime": "2025-02-13T15:59:59+0000",
        "payAmount": {
          "amount": 100,
          "currency": "SAR"
        },
        "paymentMethodType": "ONE_TOUCH",
        "targetOrg": "NAVERPAY",
        "lastPaymentInfo": {
          "tradeToken": "T20221212174800970116912",
          "lastPaymentStatus": "SUCCESS",
          "payTime": "2025-01-12T15:59:59+0000"
        }
      },
      {
        "subscriptionIndex": 1,
        "paymentStatus": "PENDING",
        "periodStartTime": "2025-02-13T15:59:59+0000",
        "periodEndTime": "2025-03-13T15:59:59+0000",
        "payAmount": {
          "amount": 100,
          "currency": "SAR"
        },
        "paymentMethodType": "ONE_TOUCH",
        "targetOrg": "NAVERPAY",
        "lastPaymentInfo": {
          "tradeToken": "T20221212174800970116912",
          "lastPaymentStatus": "FAILED",
          "payTime": "2025-02-12T15:59:59+0000",
          "errorCode": "xxxx",
          "errorMsg": "xxxx"
        }
      }
    ]
  }
}
```
