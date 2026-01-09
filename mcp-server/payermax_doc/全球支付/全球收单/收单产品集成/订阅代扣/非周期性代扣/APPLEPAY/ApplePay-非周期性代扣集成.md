# ApplePay-非周期性代扣集成

该文档介绍了非周期性代扣集成ApplePay的相关集成步骤，具体包含：绑定支付方式、获取绑定支付方式结果、发起代扣、获取代扣结果等。

## 1. 前端交互

## 2. 准备事项

根据配置与签名引导，获取商户自助平台账号、获取商户appId和密钥、配置异步通知地址、配置公钥和私钥。

## 3. 绑定支付方式

核心参数说明：

- **totalAmount**：交易金额，支持传0或者大于0的金额；
- **paymentDetail.mitType**：代扣类型，SCHEDULED标识为周期性订阅，UNSCHEDULED标识为非周期性代扣；
- **paymentDetail.tokenForFutureUse**：true/false，是否需要生成token用于后续代扣；首次绑定支付方式时，该值传true；
- **paymentDetail.merchantInitiated**：true/false，是否是商户发起的交易；首次绑定支付方式时，需要用户参与完成认证或授权，传值为false；
- **mitManagementUrl**：商户管理代扣产品的地址，用户可通过访问该地址操作订阅计划，如取消代扣等。

### 3.1 使用PayerMax收银台绑定支付方式

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
    "country": "US",
    "currency": "USD", // 代扣币种
    "userId": "test1111", // 用户号
    "language": "en",
    "reference": "test subscription",
    "frontCallbackUrl": "https://[your domain name]/[your callback URL]",
    "notifyUrl": "https://[your domain name]/[your notify URL]",
    "integrate": "Hosted_Checkout", // 固定值：Hosted_Checkout
    "expireTime": "1800",
    "mitManagementUrl": "https://[your domain name]/[your subscription management URL]", //必填
    "paymentDetail": {
      "paymentMethodType": "APPLEPAY", //必传，值为APPLEPAY
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
        "userAgent": "Mozilla/5.0 (iPad; CPU OS 18_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/22E252 [FBAN/FBIOS;FBAV/513.1.0.55.90;FBBV/735017191;FBDV/iPad13,16;FBMD/iPad;FBSN/iPadOS;FBSV/18.4.1;FBSS/2;FBID/tablet;FBLC/en_GB;FBOP/5;FBRV/737247184]"
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
    "country": "US",
    "currency": "USD", // 代扣币种
    "userId": "test1111", // 用户号
    "language": "en",
    "reference": "test subscription",
    "frontCallbackUrl": "https://[your domain name]/[your callback URL]",
    "notifyUrl": "https://[your domain name]/[your notify URL]",
    "integrate": "Hosted_Checkout", // 固定值：Hosted_Checkout
    "expireTime": "1800",
    "mitManagementUrl": "https://[your domain name]/[your subscription management URL]", //必填
    "paymentDetail": {
      "paymentMethodType": "APPLEPAY", //必传，值为APPLEPAY
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
        "userAgent": "Mozilla/5.0 (iPad; CPU OS 18_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/22E252 [FBAN/FBIOS;FBAV/513.1.0.55.90;FBBV/735017191;FBDV/iPad13,16;FBMD/iPad;FBSN/iPadOS;FBSV/18.4.1;FBSS/2;FBID/tablet;FBLC/en_GB;FBOP/5;FBRV/737247184]"
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
