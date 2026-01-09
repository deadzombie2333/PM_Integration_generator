# Card-非周期性代扣集成

该文档介绍了非周期性代扣的相关集成步骤，具体包含：绑定支付方式、获取绑定支付方式结果、发起代扣、获取代扣结果等。

## 1. 准备事项

根据配置与签名引导，获取商户自助平台账号、获取商户appId和密钥、配置异步通知地址、配置公钥和私钥。

## 2. 绑定支付方式

核心参数说明：

- **totalAmount**：交易金额，支持传0或者大于0的金额；
- **paymentDetail.mitType**：代扣类型，SCHEDULED标识为周期性订阅，UNSCHEDULED标识为非周期性代扣；
- **paymentDetail.tokenForFutureUse**：true/false，是否需要生成token用于后续代扣；首次绑定支付方式时，该值传true；
- **paymentDetail.merchantInitiated**：true/false，是否是商户发起的交易；首次绑定支付方式时，需要用户参与完成认证或授权，传值为false。

### 2.1 使用PayerMax收银台绑定支付方式

收银台模式绑定支付方式接口文档，请参阅收银台-下单 API。

不同环境的请求地址如下。

- **Prod请求地址**：https://pay-gate.payermax.com/aggregate-pay/api/gateway/orderAndPay
- **Test请求地址**：https://pay-gate-uat.payermax.com/aggregate-pay/api/gateway/orderAndPay

**交易金额大于0元时，请求参数示例:**

```json
{
  "version": "1.5",
  "keyVersion": "1",
  "requestTime": "2022-01-17T09:05:52.194+00:00",
  "appId": "bbd8d2639a7c4dfd8df7d005294390df",
  "merchantNo": "020113838535952",
  "data": {
    "outTradeNo": "APIFOXDEV1745388079422", // 商户下单唯一单号
    "subject": "代扣标题", // 标题
    "totalAmount": 10, // 代扣金额
    "currency": "USD", // 代扣币种
    "userId": "test1111", // 用户号
    "language": "en",
    "reference": "test subscription",
    "frontCallbackUrl": "https://[your domain name]/[your callback URL]",
    "notifyUrl": "https://[your domain name]/[your notify URL]",
    "integrate": "Hosted_Checkout", // 固定值：Hosted_Checkout
    "expireTime": "1800",
    "paymentDetail": {
      "paymentMethodType": "CARD", //必传，值为CARD
      "mitType": "UNSCHEDULED", // 必传，MIT类型，非周期性代扣时为UNSCHEDULED
      "tokenForFutureUse": true, // 必传，值为true，生成paymentTokenID，用于后续代扣
      "merchantInitiated": false, // 必传，false标识不是商户主动发起，有用户参与；true标识商户主动发起，不需要用户参与
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
        "userAgent": "Mozilla/5.0"
      }
    }
  }
}
```

**交易金额为0时，请求参数示例:**

```json
{
  "version": "1.5",
  "keyVersion": "1",
  "requestTime": "2022-01-17T09:05:52.194+00:00",
  "appId": "bbd8d2639a7c4dfd8df7d005294390df",
  "merchantNo": "020113838535952",
  "data": {
    "outTradeNo": "APIFOXDEV1745388079422", // 商户下单唯一单号
    "subject": "代扣标题", // 标题
    "totalAmount": 0, // 代扣金额
    "currency": "USD", // 代扣币种
    "userId": "test1111", // 用户号
    "language": "en",
    "reference": "test subscription",
    "frontCallbackUrl": "https://[your domain name]/[your callback URL]",
    "notifyUrl": "https://[your domain name]/[your notify URL]",
    "integrate": "Hosted_Checkout", // 固定值：Hosted_Checkout
    "expireTime": "1800",
    "paymentDetail": {
      "paymentMethodType": "CARD", //必传，值为CARD
      "mitType": "UNSCHEDULED", // 必传，MIT类型，非周期性代扣时为UNSCHEDULED
      "tokenForFutureUse": true, // 必传，值为true，生成paymentTokenID，用于后续代扣
      "merchantInitiated": false, // 必传，false标识不是商户主动发起，有用户参与；true标识商户主动发起，不需要用户参与
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
        "userAgent": "Mozilla/5.0"
      }
    }
  }
}
```

**响应示例:**

