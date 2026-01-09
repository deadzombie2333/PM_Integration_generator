# Google Pay™️ - 纯API模式集成

该文档介绍纯API模式下，使用Google Pay的集成步骤。

纯API集成模式下，商户需要自行构建相关的支付页面，如：收银页、支付结果页等；此外，还需要商户进行复杂的证书配置以及加解密处理。因此，该模式需要商户投入更多的研发成本。

关于纯API集成模式的更多信息，请查看集成模式概览。

## 1. 交互流程

商户需要自己先获取Google Pay Token，解密Token得到卡信息，然后将解密后的卡信息传递给PayerMax。

## 2. 集成步骤

> **注意**: 若商户已在自己收银台集成过Google Pay，可直接按步骤2.2对接即可。

### 2.1 集成Google Pay

有关于Google Pay集成的信息，请首先参考 [Google Pay API 指南](https://developers.google.com/pay/api)。

要详细了解Google Pay付款请求，请参考：[Google Pay Object Reference](https://developers.google.com/pay/api/web/reference/object)。

#### 2.1.1 配置Google Pay商户账户

1. 注册 [Google Pay Business Console](https://pay.google.com/business/console)
2. 获取核心参数：
   - `merchantId` - 谷歌商户ID
   - `paymentGatewayId` - 支付网关ID
3. 生成解密密钥：

```bash
# 生成ECDSA密钥对
openssl ecparam -genkey -name prime256v1 -noout -out google_pay_private.pem
openssl ec -in google_pay_private.pem -pubout -out google_pay_public.pem
```

#### 2.1.2 客户端集成Google Pay支付

服务端提供支付配置参数供客户端初始化Google Pay。

```javascript
const paymentsClient = new google.payments.api.PaymentsClient({
  environment: 'PRODUCTION' // 或 'TEST'
});

const paymentDataRequest = {
  apiVersion: 2,
  apiVersionMinor: 0,
  merchantInfo: {
    merchantId: 'YOUR_GOOGLE_MERCHANT_ID',
    merchantName: 'Your Store Name'
  },
  allowedPaymentMethods: [{
    type: 'CARD',
    parameters: {
      allowedAuthMethods: ['PAN_ONLY', 'CRYPTOGRAM_3DS'],
      allowedCardNetworks: ['VISA', 'MASTERCARD', 'AMEX']
    },
    tokenizationSpecification: {
      type: 'PAYMENT_GATEWAY',
      parameters: {
        'gateway': 'companyA',
        'gatewayMerchantId': 'YOUR_COMPANY_A_MID'
      }
    }
  }],
  transactionInfo: {
    totalPrice: '99.99',
    totalPriceStatus: 'FINAL',
    currencyCode: 'USD'
  }
};

paymentsClient.loadPaymentData(paymentDataRequest)
  .then(paymentData => {
    // 获取加密Token
    const token = paymentData.paymentMethodData.tokenizationData.token;
    // 发送至商户服务端
    sendToServer({ googlePayToken: token });
  })
  .catch(err => console.error(err));
```

#### 2.1.3 服务端解密Payment Token

1. 客户端返回支付令牌 `paymentMethodData`
2. 将Token在服务端进行解密，具体请参考：[如何解密付款方式令牌](https://developers.google.com/pay/api/web/guides/resources/payment-data-cryptography)

### 2.2 调用PayerMax进行支付

创建支付 `/orderAndPay` API 接口请求，其中关键字段：

- `paymentDetail.paymentMethodType`: `GOOGLEPAY`
- `paymentDetail.googlePayDetails`: 为解密后的支付信息

#### 接口请求示例

将Google Pay Token解密后的卡信息，传递给 `data.paymentDetail.googlePayDetails` 字段中。

```json
{
  "version": "1.4",
  "keyVersion": "1",
  "requestTime": "2022-02-25T09:23:06.473+00:00",
  "appId": "6666c8b036a24579974497c2f9800001",
  "merchantNo": "020213834421284",
  "data": {
    "outTradeNo": "Test1645780876511",
    "subject": "this is subject",
    "totalAmount": 1,
    "currency": "AED",
    "country": "AE",
    "userId": "userId001",
    "integrate": "Direct_Payment",
    "expireTime": "1800",
    "paymentDetail": {
      "paymentMethodType": "GOOGLEPAY",
      "buyerInfo": {
        "firstName": "James",
        "lastName": "Smith",
        "phoneNo": "903124360628",
        "email": "james@google.com",
        "clientIp": "124.156.108.193",
        "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
      },
      "googlePayDetails": {
        "authMethod": "CRYPTOGRAM_3DS",
        "cardHolderFullName": "cryptogram googlePayDetails cardHolderFullName",
        "cardNetwork": "VISA",
        "expirationMonth": "01",
        "expirationYear": "2029",
        "pan": "3604241234569621",
        "description": ""
      }
    },
    "goodsDetails": [
      {
        "goodsId": "D002",
        "goodsName": "Key buckle",
        "quantity": "2",
        "price": "0.5",
        "goodsCurrency": "AED",
        "showUrl": "http://ttt.com",
        "goodsCategory": "电脑"
      }
    ],
    "shippingInfo": {
      "firstName": "James",
      "lastName": "Smith",
      "phoneNo": "903124360628",
      "email": "James@google.com",
      "address1": "GOLGELI SOKAK NO.34, 06700",
      "city": "GAZIOSMANPASA/ANKAR",
      "country": "TR",
      "zipCode": "06700"
    },
    "billingInfo": {
      "firstName": "James",
      "lastName": "Smith",
      "phoneNo": "903124360628",
      "email": "James@google.com",
      "address1": "GOLGELI SOKAK NO.34, 06700",
      "city": "GAZIOSMANPASA/ANKAR",
      "country": "TR",
      "zipCode": "06700"
    },
    "riskParams": {
      "registerName": "lily",
      "regTime": "2023-07-01 12:08:34",
      "liveCountry": "VN",
      "payerAccount": "987654XXX",
      "payerName": "lily",
      "taxId": "1234567890"
    },
    "language": "en",
    "reference": "020213827524152",
    "terminalType": "WAP",
    "frontCallbackUrl": "https://xxx.com",
    "notifyUrl": "https://yyy.com"
  }
}
```

#### 接口响应示例

```json
{
  "code": "APPLY_SUCCESS",
  "msg": " Success.",
  "data": {
    "outTradeNo": "a1234934974321",
    "tradeToken": "T2025051210335071234567",
    "status": "SUCCESS"
  }
}
```

## 重要提示

### 品牌指南合规

如果您向客户提供 Google Pay 作为付款方式，您必须：

- 使用官方的 Google Pay 徽标和按钮素材
- 遵守《[Google Pay Android 品牌指南](https://developers.google.com/pay/api/android/guides/brand-guidelines)》
- 遵守《[Google Pay 网页品牌指南](https://developers.google.com/pay/api/web/guides/brand-guidelines)》
- 不得修改 Google Pay 素材的颜色、比例或外观

### 政策合规

您必须遵守 Google 政策：

- 所有商家都必须遵守《[Google Pay and Wallet API's Acceptable Use Policy](https://payments.developers.google.com/terms/aup)》
- 接受《[Google Pay API Terms of Service](https://payments.developers.google.com/terms/sellertos)》中定义的条款

### 3DS 验证

我们对 Google Pay PAN_ONLY 交易提供 3DS。

对于从 Google Pay PAN_ONLY 加密负载 (encrypted payload) 返回的每一笔 PAN_ONLY 凭证 (credential)，请根据指南启动 3DS 验证。