```json
{
  "msg": "Success.",
  "code": "APPLY_SUCCESS",
  "data": {
    // PayerMax 收银台地址
    "redirectUrl": "https://cashier-n-uat.payermax.com/static/processApiV2.html?tradeToken=T2025042306527802000033&integrate=DIRECT_API&country=UN&payRequestNo=20250423060120EP4366527897000250005&merchantId=010213834784554&merchantAppId=6666c8b036a24579974497c2f9a33333&token=902170aeaadb4621af8d9530398d0efa&orderLan=en&countryLan=en&strategyLan=LUBCO&pmaxLinkV=1",
    "outTradeNo": "APIFOXDEV1745388079422",
    "tradeToken": "T2025042306527802000033",
    "status": "PENDING"
  }
}
```

### 2.2 API模式绑定支付方式

API模式绑定支付方式API文档，请参阅纯API支付 API。

不同环境的请求地址如下：

- **Prod请求地址**：https://pay-gate.payermax.com/aggregate-pay/api/gateway/orderAndPay
- **Test请求地址**：https://pay-gate-uat.payermax.com/aggregate-pay/api/gateway/orderAndPay

**请求参数示例:**

```json
{
  "version": "1.5",
  "keyVersion": "1",
  "requestTime": "2022-01-17T09:05:52.194+00:00",
  "appId": "bbd8d2639a7c4dfd8df7d005294390df",
  "merchantNo": "020113838535952",
  "data": {
    "outTradeNo": "APIFOXDEV1745388079422", // 商户下单唯一单号
    "subject": "代扣标题", // 标题
    "totalAmount": 10, // 代扣金额
    "currency": "USD", // 代扣币种
    "userId": "test1111", // 用户号
    "language": "en",
    "reference": "test subscription",
    "frontCallbackUrl": "https://[your domain name]/[your callback URL]",
    "notifyUrl": "https://[your domain name]/[your notify URL]",
    "integrate": "Direct_Payment", // 固定值：Direct_Payment
    "expireTime": "1800",
    "terminalType": "WEB", // 终端类型，WEB、WAP or APP
    "osType": "ANDROID", // 操作系统类型 ANDROID or IOS
    "paymentDetail": {
      "paymentMethodType": "CARD", //必传，值为CARD
      "mitType": "UNSCHEDULED", // 必传，MIT类型，非周期性代扣时为UNSCHEDULED
      "tokenForFutureUse": true, // 必传，值为true，生成paymentTokenID，用于后续代扣
      "merchantInitiated": false, // false表示是需要用户参数；true表示商户发起的代扣，无需用户参与
      "cardInfo": { //必传 卡信息
        "cardIdentifierNo": "4001563861135570",
        "cardHolderFullName": "James Smith",
        "cardExpirationMonth": "05",
        "cardExpirationYear": "25",
        "cvv": "123"
      },
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
        "userAgent": "Mozilla/5.0"
      }
    }
  }
}
```

**响应示例:**

```json
{
  "msg": "Success.",
  "code": "APPLY_SUCCESS",
  "data": {
    // 3ds挑战页地址
    "redirectUrl": "https://cashier-n-uat.payermax.com/static/processApiV2.html?tradeToken=T2025042306527802000033&integrate=DIRECT_API&country=UN&payRequestNo=20250423060120EP4366527897000250005&merchantId=010213834784554&merchantAppId=6666c8b036a24579974497c2f9a33333&token=902170aeaadb4621af8d9530398d0efa&orderLan=en&countryLan=en&strategyLan=LUBCO&pmaxLinkV=1",
    "outTradeNo": "APIFOXDEV1745388079422",
    "tradeToken": "T2025042306527802000033",
    "status": "PENDING"
  }
}
```

### 2.3 使用前置组件绑定支付方式

前置组件绑定支付方式，商户需要通过两个步骤完成集成，具体请参考：集成步骤。

前置组件绑定支付方式时，商户服务端需要调用PayerMax提供的2个API接口：Apply Drop-in Session API 和 前置组件支付 API。

**Apply Drop-in Session接口不同环境请求地址如下：**

- **Prod请求地址**：https://pay-gate.payermax.com/aggregate-pay/api/gateway/applyDropinSession
- **Test请求地址**：https://pay-gate-uat.payermax.com/aggregate-pay/api/gateway/applyDropinSession

**Apply Drop-in Session请求入参示例：**

```json
{
  "version": "1.5",
  "keyVersion": "1",
  "requestTime": "2022-01-17T09:05:52.194+00:00",
  "appId": "3b242b56a8b64274bcc37dac281120e3",
  "merchantNo": "020213827212251",
  "data": {
    "totalAmount": "10", // 代扣金额
    "mitType": "UNSCHEDULED", // 必填，值为SCHEDULED或UNSCHEDULED
    "currency": "USD", // 必填
    "country": "SA", // 非必填
    "userId": "U10001", // 必填，用户id
    "componentList": [ // 必填，组件支持的支付方式
      "CARD"
    ]
  }
}
```

**响应示例:**

```json
{
  "code": "APPLY_SUCCESS",
  "msg": "Success.",
  "data": {
    "clientKey": "37114858239eur2384237r810482390",
    "sessionKey": "bdsf8982348974hhf82934bf8239424"
  }
}
```

**前置组件支付接口不同环境的请求地址如下：**

- **Prod请求地址**：https://pay-gate.payermax.com/aggregate-pay/api/gateway/orderAndPay
- **Test请求地址**：https://pay-gate-uat.payermax.com/aggregate-pay/api/gateway/orderAndPay

**请求参数示例：**

```json
{
  "version": "1.5",
  "keyVersion": "1",
  "requestTime": "2022-01-17T09:05:52.194+00:00",
  "appId": "bbd8d2639a7c4dfd8df7d005294390df",
  "merchantNo": "020113838535952",
  "data": {
    "outTradeNo": "APIFOXDEV1745388079422", // 商户下单唯一单号
    "subject": "代扣标题", // 标题
    "totalAmount": 10, // 代扣金额
    "currency": "USD", // 代扣币种
    "userId": "test1111", // 用户号
    "language": "en",
    "reference": "test mit",
    "frontCallbackUrl": "https://[your domain name]/[your callback URL]",
    "notifyUrl": "https://[your domain name]/[your notify URL]",
    "integrate": "Direct_Payment", // 固定值：Direct_Payment
    "expireTime": "1800",
    "terminalType": "WEB", // 终端类型，WEB、WAP or APP
    "osType": "ANDROID", // 操作系统类型 ANDROID or IOS
    "paymentDetail": {
      "paymentToken": "CPT4f200d278f3a454b9e91c81edc641e2b", // 必传
      "sessionKey": "bdsf8982348974hhf82934bf8239424", // 必传
      "mitType": "UNSCHEDULED", // 必传，MIT类型，非周期性代扣时为UNSCHEDULED
      "tokenForFutureUse": true, // 必传，值为true，生成paymentTokenID，用于后续代扣
      "merchantInitiated": false, // 必传，false标识不是商户主动发起，有用户参与；true标识商户主动发起，不需要用户参与
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
        "userAgent": "Mozilla/5.0"
      }
    }
  }
}
```

**响应示例:**

```json
{
  "code": "APPLY_SUCCESS",
  "msg": "",
  "data": {
    //3ds验证地址
    "redirectUrl": "https://cashier-n-uat.payermax.com/index.html#/cashier/home?merchantId=020213827212251&merchantAppId=3b242b56a8b64274bcc37dac281120e3&country=ID&tradeToken=TOKEN20220117091121294138752&language=en&token=IHjqkZ8%2F%2FFcnfDPxWTvJFOrulUAKfXFUkxHJSiTdlnjnX1G6AOuTiSl6%2BN05EzxTaJkcSsSyGh5a1q%2FACwWN0sDD%2FgwY5YdWu3ghDcH2wqm%2BJIcEh0qZqo%2BQFnXp65bvkLZnY7VO7HwZGzyrpMBlPhfRCQxwBbc6lJcSYuPf%2Fe8%3D&amount=10000¤cy=IDR&frontCallbackUrl=https%3A%2F%2Fwww.payermax.com",
    "outTradeNo": "P1642410680681",
    "tradeToken": "T2024062702289232000001",
    "status": "PENDING"
  }
}
```

## 3. 获取绑定支付方式结果

商户可以通过绑定支付方式时上送的notifyUrl地址来接收绑定支付方式结果，详细结果报文请参考：支付结果通知 API。

**绑定支付方式成功通知参数示例：**

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
        "cardInfo": {
          "cardIdentifierName": "**D",
          "cardIdentifierNo": "424242******0000",
          "cardOrg": "VISA",
          "country": "GB"
        },
        "paymentMethodType": "CARD",
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

绑定支付方式成功后，PayerMax会生成paymentTokenID，后续代扣时需使用该paymentTokenID来进行代扣。

**绑定支付方式失败通知参数示例：**

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
        "cardInfo": {
          "cardIdentifierName": "**D",
          "cardIdentifierNo": "424242******0000",
          "cardOrg": "VISA"
        },
        "paymentMethodType": "CARD"
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

## 4. 发起代扣

参数说明：

- **totalAmount**：交易金额必须大于0；
- **integrate**：传固定值Direct_Payment；
- **paymentDetail.mitType**：代扣类型，SCHEDULED为周期性订阅，UNSCHEDULED为非周期性代扣；
- **paymentDetail.tokenForFutureUse**：true/false，是否需要生成token用于后续代扣；后续扣款，传false或不传；
- **paymentDetail.merchantInitiated**：true/false，是否是商户发起的交易；后续扣款，由商户发起，无需用户参与，传值为true；
- **paymentDetail.paymentTokenID**：绑定方式成功后PayerMax返回的Token。

后续代扣API文档，请参阅纯API支付 API。

不同环境的请求地址如下：

- **Prod请求地址**：https://pay-gate.payermax.com/aggregate-pay/api/gateway/orderAndPay
- **Test请求地址**：https://pay-gate-uat.payermax.com/aggregate-pay/api/gateway/orderAndPay

**请求参数示例：**

```json
{
  "version": "1.5",
  "keyVersion": "1",
  "requestTime": "2022-01-17T09:05:52.194+00:00",
  "appId": "bbd8d2639a7c4dfd8df7d005294390df",
  "merchantNo": "020113838535952",
  "data": {
    "outTradeNo": "APIFOXDEV1745388079422", // 商户下单唯一单号
    "subject": "代扣标题", // 标题
    "totalAmount": 10, // 代扣金额
    "currency": "USD", // 代扣币种
    "country": "SA", // 必填
    "userId": "test1111", // 用户号
    "language": "en",
    "reference": "test subscription",
    "frontCallbackUrl": "https://[your domain name]/[your callback URL]",
    "notifyUrl": "https://[your domain name]/[your notify URL]",
    "integrate": "Direct_Payment", // 固定值：Direct_Payment
    "expireTime": "1800",
    "terminalType": "WEB", // 终端类型，WEB、WAP or APP
    "osType": "ANDROID", // 操作系统类型 ANDROID or IOS
    "paymentDetail": {
      "paymentMethodType": "CARD", //必传，值为CARD
      "mitType": "UNSCHEDULED", // 必传，MIT类型，非周期性代扣时为UNSCHEDULED
      "tokenForFutureUse": false, // 必传，值为true，生成paymentTokenID，用于后续代扣
      "merchantInitiated": true, // false表示是需要用户参数；true表示商户发起的代扣，无需用户参与
      "paymentTokenID": "PMTOKEN20230424072005899168200035002", // 首笔代扣成功后PayerMax返回给商户的Token值
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
        "userAgent": "Mozilla/5.0"
      }
    }
  }
}
```

**商户响应参数示例：**

```json
{
  "msg": "Success.",
  "code": "APPLY_SUCCESS",
  "data": {
    "outTradeNo": "APIFOXDEV1745388079422",
    "tradeToken": "T2025042306527802000033",
    "status": "SUCCESS"
  }
}
```

## 5. 获取代扣结果

无论绑定支付方式还是后续代扣，扣款成功或失败以后，PayerMax会将扣款结果通知给商户，商户也可主动查询代扣结果。

### 5.1 使用callback获取支付结果

商户可以通过支付时上送的notifyUrl地址来接收支付结果，详细通知报文请参考：支付结果通知 API。

**代扣成功通知参数示例：**

```json
{
  "appId": "d68f5da6a0174388821a64114c6b322c",
  "code": "APPLY_SUCCESS",
  "data": {
    "channelNo": "TPC425300174064927201759000685",
    "completeTime": "2025-02-27T09:41:12.267Z",
    "country": "US",
    "currency": "USD",
    "outTradeNo": "20250227174104451122388",
    "paymentDetails": [
      {
        "cardInfo": {
          "cardIdentifierName": "**D",
          "cardIdentifierNo": "424242******0000",
          "cardOrg": "VISA",
          "country": "GB"
        },
        "paymentMethodType": "CARD",
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

**代扣失败通知参数示例：**

```json
{
  "appId": "d68f5da6a0174388821a64114c6b322c",
  "code": "PAYMENT_FAILED",
  "data": {
    "channelNo": "TPC462800174064934688659000687",
    "completeTime": "2025-02-27T09:44:00.216Z",
    "country": "US",
    "currency": "USD",
    "outTradeNo": "20250227174218727122389",
    "paymentDetails": [
      {
        "cardInfo": {
          "cardIdentifierName": "**D",
          "cardIdentifierNo": "424242******0000",
          "cardOrg": "VISA"
        },
        "paymentMethodType": "CARD"
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

接收到通知结果以后，需要响应正确的code和message给PayerMax，否则PayerMax会认为商户未能正常接收到通知消息，会重试通知6次。

**商户响应参数示例：**

```json
{
  "msg": "Success",
  "code": "SUCCESS"
}
```

### 5.2 使用查询获取支付结果

获取支付结果API文档，请参阅交易查询 API。

不同环境的请求地址如下：

- **Prod请求地址**：https://pay-gate.payermax.com/aggregate-pay/api/gateway/orderQuery
- **Test请求地址**：https://pay-gate-uat.payermax.com/aggregate-pay/api/gateway/orderQuery

**代扣结果查询请求参数示例：**

```json
{
  "version": "1.5",
  "keyVersion": "1",
  "requestTime": "2022-01-17T07:51:15.597+00:00",
  "appId": "a0dddd1f622243cb9aa1b676e808b5f8",
  "merchantNo": "02021382719993",
  "data": {
    "outTradeNo": "P1642410680681"
  }
}
```

**代扣结果查询响应参数示例：**

```json
{
  "msg": "Success.",
  "code": "APPLY_SUCCESS",
  "data": {
    "reference": "reference查询和回调返回",
    "country": "SA",
    "totalAmount": 10,
    "outTradeNo": "P1642410680681",
    "currency": "USD",
    "channelNo": "DMCP000000000177005",
    "thirdChannelNo": "4ikqJ6ktEqyRawE1dvqb9c",
    "paymentCode": "2312121212",
    "tradeToken": "T2024062702289232000001",
    "completeTime": "2023-10-20T03:28:23.092Z",
    "paymentDetails": [
      {
        "targetOrg": "*",
        "cardInfo": {
          "cardOrg": "VISA",
          "country": "UN",
          "cardIdentifierNo": "400555******0001",
          "cardIdentifierName": "**ngwei"
        },
        "paymentTokenID": "PMTOKEN20250224063712195626335000250",
        "payAmount": 10,
        "exchangeRate": "1",
        "paymentMethod": "CARD",
        "payCurrency": "USD",
        "paymentMethodType": "CARD"
      }
    ],
    "status": "SUCCESS",
    "resultMsg": ""
  }
}
```

## 6. 解绑支付方式

用户取消代扣后，商户需要为用户解绑该支付方式，解绑支付方式API文档，请参考PaymentTokenID解绑 API。

不同环境的请求地址如下：

- **Prod请求地址**：https://pay-gate.payermax.com/aggregate-pay/api/gateway/removePaymentToken
- **Test请求地址**：https://pay-gate-uat.payermax.com/aggregate-pay/api/gateway/removePaymentToken

**请求参数示例：**

```json
{
  "version": "1.5",
  "keyVersion": "1",
  "requestTime": "2022-01-22T10:00:00.500+08:00",
  "appId": "46153e2b787241ae8b01857bb087d1bd",
  "merchantNo": "010229810189301",
  "data": {
    "userId": "TEST",
    "paymentTokenID": "PMTOKEN20230424072005899168200035002",
    "removeReason": "remove"
  }
}
```

**响应参数示例：**

```json
{
  "code": "APPLY_SUCCESS",
  "msg": "Success",
  "data": {
    "paymentTokenID": "PMTOKEN20230424072005899168200035002",
    "userId": "Test",
    "paymentTokenStatus": "Deleted"
  }
}
```
